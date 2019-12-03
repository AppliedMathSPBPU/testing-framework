from abc import ABC, abstractmethod

from dash import Dash
from dash.development.base_component import Component

from testingframework.reportgeneration.uireportgenerator.report_generator import ReportGenerator


class Widget(ABC):
    @abstractmethod
    def get_layout(self, report_generator: ReportGenerator) -> Component:
        pass

    @abstractmethod
    def assign_callbacks(self, app: Dash, report_generator: ReportGenerator) -> None:
        pass
