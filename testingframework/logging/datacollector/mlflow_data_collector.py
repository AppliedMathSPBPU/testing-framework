from typing import List, Set

import mlflow
from mlflow.tracking import MlflowClient
from mlflow.entities import Experiment
from mlflow.entities import Run

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

    def get_runs(self, search_query: str = "") -> List[dict]:
        return [run.to_dictionary() for run in self.__get_mlflow_runs(search_query)]
    # end of 'get_runs' function

    def get_parameter_values(self, parameter_name: str, runs: List[dict]) -> List[str]:
        output: List[str] = []

        for run in runs:
            try:
                output.append(run["data"]["parameters"][parameter_name])
            except KeyError:
                output.append("")

        return output
    # end of 'get_parameter' function

    def get_metric_values(self, metric_name: str, runs: List[dict]) -> List[float]:
        output: List[float] = []

        for run in runs:
            try:
                output.append(run["data"]["metrics"][metric_name])
            except KeyError:
                output.append(float("NaN"))

        return output
    # end of 'get_metric' function

    def get_artifacts(self, artifact_name: str, search_query: str = "") -> List[str]:
        runs: List[Run] = self.__get_mlflow_runs(search_query)

        return [run.info.artifact_uri + "/" + artifact_name for run in runs]
    # end of 'get_artifact' function

    def list_metrics(self, runs: List[dict]) -> List[str]:
        metric_names: Set[str] = set()

        for run in runs:
            metrics: dict = run["data"]["metrics"]
            metric_names.update(metrics.keys())

        return list(metric_names)
    # end of 'list_metrics' function

    def list_experiments(self) -> List[str]:
        return [experiment.name
                for experiment in MlflowClient(self.__get_uri()).list_experiments()]
    # end of 'list_experiments' function

