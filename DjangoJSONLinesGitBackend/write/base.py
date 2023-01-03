# -*- coding: utf-8 -*-
import logging
import pandas as pd
from git import Repo

from ..read.base import DatabaseWrapper as DatabaseWrapperRead

log = logging.getLogger(__name__)


class DatabaseWrapper(DatabaseWrapperRead):

    vendor = "jsongit-write"

    def close(self, *args, **kwargs):
        """
        Close the connection to the database.

        Export the data from the database to JSONLines files and commit the changes
        to the git repository before closing the connection.
        """
        self.export_as_json()
        super(DatabaseWrapper, self).close()

    def export_as_json(self):
        """
        Export the database tables as JSONLines files.
        
        Iterate over all tables in the database and export the data as a
        JSONLines file. Then commit all changes to the git repository.
        """
        
        sql_query = """SELECT name FROM sqlite_master
  WHERE type='table';"""
        tables = self.connection.cursor().execute(sql_query).fetchall()
        for table in tables:
            df = pd.read_sql_query(
                f"SELECT * from {table[0]}", self.connection)
            df.to_json(
                self.path / f"{table[0]}.jsonl", orient="records", lines=True)
            print(df.head)

        repo = Repo.init(self.path)
        repo.index.add(['*'])
        repo.index.commit("auto commit")
        with open(self.path / '.last_commit.txt', 'w') as last_commit:
            last_commit.write(repo.head.commit.hexsha)
        del repo
