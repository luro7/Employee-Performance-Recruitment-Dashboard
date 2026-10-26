"""Shared SQL query API for employees and teams."""

from .sql_execution import QueryMixin


class QueryBase(QueryMixin):
    """Publish business-critical event summaries and notes."""

    name = ""

    def names(self):
        """Return empty options in the generic base implementation."""
        return []

    def event_counts(self, entity_id):
        """Return daily positive and negative event counts for an entity."""
        if self.name not in {"employee", "team"}:
            raise ValueError("Unsupported entity table")
        column = f"{self.name}_id"
        sql = f"""
            SELECT ee.event_date,
                   SUM(COALESCE(ee.positive_events, 0)) AS positive_events,
                   SUM(COALESCE(ee.negative_events, 0)) AS negative_events
            FROM {self.name} AS entity
            JOIN employee_events AS ee
              ON entity.{column} = ee.{column}
            WHERE entity.{column} = ?
            GROUP BY ee.event_date
            ORDER BY ee.event_date
        """
        return self.pandas_query(sql, (entity_id,))

    def notes(self, entity_id):
        """Return dated manager notes for an employee or an entire team."""
        if self.name not in {"employee", "team"}:
            raise ValueError("Unsupported entity table")
        column = f"{self.name}_id"
        sql = f"""
            SELECT n.note_date, n.note
            FROM notes AS n
            WHERE n.{column} = ?
            ORDER BY n.note_date DESC
        """
        return self.pandas_query(sql, (entity_id,))
