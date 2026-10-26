"""Shared employee and team SQL queries."""

from .sql_execution import QueryMixin


class QueryBase(QueryMixin):
    """Reusable SQL queries for event counts and manager notes."""

    name = ""

    def names(self):
        """Return empty choices; subclasses list their employees or teams."""
        return []

    def event_counts(self, entity_id):
        """Get total positive and negative events by date for one entity."""
        if self.name not in {"employee", "team"}:
            raise ValueError("QueryBase must be subclassed by Employee or Team")

        sql_query = f"""
            SELECT event_date,
                   SUM(positive_events) AS positive_events,
                   SUM(negative_events) AS negative_events
            FROM {self.name}
            JOIN employee_events USING ({self.name}_id)
            WHERE {self.name}.{self.name}_id = ?
            GROUP BY event_date
            ORDER BY event_date
        """
        return self.pandas_query(sql_query, (int(entity_id),))

    def notes(self, entity_id):
        """Return dated manager notes for the selected employee or team."""
        if self.name not in {"employee", "team"}:
            raise ValueError("QueryBase must be subclassed by Employee or Team")

        sql_query = f"""
            SELECT notes.note_date, notes.note
            FROM {self.name}
            JOIN notes USING ({self.name}_id)
            WHERE {self.name}.{self.name}_id = ?
            ORDER BY notes.note_date DESC
        """
        return self.pandas_query(sql_query, (int(entity_id),))
