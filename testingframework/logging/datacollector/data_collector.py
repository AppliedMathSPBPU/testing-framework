from typing import List

from abc import ABC, abstractmethod

from testingframework.logging.session import Session

from pandas import DataFrame


class DataCollector(ABC):
    def __init__(self, session: Session = Session()) -> None:
        super().__init__()

        self._session: Session = Session(session.experiment_name, session.project_name,
                                         session.storage_path)

        self.set_storage_path(session.storage_path)
        self.set_project(session.project_name)
        self.set_experiment(session.experiment_name)
    # end of '__init__' function

    @abstractmethod
    def set_project(self, project_name: str = "") -> None:
        """Set active project. Sets 'Default' if doesn't exist.

        Args:
            project_name (str): Project name.
        """
        pass

    @abstractmethod
    def set_experiment(self, experiment_name: str = "") -> None:
        """Set active experiment. Sets 'Default' if doesn't exist.

        Args:
            experiment_name (str): Experiment name.
        """
        pass

    @abstractmethod
    def set_storage_path(self, storage_path: str = "") -> None:
        """Set logged data local storage path. Default: './projects'

        Args:
            storage_path (str): Local storage path.
        """
        pass

    @abstractmethod
    def get_runs(self, search_query: str = "") -> DataFrame:
        pass

    @abstractmethod
    def get_parameter_values(self, parameter_name: str, runs: DataFrame) -> List[str]:
        pass

    @abstractmethod
    def get_metric_values(self, metric_name: str, runs: DataFrame) -> List[float]:
        pass

    @abstractmethod
    def get_artifacts(self, artifact_name: str, runs: DataFrame, artifact_path: str = "") -> List[str]:
        pass
    
    @abstractmethod
    def list_metrics(self, runs: DataFrame) -> List[str]:
        pass

    @abstractmethod
    def list_experiments(self) -> List[str]:
        pass

    @abstractmethod
    def list_projects(self) -> List[str]:
        pass
# end of 'DataCollector' class
