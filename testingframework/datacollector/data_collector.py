from typing import List

from abc import ABC, abstractmethod
from testingframework.datacollector.criterion import Criterion


class DataCollector(ABC):
    @abstractmethod
    def get_runs(self, criteria: List[Criterion]) -> List[dict]:
        pass

    @abstractmethod
    def get_metric(self, metric_name: str, criteria: List[Criterion]) -> List[float]:
        pass
