from typing import List

from dash import Dash
from dash.development.base_component import Component
import dash_html_components as html

from testingframework.reportgeneration.uireportgenerator.report_generator import ReportGenerator
from testingframework.reportgeneration.uireportgenerator.widgets.widget import Widget


class PageWidget(Widget):
    def __init__(self, pathname: str, widgets: List[Widget]) -> None:
        super().__init__()

        self.pathname = pathname
        self.widgets = widgets
    # end of '__init__' function

    def get_layout(self, report_generator: ReportGenerator) -> Component:
        return html.Div(children=[widget.get_layout(report_generator)
                                  for widget in self.widgets])
    # end of '__init__' function

    def assign_callbacks(self, app: Dash, report_generator: ReportGenerator) -> None:
        for widget in self.widgets:
            widget.assign_callbacks(app, report_generator)
