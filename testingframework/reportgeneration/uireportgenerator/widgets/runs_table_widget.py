import dash_core_components as dcc
import dash_html_components as html
from dash import Dash
from dash.development.base_component import Component
from dash.dependencies import Input, Output, State
import dash_table as dt
import pandas as pd

from testingframework.reportgeneration.uireportgenerator.report_generator import ReportGenerator
from testingframework.reportgeneration.uireportgenerator.widgets.multi_page_widget import MultiPageWidget
from testingframework.reportgeneration.uireportgenerator.widgets.session_widget import SessionWidget
from testingframework.reportgeneration.uireportgenerator.widgets.widget import Widget


class RunsTableWidget(Widget):
    RUNS_TABLE_WIDGET_ID: str = "runs_table_widget"
    SEARCH_QUERY_ID: str = "search_query"
    SEARCH_BUTTON_ID: str = "search_button"
    RUNS_TABLE_ID: str = "runs_table"
    GENERATE_REPORT_BUTTON_ID: str = "generate_report_button"

    def get_layout(self, report_generator: ReportGenerator) -> Component:
        df = report_generator.runs

        return html.Div(children=[
            dcc.Input(id=self.SEARCH_QUERY_ID),
            html.Div(id="test"),
            html.Button("Search", id=self.SEARCH_BUTTON_ID),
            html.Button("Generate report", id=self.GENERATE_REPORT_BUTTON_ID),
            dt.DataTable(id=self.RUNS_TABLE_ID,
                         columns=[{"name": i, "id": i} for i in df.columns],
                         data=df.to_dict("re"), row_selectable='multi')
        ], id=self.RUNS_TABLE_WIDGET_ID)
    # end of 'get_component' function

    def assign_callbacks(self, app: Dash, report_generator: ReportGenerator) -> None:
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

            report_generator.data_collector.set_storage_path(storage_path)
            report_generator.data_collector.set_project(project)
            report_generator.data_collector.set_experiment(experiment)
            df = report_generator.data_collector.get_runs(query)
            print(str(df))

            return df.to_dict("records"), [{"name": i, "id": i} for i in df.columns]

        # end of 'search_runs' function

        @app.callback(Output("test", "children"),
                      [Input(self.GENERATE_REPORT_BUTTON_ID, "n_clicks")],
                      [State(self.RUNS_TABLE_ID, "data"),
                       State(self.RUNS_TABLE_ID, "selected_rows")])
        def generate_report(n_clicks, table_rows, selected_row_indices):
            print("Generate report")

            report_generator.runs = pd.DataFrame(table_rows)
            if selected_row_indices:
                report_generator.runs = report_generator.runs.loc[selected_row_indices]

            return ""
        # end of 'generate_report' function
    # end of 'assign_callbacks' function
