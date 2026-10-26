"""Shared database access utilities for employee and team queries."""

import sqlite3
from functools import wraps
from pathlib import Path

import pandas as pd

db_path = Path(__file__).resolve().parent / "employee_events.db"


class QueryMixin:
    """Manage SQLite connections for all published query APIs."""

    def pandas_query(self, sql_query, params=()):
        """Execute a SELECT statement and return a pandas DataFrame."""
        with sqlite3.connect(db_path) as connection:
            return pd.read_sql_query(sql_query, connection, params=params)

    def query(self, sql_query, params=()):
        """Execute a SELECT statement and return a list of tuples."""
        with sqlite3.connect(db_path) as connection:
            return connection.execute(sql_query, params).fetchall()


def query(func):
    """Execute an SQL statement returned by a decorated function."""

    @wraps(func)
    def run_query(*args, **kwargs):
        sql_query = func(*args, **kwargs)
        with sqlite3.connect(db_path) as connection:
            return connection.execute(sql_query).fetchall()

    return run_query
