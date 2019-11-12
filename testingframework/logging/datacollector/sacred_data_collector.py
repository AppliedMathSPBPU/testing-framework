from typing import List

from testingframework.logging.datacollector import Criterion
from testingframework.logging.datacollector.data_collector import DataCollector


class SacredDataCollector(DataCollector):
    def get_runs(self, criteria: List[Criterion]) -> List[dict]:
        pass

    def get_metric_values(self, metric_name: str, criteria: List[Criterion]) -> List[float]:
        pass
