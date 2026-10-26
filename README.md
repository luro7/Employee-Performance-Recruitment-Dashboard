# Employee Performance & Recruitment Risk Dashboard

A FastHTML dashboard and reusable SQLite-backed Python package for the Udacity Data Scientist Nanodegree.

## Motivation

Manufacturing managers need to monitor positive and negative employee performance events while understanding the **estimated likelihood of recruitment by another company**. The application presents individual and team views. The team risk estimate is the **average per-member recruitment probability**, not the probability that at least one team member will depart.

## Features

- Employee and Team selection using reusable FastHTML form components.
- **Cumulative performance chart:** positive and negative manager-recorded events grouped by date.
- **Recruitment-risk bar chart:** a trained Udacity classifier returns probabilities; color varies with risk.
- Dated manager notes table.
- Dynamic page heading: "Employee Performance" or "Team Performance".
- Reusable SQL API for names, event counts, notes, and model features.

## Repository structure

| Path | Purpose |
|---|---|
| `python-package/employee_events/` | Installable SQL package: QueryMixin, QueryBase, Employee, Team and starter SQLite database |
| `python-package/dist/employee_events-0.1.0.tar.gz` | Built source distribution required by the project rubric |
| `report/dashboard.py` | FastHTML app, employee/team routes, widgets, and visualizations |
| `report/utils.py` | Portable model-loading paths and pickle loader |
| `report/base_components/` | Original Udacity base UI components, reused via inheritance |
| `report/combined_components/` | Original Udacity multi-component layout framework |
| `assets/model.pkl` | Original Udacity pretrained model |
| `tests/test_employee_events.py` | Database, schema and Python package tests |
| `.github/workflows/tests.yml` | Installs the package, builds sdist, tests and verifies dashboard imports on pushes to main |
| `requirements.txt` | Python dependencies, including editable local package installation |

## Installation and use

Use **Python 3.10** (aligned with GitHub Actions). In the project root:

```bash
python -m pip install -r requirements.txt
python -m pytest -q
python report/dashboard.py
```

Open the local dashboard address printed by the FastHTML server (normally `http://localhost:5001`).

To build the package manually:

```bash
cd python-package
python -m pip install -e .
python setup.py sdist --dist-dir dist
```

The root `requirements.txt` already installs the local package in editable mode.

## SQL API usage

```python
from employee_events import Employee, Team

employees = Employee()
teams = Team()

employee_choices = employees.names()  # (employee name, employee ID)
team_choices = teams.names()          # (team name, team ID)

employee_event_history = employees.event_counts(employee_choices[0][1])
team_event_history = teams.event_counts(team_choices[0][1])
employee_features = employees.model_data(employee_choices[0][1])
team_features = teams.model_data(team_choices[0][1])
```

`QueryMixin` creates, uses and closes SQLite connections, returning either tuples or pandas DataFrames. `QueryBase` contains shared SQL logic; `Employee` and `Team` specialize names and model feature queries.

## Source files and CI

The original starter database and trained model are **binary files supplied by Udacity**, already copied byte-for-byte into this repository. The original model, SQLite database, and built `employee_events-0.1.0.tar.gz` source distribution are committed to this repository. GitHub Actions verifies the database, rebuilds and checks the source distribution, runs the test suite, and renders both employee/team views on every push to `main`.

A fresh checkout already includes the required binary assets and needs no separate downloads.

## Interpretation and limitations

The estimates reflect patterns in Udacity's provided model; they **do not** prove that an employee intends to leave. Manager-recorded positive and negative events may not capture all performance dimensions and could be biased. This application is a learning exercise and should not independently drive decisions about compensation, promotions, or termination.

## Acknowledgments

Udacity's [starter project](https://github.com/udacity/dsnd-dashboard-project) supplies reusable FastHTML component classes, a SQLite sample dataset, and a pickled model. The SQL package, app-specific subclasses, routes, validation tests, CI and project documentation are implemented for this project. The original Udacity license is included as `LICENSE.txt`.
