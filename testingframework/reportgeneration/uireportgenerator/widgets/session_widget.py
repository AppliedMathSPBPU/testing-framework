import dash_core_components as dcc
import dash_html_components as html
from dash import Dash
from dash.development.base_component import Component
from dash.dependencies import Input, Output, State

from testingframework.reportgeneration.uireportgenerator.report_generator import ReportGenerator
from testingframework.reportgeneration.uireportgenerator.widgets.widget import Widget


class SessionWidget(Widget):
    SESSION_WIDGET_ID: str = "session_widget"
    HIDDEN_DIV_ID: str = "session_hidden_div"
    STORAGE_PATH_INPUT_ID: str = "storage_path_input"
    SET_STORAGE_PATH_BUTTON_ID: str = "set_storage_path_button"
    PROJECTS_DROPDOWN_ID: str = "projects_dropdown"
    EXPERIMENTS_DROPDOWN_ID: str = "experiments_dropdown"

    def get_layout(self, report_generator: ReportGenerator) -> Component:
        return html.Div(children=[
            html.Div(id=self.HIDDEN_DIV_ID, style="hidden"),
            dcc.Input(id=self.STORAGE_PATH_INPUT_ID),
            html.Button("Set", id=self.SET_STORAGE_PATH_BUTTON_ID),
            dcc.Dropdown(id=self.PROJECTS_DROPDOWN_ID),
            dcc.Dropdown(id=self.EXPERIMENTS_DROPDOWN_ID)
        ], id=self.SESSION_WIDGET_ID)
    # end of 'get_component' function

    def assign_callbacks(self, app: Dash, report_generator: ReportGenerator) -> None:
        @app.callback(Output(self.PROJECTS_DROPDOWN_ID, 'options'),
                      [Input(self.SET_STORAGE_PATH_BUTTON_ID, 'n_clicks')],
                      [State(self.STORAGE_PATH_INPUT_ID, 'value')])
        def on_set_storage_path(n_clicks, storage_path: str):
            if n_clicks == 0 or storage_path is None:
                return []

            print("Setting storage path: " + str(storage_path))
            report_generator.data_collector.set_storage_path(storage_path)
            try:
                projects = report_generator.data_collector.list_projects()
            except FileNotFoundError:
                projects = []
            return [{'label': project_name, 'value': project_name}
                    for project_name in projects]
        # end of 'on_set_storage_path' function

        @app.callback(Output(self.EXPERIMENTS_DROPDOWN_ID, 'options'),
                      [Input(self.PROJECTS_DROPDOWN_ID, 'value')])
        def on_set_project(project_name):
            print("Setting project: " + str(project_name))
            report_generator.data_collector.set_project(project_name)
            return [{'label': experiment_name, 'value': experiment_name}
                    for experiment_name in
                    report_generator.data_collector.list_experiments()]
        # end of 'on_set_project' function

        @app.callback(Output(self.HIDDEN_DIV_ID, 'children'),
                      [Input(self.EXPERIMENTS_DROPDOWN_ID, 'value')])
        def on_set_experiment(experiment_name):
            print("Setting experiment: " + str(experiment_name))
            report_generator.data_collector.set_experiment(experiment_name)
            return []
        # end of 'on_set_experiment' function
    # end of 'assign_callbacks' function
