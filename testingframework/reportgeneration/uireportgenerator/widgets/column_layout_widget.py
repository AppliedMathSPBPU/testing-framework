from typing import List

from dash import Dash
from dash.development.base_component import Component
import dash_html_components as html

from testingframework.reportgeneration.uireportgenerator.widgets.widget import Widget


class ColumnLayoutWidget(Widget):
    COLUMN_LAYOUT_TABLE_ID: str = "column_layout_table"

    def __init__(self) -> None:
        super().__init__()

        self._columns: List[Widget] = []
    # end of '__init__' function

    def add_column(self, column: Widget) -> None:
        self._columns.append(column)
    # end of 'add_column' function

    def get_layout(self) -> Component:
        return html.Table(
            children=html.Tr([html.Th(col.get_layout())
                              for col in self._columns]),
            style={"width": "100%"}
        )
    # end of 'get_layout' function

    def assign_callbacks(self, app: Dash) -> None:
        for col in self._columns:
            col.assign_callbacks(app)
    # end of 'assign_callbacks' function
