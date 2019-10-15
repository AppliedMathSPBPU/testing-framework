from typing import List

from testingframework.datacollector.criterion import Criterion
from testingframework.datacollector.data_collector import DataCollector


class MLFlowDataCollector(DataCollector):
    def get_runs(self, criteria: List[Criterion]) -> List[dict]:
        pass

    def get_metric(self, metric_name: str, criteria: List[Criterion]) -> List[float]:
        pass
