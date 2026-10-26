"""Database existence, schema, and shared SQL API tests."""

from pathlib import Path
from sqlite3 import connect

import pytest

from employee_events import Employee, QueryBase, Team


project_root = Path(__file__).resolve().parent.parent


@pytest.fixture
def db_path():
    """Provide the absolute path to the original Udacity SQLite database."""
    return project_root / "python-package" / "employee_events" / (
        "employee_events.db"
    )


def test_db_exists(db_path):
    """The packaged SQLite database must be available."""
    assert db_path.is_file()


@pytest.fixture
def db_conn(db_path):
    """Provide a SQLite connection that closes after each test."""
    with connect(db_path) as connection:
        yield connection


@pytest.fixture
def table_names(db_conn):
    """Return the database table names."""
    rows = db_conn.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table'"
    ).fetchall()
    return [row[0] for row in rows]


def test_employee_table_exists(table_names):
    """Employee table exists."""
    assert "employee" in table_names


def test_team_table_exists(table_names):
    """Team table exists."""
    assert "team" in table_names


def test_employee_events_table_exists(table_names):
    """Employee events table exists."""
    assert "employee_events" in table_names


def test_employee_queries_return_tabular_data():
    """Employees expose names, event-count frames, notes, and ML inputs."""
    employee = Employee()
    name_rows = employee.names()
    assert name_rows

    employee_id = name_rows[0][1]
    assert employee.username(employee_id)
    counts = employee.event_counts(employee_id)
    assert list(counts.columns) == [
        "event_date", "positive_events", "negative_events"
    ]
    assert {"note_date", "note"} <= set(employee.notes(employee_id).columns)
    assert list(employee.model_data(employee_id).columns) == [
        "positive_events", "negative_events"
    ]


def test_team_queries_return_tabular_data():
    """Teams expose names, events, notes, and individual model inputs."""
    team = Team()
    name_rows = team.names()
    assert name_rows

    team_id = name_rows[0][1]
    assert team.username(team_id)
    assert {"event_date", "positive_events", "negative_events"} <= set(
        team.event_counts(team_id).columns
    )
    assert {"note_date", "note"} <= set(team.notes(team_id).columns)
    assert list(team.model_data(team_id).columns) == [
        "positive_events", "negative_events"
    ]


def test_common_sql_uses_inheritance():
    """Employee and Team share the reusable base query methods."""
    assert issubclass(Employee, QueryBase)
    assert issubclass(Team, QueryBase)
