from typing import Dict

from testingframework.reportgeneration.uireportgenerator.report_generator import ReportGenerator
from testingframework.reportgeneration.uireportgenerator.report_templates.report_template import ReportTemplate
import dash

from testingframework.reportgeneration.uireportgenerator.widgets.page_widget import PageWidget
from testingframework.reportgeneration.uireportgenerator.widgets.multi_page_widget import MultiPageWidget
from testingframework.reportgeneration.uireportgenerator.widgets.report_widget import ReportWidget
from testingframework.reportgeneration.uireportgenerator.widgets.runs_table_widget import RunsTableWidget
from testingframework.reportgeneration.uireportgenerator.widgets.session_widget import SessionWidget


class UIReportGenerator(ReportGenerator):
    def __init__(self):
        super().__init__()

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
        pages_widget: MultiPageWidget = MultiPageWidget()
        pages_widget.add_page(PageWidget("", [SessionWidget(), RunsTableWidget(), ReportWidget(self.report_templates)]))
        #pages_widget.add_page(PageWidget("report", [ReportWidget(self.report_templates)]))

        # assign dash layout
        self.app.layout = pages_widget.get_layout(self)

        # assign dash callbacks
        pages_widget.assign_callbacks(self.app, self)

        # start server
        self.app.run_server()
    # end of 'start_ui' function
