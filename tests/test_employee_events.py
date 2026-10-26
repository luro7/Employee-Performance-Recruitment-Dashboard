"""Database contract and employee/team SQL API tests."""

import sqlite3
from pathlib import Path

import pytest

project_root = Path(__file__).resolve().parents[1]


@pytest.fixture
def db_path():
    """Return the SQLite database stored in the package source."""
    return (
        project_root
        / "python-package"
        / "employee_events"
        / "employee_events.db"
    )


def test_db_exists(db_path):
    """Ensure project database was committed alongside the code."""
    assert db_path.is_file()


@pytest.fixture
def db_conn(db_path):
    """Open a SQLite connection and close it after each test."""
    with sqlite3.connect(db_path) as connection:
        yield connection


@pytest.fixture
def table_names(db_conn):
    """Read all database table names."""
    rows = db_conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table'"
    ).fetchall()
    return [row[0] for row in rows]


def test_employee_table_exists(table_names):
    """The employee table is required for the dashboard."""
    assert "employee" in table_names


def test_team_table_exists(table_names):
    """The team table is required for team filtering."""
    assert "team" in table_names


def test_employee_events_table_exists(table_names):
    """The employee_events table stores performance history."""
    assert "employee_events" in table_names


def test_notes_table_exists(table_names):
    """The notes table stores manager commentary."""
    assert "notes" in table_names


def test_employee_and_team_queries(db_conn):
    """Verify that SQL package data is ready for dashboard use."""
    from employee_events import Employee, Team

    employee_id = db_conn.execute(
        "SELECT employee_id FROM employee ORDER BY employee_id LIMIT 1"
    ).fetchone()[0]
    team_id = db_conn.execute(
        "SELECT team_id FROM team ORDER BY team_id LIMIT 1"
    ).fetchone()[0]

    employee = Employee()
    team = Team()
    assert employee.names()
    assert team.names()
    assert employee.username(employee_id)
    assert team.username(team_id)
    for api, entity_id in ((employee, employee_id), (team, team_id)):
        counts = api.event_counts(entity_id)
        assert {"event_date", "positive_events", "negative_events"} <= set(
            counts.columns
        )
        assert {"note_date", "note"} <= set(api.notes(entity_id).columns)
        assert {"positive_events", "negative_events"} <= set(
            api.model_data(entity_id).columns
        )
