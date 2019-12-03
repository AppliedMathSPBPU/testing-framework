from testingframework.logging.datacollector.data_collector import DataCollector
from testingframework.logging.datacollector.mlflow_data_collector import MLflowDataCollector
import pandas as pd


class ReportGenerator:
    def __init__(self):
        # TODO: other data collectors
        self.data_collector: MLflowDataCollector = MLflowDataCollector()
        self.runs: pd.DataFrame = self.data_collector.get_runs()
    # end of '__init__' function
