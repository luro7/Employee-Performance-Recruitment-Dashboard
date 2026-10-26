"""Shared, safe SQLite execution utilities for the employee events package."""

from functools import wraps
from pathlib import Path
from sqlite3 import connect

import pandas as pd


db_path = Path(__file__).resolve().parent / "employee_events.db"


class QueryMixin:
    """Manage one SQLite connection per query for reusable SQL consumers."""

    def query(self, sql_query, params=()):
        """Execute SQL and return rows as a list of tuples."""
        if not db_path.is_file():
            raise FileNotFoundError(f"Database not found: {db_path}")
        with connect(db_path) as connection:
            return connection.execute(sql_query, params).fetchall()

    def pandas_query(self, sql_query, params=()):
        """Execute SQL and return tabular results as a pandas DataFrame."""
        if not db_path.is_file():
            raise FileNotFoundError(f"Database not found: {db_path}")
        with connect(db_path) as connection:
            return pd.read_sql_query(sql_query, connection, params=params)


def query(func):
    """Run the SQL returned by a decorated method and return tuple rows."""
    @wraps(func)
    def run_query(*args, **kwargs):
        sql_query = func(*args, **kwargs)
        return QueryMixin().query(sql_query)

    return run_query
