from typing import List

from dash.development.base_component import Component
import dash_core_components as dcc
import plotly.graph_objs as go
from pandas import DataFrame

from testingframework.reportgeneration.uireportgenerator.report_templates.report_template import ReportTemplate


class BoxPlotsReportTemplate(ReportTemplate):
    @property
    def name(self) -> str:
        return "Box plots"

    def generate_report(self, runs: DataFrame) -> List[Component]:
        print("Generating box plots report")
        print(runs)

        # search metrics columns
        metrics_columns: List[str] = []
        for column in runs.columns:
            tokens = column.split(".")
            if tokens[0] == "metrics":
                metrics_columns.append(column)

        print(metrics_columns)

        # generate box plots for every metric
        data = [go.Box(y=runs[metric].tolist()) for metric in metrics_columns]

        return [dcc.Graph(figure={'data': data}, id='box-plot-1')]
