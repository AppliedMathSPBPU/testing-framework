from typing import List

from dash import Dash
from dash.development.base_component import Component
import dash_html_components as html

from testingframework.reportgeneration.uireportgenerator.widgets.widget import Widget


class PageWidget(Widget):
    def __init__(self, pathname: str, widgets: List[Widget]) -> None:
        super().__init__()

        self.pathname = pathname
        self.widgets = widgets
    # end of '__init__' function

    def get_layout(self) -> Component:
        return html.Div(children=[widget.get_layout()
                                  for widget in self.widgets])
    # end of 'get_layout' function

    def assign_callbacks(self, app: Dash) -> None:
        for widget in self.widgets:
            widget.assign_callbacks(app)
    # end of 'assign_callbacks' function
