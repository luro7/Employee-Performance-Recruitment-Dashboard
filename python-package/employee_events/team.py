"""SQL-backed API for groups of employees."""

from .query_base import QueryBase


class Team(QueryBase):
    """Access team labels, events, notes and per-member model inputs."""

    name = "team"

    def names(self):
        """Return (team name, team ID) for every team."""
        return self.query("""
            SELECT team_name, team_id
            FROM team
            ORDER BY team_name, team_id
        """)

    def username(self, entity_id):
        """Return the name for the selected team."""
        return self.query("""
            SELECT team_name FROM team WHERE team_id = ?
        """, (entity_id,))

    def model_data(self, entity_id):
        """Return one event-count row per employee in a team."""
        return self.pandas_query("""
            SELECT COALESCE(SUM(ee.positive_events), 0) AS positive_events,
                   COALESCE(SUM(ee.negative_events), 0) AS negative_events
            FROM employee AS e
            LEFT JOIN employee_events AS ee
              ON e.employee_id = ee.employee_id
            WHERE e.team_id = ?
            GROUP BY e.employee_id
            ORDER BY e.employee_id
        """, (entity_id,))
