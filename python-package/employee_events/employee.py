"""Employee-specific SQL API."""

from .query_base import QueryBase


class Employee(QueryBase):
    """Read employee names, performance events, notes and model features."""

    name = "employee"

    def names(self):
        """Return (full name, employee ID) pairs sorted by employee name."""
        return self.query("""
            SELECT first_name || ' ' || last_name AS full_name,
                   employee_id
            FROM employee
            ORDER BY last_name, first_name
        """)

    def username(self, entity_id):
        """Return the chosen employee's full name as a one-row tuple list."""
        return self.query("""
            SELECT first_name || ' ' || last_name AS full_name
            FROM employee
            WHERE employee_id = ?
        """, (int(entity_id),))

    def model_data(self, entity_id):
        """Return the two aggregated event features for the risk model."""
        return self.pandas_query("""
            SELECT SUM(positive_events) AS positive_events,
                   SUM(negative_events) AS negative_events
            FROM employee
            JOIN employee_events USING (employee_id)
            WHERE employee.employee_id = ?
        """, (int(entity_id),))
