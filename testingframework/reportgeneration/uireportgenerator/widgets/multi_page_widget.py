from typing import Dict

from dash import Dash
from dash.development.base_component import Component
import dash_html_components as html
from dash.dependencies import Input, Output

from testingframework.reportgeneration.uireportgenerator.widgets.page_widget import PageWidget
from testingframework.reportgeneration.uireportgenerator.widgets.widget import Widget


class MultiPageWidget(Widget):
    LOCATION_ID: str = "location"
    PAGE_CONTENT_ID: str = "page_content"

    def __init__(self) -> None:
        super().__init__()

        self._pages: Dict[str, Widget] = {}
    # end of '__init__' function

    def add_page(self, page: PageWidget) -> None:
        self._pages.update({page.pathname: page})
    # end of 'add_page' function

    def get_layout(self) -> Component:
        return html.Div(children=[
            html.Plaintext(id=self.LOCATION_ID),
            html.Div(id=self.PAGE_CONTENT_ID,
                     children=self._pages.get("").get_layout())
        ])
    # end of 'get_layout' function

    def assign_callbacks(self, app: Dash) -> None:
        for page in self._pages.values():
            page.assign_callbacks(app)

        @app.callback(Output(self.PAGE_CONTENT_ID, "children"),
                      [Input(self.LOCATION_ID, "children")])
        def update_page_content(pathname):
            if pathname is None:
                pathname = ""
                
            print("Switching to " + pathname)

            if pathname in self._pages:
                return self._pages.get(pathname).get_layout()

            print("No such page found!")
            return []
        # end of 'update_page_content' function
    # end of 'assign_callbacks' function
