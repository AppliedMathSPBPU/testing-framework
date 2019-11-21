from typing import List, Set

import mlflow
from pandas import DataFrame
from mlflow.tracking import MlflowClient
from mlflow.entities import Experiment
from mlflow.entities import Run
import pathlib as pth

from testingframework.logging.datacollector.data_collector import DataCollector
from testingframework.logging.session import Session


class MLflowDataCollector(DataCollector):
    def __init__(self, session: Session = Session()) -> None:
        self.__experiment_id: int = None
        super().__init__(session)
    # end of '__init__' function

    def __get_uri(self):
        return self._session.storage_path + "/" + self._session.project_name
    # end of '__get_uri' function

    def set_project(self, project_name: str = "") -> None:
        """Set active project. Sets 'Default' if doesn't exist.

        Args:
            project_name (str): Project name.
        """
        # TODO: catch doesn't exist
        self._session.project_name = project_name

        self.set_experiment()
    # end of 'set_project' function

    def set_experiment(self, experiment_name: str = "") -> None:
        """Set active experiment. Sets 'Default' if doesn't exist.

        Args:
            experiment_name (str): Experiment name.
        """
        self._session.experiment_name = experiment_name
        client = MlflowClient(self.__get_uri())
        # TODO: catch doesn't exist
        experiment: Experiment = client.get_experiment_by_name(self._session.experiment_name)
        self.__experiment_id = experiment.experiment_id
    # end of 'set_experiment' function

    def set_storage_path(self, storage_path: str = "") -> None:
        """Set logged data local storage path. Default: './projects'

        Args:
            storage_path (str): Local storage path.
        """
        self._session.storage_path = storage_path
    # end of 'set_storage_path' function

    def __get_mlflow_runs(self, search_query: str = "") -> List[Run]:
        client = mlflow.tracking.MlflowClient(self.__get_uri())
        return client.search_runs(self.__experiment_id, search_query)
    # end of '__get_mlflow_runs' function

    def get_runs(self, search_query: str = "") -> DataFrame:
        mlflow.set_tracking_uri(self.__get_uri())
        return mlflow.search_runs(filter_string=search_query)
    # end of 'get_runs' function

    def get_parameter_values(self, parameter_name: str, runs: DataFrame) -> List[str]:
        return runs[:, "parameters." + parameter_name]
    # end of 'get_parameter' function

    def get_metric_values(self, metric_name: str, runs: DataFrame) -> List[float]:
        return runs[:, "metrics." + metric_name]
    # end of 'get_metric' function

    def get_artifacts(self, artifact_name: str, runs: DataFrame, artifact_path: str = "") -> List[str]:
        return [uri + "/" + artifact_path + "/" + artifact_name for uri in runs[:, "artifact_uri"]]
    # end of 'get_artifact' function

    def list_metrics(self, runs: DataFrame) -> List[str]:
        metric_names: Set[str] = set()

        for run in runs:
            metrics: DataFrame = run["data"]["metrics"]
            metric_names.update(metrics.keys())

        return list(metric_names)
    # end of 'list_metrics' function

    def list_experiments(self) -> List[str]:
        return [experiment.name
                for experiment in MlflowClient(self.__get_uri()).list_experiments()]
    # end of 'list_experiments' function

    def list_projects(self) -> List[str]:
        output: List[str] = []

        for path in pth.Path(self.__get_uri()).iterdir():
            if path.is_dir():
                output.append(path.name)

        return output
    # end of 'list_projects' function
