import os
import sys
import shutil

from django.db.backends.sqlite3.creation import DatabaseCreation as Sqlite3DatabaseCreation


class DatabaseCreation(Sqlite3DatabaseCreation):

    def _create_test_db(self, verbosity, autoclobber, keepdb=False):
        test_database_name = self._get_test_db_name()

        if keepdb:
            return test_database_name
        if not self.is_in_memory_db(test_database_name):
            # Erase the old test database
            if verbosity >= 1:
                self.log(
                    "Destroying old test database for alias %s..."
                    % (self._get_database_display_str(verbosity, test_database_name),)
                )
            if os.access(test_database_name, os.F_OK):
                if not autoclobber:
                    confirm = input(
                        "Type 'yes' if you would like to try deleting the test "
                        "database '%s', or 'no' to cancel: " % test_database_name
                    )
                if autoclobber or confirm == "yes":
                    try:
                        shutil.rmtree(test_database_name)
                    except Exception as e:
                        self.log(
                            "Got an error deleting the old test database: %s" % e)
                        sys.exit(2)
                else:
                    self.log("Tests cancelled.")
                    sys.exit(1)
        return test_database_name

    def _destroy_test_db(self, test_database_name, verbosity):
        if test_database_name and not self.is_in_memory_db(test_database_name):
            # Remove the SQLite database file and git repository
            shutil.rmtree(test_database_name)
