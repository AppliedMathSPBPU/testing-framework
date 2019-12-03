from abc import ABC, abstractmethod
from typing import List

from dash.development.base_component import Component
from pandas import DataFrame


class ReportTemplate(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def generate_report(self, runs: DataFrame) -> List[Component]:
        pass
