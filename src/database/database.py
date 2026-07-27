import sqlite3
import pandas as pd

from src.config.paths import DATABASE_PATH


class DatabaseManager:

    def __init__(self):
        self.db_path = DATABASE_PATH

    def connect(self):
        """Create SQLite connection."""
        return sqlite3.connect(self.db_path)

    def create_table(self, dataframe: pd.DataFrame, table_name: str):
        """
        Creates a table automatically from dataframe columns.
        Existing table is replaced.
        """

        conn = self.connect()

        dataframe.to_sql(
            table_name,
            conn,
            if_exists="replace",
            index=False
        )

        conn.close()

    def read_table(self, table_name: str):

        conn = self.connect()

        df = pd.read_sql(
            f"SELECT * FROM {table_name}",
            conn
        )

        conn.close()

        return df

    def execute(self, query):

        conn = self.connect()

        cursor = conn.cursor()

        cursor.execute(query)

        conn.commit()

        conn.close()

    def table_exists(self, table_name):

        conn = self.connect()

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type='table'
            AND name=?
            """,
            (table_name,)
        )

        result = cursor.fetchone()

        conn.close()

        return result is not None

    def get_table_names(self):

        conn = self.connect()

        query = """
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        ORDER BY name
        """

        tables = pd.read_sql(query, conn)

        conn.close()

        return tables["name"].tolist()