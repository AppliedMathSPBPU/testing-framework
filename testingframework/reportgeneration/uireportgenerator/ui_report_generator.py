from typing import Dict

import dash
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html

from testingframework.logging.datacollector.mlflow_data_collector import MLflowDataCollector

from testingframework.reportgeneration.uireportgenerator.report_templates.report_template import ReportTemplate
from testingframework.reportgeneration.uireportgenerator.widgets.column_layout_widget import ColumnLayoutWidget
from testingframework.reportgeneration.uireportgenerator.widgets.page_widget import PageWidget
from testingframework.reportgeneration.uireportgenerator.widgets.multi_page_widget import MultiPageWidget
from testingframework.reportgeneration.uireportgenerator.widgets.report_widget import ReportWidget
from testingframework.reportgeneration.uireportgenerator.widgets.runs_table_widget import RunsTableWidget
from testingframework.reportgeneration.uireportgenerator.widgets.session_widget import SessionWidget


class UIReportGenerator:
    def __init__(self):
        super().__init__()

        self.data_collector: MLflowDataCollector = MLflowDataCollector()
        self.runs: pd.DataFrame = self.data_collector.get_runs()
        self.report_templates: Dict[str, ReportTemplate] = {}
        self.app = dash.Dash("Report Generation UI")
    # end of '__init__' function

    def add_report_template(self, template: ReportTemplate):
        self.report_templates.update({template.name: template})
    # end of 'add_report_template' function

    def start_ui(self):
        # dash can huff my shorts
        self.app.config.suppress_callback_exceptions = True

        # create multi-page widget
        # pages_widget: MultiPageWidget = MultiPageWidget()
        # pages_widget.add_page(PageWidget("", [SessionWidget(), RunsTableWidget(), ReportWidget(self.report_templates)]))
        # #pages_widget.add_page(PageWidget("report", [ReportWidget(self.report_templates)]))

        # create column layout widget
        layout = ColumnLayoutWidget()
        layout.add_column(PageWidget("", [SessionWidget(self.data_collector),
                                          RunsTableWidget(self.data_collector,
                                                          self.runs)]))
        layout.add_column(PageWidget("", [ReportWidget(self.report_templates,
                                                       self.runs)]))

        # assign dash layout
        # self.app.layout = pages_widget.get_layout(self)
        self.app.layout = layout.get_layout()

        # assign dash callbacks
        # pages_widget.assign_callbacks(self.app, self)
        layout.assign_callbacks(self.app)

        # start server
        self.app.run_server(debug=True)
    # end of 'start_ui' function
