import dash_core_components as dcc
import dash_html_components as html
from dash import Dash
from dash.development.base_component import Component
from dash.dependencies import Input, Output, State
import dash_table as dt
import pandas as pd

from testingframework.logging.datacollector.data_collector import DataCollector
from testingframework.reportgeneration.uireportgenerator.report_generator import ReportGenerator
from testingframework.reportgeneration.uireportgenerator.widgets.session_widget import SessionWidget
from testingframework.reportgeneration.uireportgenerator.widgets.widget import Widget


class RunsTableWidget(Widget):
    RUNS_TABLE_WIDGET_ID: str = "runs_table_widget"
    SEARCH_QUERY_ID: str = "search_query"
    SEARCH_BUTTON_ID: str = "search_button"
    RUNS_TABLE_ID: str = "runs_table"
    GENERATE_REPORT_BUTTON_ID: str = "generate_report_button"

    def __init__(self, data_collector: DataCollector, runs: pd.DataFrame):
        super().__init__()

        self._runs = runs
        self._data_collector = data_collector
    # end of '__init__' function

    def get_layout(self) -> Component:
        return html.Div(children=[
            dcc.Input(id=self.SEARCH_QUERY_ID),
            html.Div(id="test"),
            html.Button("Search", id=self.SEARCH_BUTTON_ID),
            html.Button("Generate report", id=self.GENERATE_REPORT_BUTTON_ID),
            dt.DataTable(id=self.RUNS_TABLE_ID,
                         columns=[{"name": i, "id": i} for i in self._runs.columns],
                         data=self._runs.to_dict("re"), row_selectable='multi')
        ], id=self.RUNS_TABLE_WIDGET_ID)
    # end of 'get_layout' function

    def assign_callbacks(self, app: Dash) -> None:
        @app.callback([Output(self.RUNS_TABLE_ID, 'data'),
                       Output(self.RUNS_TABLE_ID, 'columns')],
                      [Input(self.SEARCH_BUTTON_ID, 'n_clicks'),
                       Input(SessionWidget.SET_STORAGE_PATH_BUTTON_ID, 'n_clicks'),
                       Input(SessionWidget.PROJECTS_DROPDOWN_ID, 'value'),
                       Input(SessionWidget.EXPERIMENTS_DROPDOWN_ID, 'value')],
                      [State(SessionWidget.STORAGE_PATH_INPUT_ID, 'value'),
                       State(self.SEARCH_QUERY_ID, 'value')])
        def search_runs(n_clicks, storage_clicks, project,
                        experiment, storage_path, query):
            print("Search runs: " + str(query))

            self._data_collector.set_storage_path(storage_path)
            self._data_collector.set_project(project)
            self._data_collector.set_experiment(experiment)
            df = self._data_collector.get_runs(query)
            print(str(df))

            return df.to_dict("records"), [{"name": i, "id": i} for i in df.columns]

        # end of 'search_runs' function

        @app.callback(Output("test", "children"),
                      [Input(self.GENERATE_REPORT_BUTTON_ID, "n_clicks")],
                      [State(self.RUNS_TABLE_ID, "data"),
                       State(self.RUNS_TABLE_ID, "selected_rows")])
        def generate_report(n_clicks, table_rows, selected_row_indices):
            print("Generate report")

            self._runs = pd.DataFrame(table_rows)
            if selected_row_indices:
                self._runs = self._runs.loc[selected_row_indices]

            return ""
        # end of 'generate_report' function
    # end of 'assign_callbacks' function
