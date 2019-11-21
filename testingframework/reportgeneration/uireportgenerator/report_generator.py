from typing import List

from testingframework.logging.datacollector.data_collector import DataCollector
from testingframework.logging.datacollector.mlflow_data_collector import MLflowDataCollector
from testingframework.reportgeneration.uireportgenerator.report_template import ReportTemplate
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.development.base_component import Component
from dash.dependencies import Input, Output


class UIReportGenerator:
    _STORAGE_PATH_INPUT_ID: str = "storage_path_input"
    _PROJECTS_DROPDOWN_ID: str = "projects_dropdown"
    _EXPERIMENTS_DROPDOWN_ID: str = "experiments_dropdown"
    _SESSION_WIDGET_ID: str = "session_widget"

    def __init__(self):
        self._report_templates: List[ReportTemplate] = []
        # TODO: other data collectors
        self._data_collector: DataCollector = MLflowDataCollector()
        self._app = dash.Dash("Report Generation UI")

        self._app.layout = self._layout()

        self._assign_callbacks()
    # end of '__init__' function

    def _layout(self) -> Component:
        return html.Div(children=[
            self._session_widget()
        ])
    # end of '_layout' function

    def _session_widget(self) -> Component:
        output = html.Div(children=[
            dcc.Input(id=self._STORAGE_PATH_INPUT_ID),
            dcc.Dropdown(id=self._PROJECTS_DROPDOWN_ID),
            dcc.Dropdown(id=self._EXPERIMENTS_DROPDOWN_ID)
        ], id=self._SESSION_WIDGET_ID)

        return output
    # end of '_session_widget' function

    def _assign_callbacks(self) -> None:
        @self._app.callback(Output(component_id=self._PROJECTS_DROPDOWN_ID, component_property='options'),
                            [Input(component_id=self._STORAGE_PATH_INPUT_ID, component_property='value')])
        def set_storage_path(storage_path):
            print("Setting storage path: " + storage_path)
            self._data_collector.set_storage_path(storage_path)
            try:
                projects = self._data_collector.list_projects()
            except FileNotFoundError:
                projects = []
            return [{'label': project_name, 'value': project_name}
                    for project_name in projects]

        @self._app.callback(Output(component_id=self._EXPERIMENTS_DROPDOWN_ID, component_property='options'),
                            [Input(component_id=self._PROJECTS_DROPDOWN_ID, component_property='value')])
        def set_project(project_name):
            print("Setting project: " + project_name)
            self._data_collector.set_project(project_name)
            return [{'label': experiment_name, 'value': experiment_name}
                    for experiment_name in self._data_collector.list_experiments()]
    # end of '_assign_callbacks' function

    def add_report_template(self, template: ReportTemplate):
        self._report_templates.append(template)
    # end of '__init__' function

    def start_ui(self):
        self._app.run_server()
    # end of '__init__' function
