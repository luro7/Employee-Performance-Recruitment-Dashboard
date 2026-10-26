"""FastHTML dashboard for employee and team event performance and risk."""

import matplotlib.pyplot as plt
from fasthtml.common import *

from employee_events import Employee, QueryBase, Team
from utils import load_model

from base_components import (
    BaseComponent,
    DataTable,
    Dropdown,
    MatplotlibViz,
    Radio,
)
from combined_components import CombinedComponent, FormGroup


class ReportDropdown(Dropdown):
    """Select an employee or team by readable name."""

    def build_component(self, entity_id, model):
        """Build a selector labeled for the current model type."""
        self.label = model.name.title()
        return super().build_component(entity_id, model)

    def component_data(self, entity_id, model):
        """Return display names and primary keys for the selector."""
        return model.names()


class Header(BaseComponent):
    """Heading that changes according to the selected entity type."""

    def build_component(self, entity_id, model):
        """Build the employee or team performance heading."""
        return H1(f"{model.name.title()} Performance")


class LineChart(MatplotlibViz):
    """Cumulative positive and negative events through time."""

    def visualization(self, entity_id, model):
        """Plot cumulative performance events for the selected entity."""
        event_data = model.event_counts(entity_id).fillna(0)
        fig, ax = plt.subplots(figsize=(9, 4.5))

        if event_data.empty:
            ax.text(0.5, 0.5, "No recorded events", ha="center",
                    va="center", transform=ax.transAxes)
            ax.set_xticks([])
            ax.set_yticks([])
        else:
            event_data = event_data.set_index("event_date").sort_index()
            event_data = event_data.cumsum()
            event_data.columns = ["Positive", "Negative"]
            event_data.plot(ax=ax, marker="o")

        self.set_axis_styling(ax, bordercolor="black", fontcolor="black")
        ax.set_title("Cumulative Performance Events")
        ax.set_xlabel("Event Date")
        ax.set_ylabel("Number of Events")
        fig.tight_layout()


class BarChart(MatplotlibViz):
    """Prediction-based recruitment risk visualization."""

    predictor = None

    def visualization(self, entity_id, model):
        """Plot an employee probability or team mean probability."""
        model_data = model.model_data(entity_id).fillna(0)
        if self.__class__.predictor is None:
            self.__class__.predictor = load_model()

        if model_data.empty:
            prediction = 0.0
        else:
            probabilities = self.predictor.predict_proba(model_data)[:, 1]
            prediction = (
                float(probabilities.mean())
                if model.name == "team"
                else float(probabilities[0])
            )

        risk_color = plt.cm.RdYlGn_r(prediction)
        fig, ax = plt.subplots(figsize=(9, 3))
        ax.barh(["Recruitment risk"], [prediction], color=risk_color)
        ax.set_xlim(0, 1)
        ax.set_title("Predicted Recruitment Risk")
        ax.set_xlabel("Estimated probability")
        ax.text(min(prediction + 0.02, 0.93), 0,
                f"{prediction:.1%}", va="center", fontweight="bold")
        self.set_axis_styling(ax, bordercolor="black", fontcolor="black")
        fig.tight_layout()


class Visualizations(CombinedComponent):
    """Display the time-series and probability charts together."""

    children = [LineChart(), BarChart()]
    outer_div_type = Div(cls="grid")


class NotesTable(DataTable):
    """Manager-entered notes displayed as a data table."""

    def component_data(self, entity_id, model):
        """Return dated notes for an employee or a team."""
        return model.notes(entity_id)


class DashboardFilters(FormGroup):
    """Filter controls for the chosen entity type and ID."""

    id = "top-filters"
    action = "/update_data"
    method = "POST"
    button_label = "View Performance"
    children = [
        Radio(
            values=["Employee", "Team"],
            name="profile_type",
            hx_get="/update_dropdown",
            hx_target="#selector",
        ),
        ReportDropdown(id="selector", name="user-selection"),
    ]


class Report(CombinedComponent):
    """Complete dashboard assembled from smaller inherited components."""

    children = [
        Header(),
        DashboardFilters(),
        Visualizations(),
        H2("Manager Notes"),
        NotesTable(),
    ]


app, rt = fast_app(
    hdrs=(
        Style("""
            body { max-width: 1200px; margin: 2rem auto;
                   padding: 0 1.4rem; font-family: sans-serif; }
            .grid { display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
                    gap: 1.5rem; }
            .grid img { max-width: 100%; }
            table { width: 100%; }
            #top-filters { margin: 1.3rem 0; }
        """),
    ),
)
report = Report()


@app.get("/")
def index():
    """Render the default employee performance dashboard."""
    choices = Employee().names()
    if not choices:
        return P("No employees available in the database.")
    return report(str(choices[0][1]), Employee())


@app.get("/employee/{employee_id}")
def employee_page(employee_id: str):
    """Render an individual employee's events and estimated risk."""
    return report(employee_id, Employee())


@app.get("/team/{team_id}")
def team_page(team_id: str):
    """Render aggregated team events and mean member risk."""
    return report(team_id, Team())


@app.get("/update_dropdown")
def update_dropdown(profile_type: str = "Employee"):
    """Replace dropdown choices after switching between team and employee."""
    model = Team() if profile_type == "Team" else Employee()
    return DashboardFilters.children[1](None, model)


@app.post("/update_data")
async def update_data(r):
    """Redirect submitted filters to the appropriate dashboard route."""
    data = await r.form()
    profile_type = data.get("profile_type", "Employee")
    entity_id = str(data.get("user-selection", "1"))

    if profile_type == "Team":
        return RedirectResponse(f"/team/{int(entity_id)}", status_code=303)
    return RedirectResponse(f"/employee/{int(entity_id)}", status_code=303)


if __name__ == "__main__":
    serve()
