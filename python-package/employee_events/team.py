"""Team-specific SQL API."""

from .query_base import QueryBase


class Team(QueryBase):
    """Read team names, aggregated events, notes and per-member features."""

    name = "team"

    def names(self):
        """Return (team name, team ID) pairs sorted by team name."""
        return self.query("""
            SELECT team_name, team_id
            FROM team
            ORDER BY team_name
        """)

    def username(self, entity_id):
        """Return the chosen team's name as a one-row tuple list."""
        return self.query("""
            SELECT team_name
            FROM team
            WHERE team_id = ?
        """, (int(entity_id),))

    def model_data(self, entity_id):
        """Return event features per employee for mean team recruitment risk."""
        return self.pandas_query("""
            SELECT positive_events, negative_events
            FROM (
                SELECT employee_id,
                       SUM(positive_events) AS positive_events,
                       SUM(negative_events) AS negative_events
                FROM team
                JOIN employee_events USING (team_id)
                WHERE team.team_id = ?
                GROUP BY employee_id
            )
        """, (int(entity_id),))
