from typing import List

import mlflow
from mlflow.tracking import MlflowClient
from mlflow.entities import Experiment
from mlflow.entities import Run

from testingframework.logging.datacollector.data_collector import DataCollector
from testingframework.logging.session import Session


class MLFlowDataCollector(DataCollector):
    def __init__(self, session: Session = Session()) -> None:
        super().__init__(session)
        self.__experiment_id: int = None
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

    def __get_mlflow_runs(self, search_query: str) -> List[Run]:
        client = mlflow.tracking.MlflowClient(self.__get_uri())
        return client.search_runs(self.__experiment_id, search_query)
    # end of '__get_mlflow_runs' function

    def get_runs(self, search_query: str) -> List[dict]:
        return [run.to_dictionary() for run in self.__get_mlflow_runs(search_query)]
    # end of 'get_runs' function

    def get_parameters(self, parameter_name: str, search_query: str) -> List[float]:
        runs: List[Run] = self.__get_mlflow_runs(search_query)

        return [run.data.params[parameter_name] for run in runs]
    # end of 'get_parameter' function

    def get_metrics(self, metric_name: str, search_query: str) -> List[float]:
        runs: List[Run] = self.__get_mlflow_runs(search_query)

        return [run.data.metrics[metric_name] for run in runs]
    # end of 'get_metric' function

    def get_artifacts(self, artifact_name: str, search_query: str) -> List[str]:
        runs: List[Run] = self.__get_mlflow_runs(search_query)

        return [run.info.artifact_uri + "/" + artifact_name for run in runs]
    # end of 'get_artifact' function
