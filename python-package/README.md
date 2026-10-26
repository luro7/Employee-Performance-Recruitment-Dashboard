# employee_events SQL API

This installable package reads the local Udacity SQLite database using a shared
`QueryMixin` and the `QueryBase`, `Employee`, and `Team` classes.

Install with `pip install -e ./python-package` from the repository root.

```python
from employee_events import Employee, Team

employees = Employee().names()
daily_events = Employee().event_counts(employees[0][1])
teams = Team().names()
```

The upstream `employee_events.db` is preserved with the package distribution.
