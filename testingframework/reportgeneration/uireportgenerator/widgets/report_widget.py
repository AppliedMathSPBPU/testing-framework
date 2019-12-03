from typing import Dict

from dash import Dash
from dash.development.base_component import Component
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


from testingframework.reportgeneration.uireportgenerator.report_generator import ReportGenerator
from testingframework.reportgeneration.uireportgenerator.report_templates.report_template import ReportTemplate
from testingframework.reportgeneration.uireportgenerator.widgets.widget import Widget


class ReportWidget(Widget):
    REPORT_WIDGET_ID = "report_widget"
    BACK_BUTTON_ID = "back_button"
    EXPORT_BUTTON_ID = "export_button"
    TEMPLATE_DROPDOWN_ID = "template_dropdown"
    REPORT_DIV_ID = "report_div"

    def __init__(self, report_templates: Dict[str, ReportTemplate]) -> None:
        super().__init__()

        self._report_templates: Dict[str, ReportTemplate] = report_templates

    def get_layout(self, report_generator: ReportGenerator) -> Component:
        return html.Div(id=self.REPORT_WIDGET_ID, children=[
            html.Button("Back", id=self.BACK_BUTTON_ID),
            html.Button("Export", id=self.EXPORT_BUTTON_ID),
            dcc.Dropdown(id=self.TEMPLATE_DROPDOWN_ID,
                         options=[{"label": t.name, "value": t.name}
                                  for t in self._report_templates.values()
                                  ]),
            html.Div(id=self.REPORT_DIV_ID)
        ])

    def assign_callbacks(self, app: Dash, report_generator: ReportGenerator) -> None:
        @app.callback(Output(self.REPORT_DIV_ID, 'children'),
                      [Input(self.TEMPLATE_DROPDOWN_ID, 'value')])
        def change_template(template_name):
            if template_name is None:
                return []
            template: ReportTemplate = self._report_templates[template_name]
            return template.generate_report(report_generator.runs)
