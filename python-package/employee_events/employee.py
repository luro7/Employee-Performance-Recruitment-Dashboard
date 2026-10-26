"""SQL-backed API for individual employees."""

from .query_base import QueryBase


class Employee(QueryBase):
    """Access employee labels, events, notes and model inputs."""

    name = "employee"

    def names(self):
        """Return (full name, employee ID) for every employee."""
        return self.query("""
            SELECT first_name || ' ' || last_name AS full_name, employee_id
            FROM employee
            ORDER BY last_name, first_name, employee_id
        """)

    def username(self, entity_id):
        """Return the full name for the selected employee."""
        return self.query("""
            SELECT first_name || ' ' || last_name AS full_name
            FROM employee
            WHERE employee_id = ?
        """, (entity_id,))

    def model_data(self, entity_id):
        """Return total positive and negative events for the classifier."""
        return self.pandas_query("""
            SELECT COALESCE(SUM(ee.positive_events), 0) AS positive_events,
                   COALESCE(SUM(ee.negative_events), 0) AS negative_events
            FROM employee AS e
            LEFT JOIN employee_events AS ee USING (employee_id)
            WHERE e.employee_id = ?
        """, (entity_id,))
