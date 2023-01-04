# -*- coding: utf-8 -*-
import logging
from pathlib import Path
from os import mkdir
from os.path import exists

from django.db.backends.sqlite3.base import DatabaseWrapper as BaseDatabaseWrapper
import pandas as pd
from git import Repo
from git.exc import InvalidGitRepositoryError

from .creation import DatabaseCreation

log = logging.getLogger(__name__)


class DatabaseWrapper(BaseDatabaseWrapper):
    """
    Django SQLite database backend storing the db file as json on git.
    """
    path = ""
    creation_class = DatabaseCreation

    def __init__(self, *args, **kwargs):
        super(DatabaseWrapper, self).__init__(*args, **kwargs)

    def get_new_connection(self, conn_params):
        """
        Get a new connection to the database.

        Initializes the git repository and updates the connection
        parameters to use the correct sqlite database file.

        Parameters:
            conn_params: A dictionary of connection parameters.

        Returns:
            A new connection to the database.
        """

        self.path = Path(conn_params['database'])
        self.git_init()
        conn_params['database'] = "shared" if conn_params['database'] == "shared" else self.path / '.db.sqlite'
        connection = super(
            DatabaseWrapper, self).get_new_connection(conn_params)
        self.update(connection)
        return connection

    def git_init(self):
        """
        Initialize the git repository.

        If the repository does not exist, create it and add a '.gitignore' file
        ignoring all files except for JSONLines files. Commit the '.gitignore' file
        and store the commit hash in a '.last_commit.txt' file.
        """
        repo: Repo
        if not exists(self.path):
            log.info(f"init git repository in {self.path}")
            mkdir(self.path)
            with open(self.path / '.gitignore', 'w') as gitgnore:
                gitgnore.write('*\n!*jsonl')
            repo = Repo.init(self.path)
            repo.index.add(['.gitignore'])
            repo.index.commit("initial commit")
            with open(self.path / '.last_commit.txt', 'w') as last_commit:
                last_commit.write(repo.head.commit.hexsha)
            log.info(f"last commit is {repo.head.commit.hexsha}")

    def update(self, connection):
        """
        Update the database with new data from the JSONLines files.

        If the commit hash stored in '.last_commit.txt' is different from the
        current commit hash, reload the database and update it with the data from
        the JSONLines files.
        """

        repo = Repo(self.path)
        hexsha = repo.head.commit.hexsha
        with open(self.path / '.last_commit.txt') as last_commit:
            last_hexsha = last_commit.read()
        if last_hexsha != hexsha:
            self.reload()
            sql_query = """SELECT name FROM sqlite_master WHERE type='table';"""
            tables = self.connection.cursor().execute(sql_query).fetchall()
            for table_name in map(lambda x: x[0], tables):
                self.connection.cursor().execute(f"TRUNCATE table")
                df = pd.read_json(
                    self.path / f"{table_name[0]}.jsonl", orient="records", lines=True)
                df.to_sql(table_name[0], self.connection, index=False)
                del df
