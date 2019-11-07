from typing import List

from abc import ABC, abstractmethod

from testingframework.logging.session import Session


class DataCollector(ABC):
    def __init__(self, session: Session = Session()) -> None:
        super().__init__()

        self._session: Session = Session(session.experiment_name, session.project_name,
                                         session.storage_path)

        self.set_project(session.project_name)
        self.set_experiment(session.experiment_name)
        self.set_storage_path(session.storage_path)
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
    def get_runs(self, search_query: str) -> List[dict]:
        pass

    @abstractmethod
    def get_parameters(self, parameter_name: str, search_query: str) -> List[float]:
        pass

    @abstractmethod
    def get_metrics(self, metric_name: str, search_query: str) -> List[float]:
        pass

    @abstractmethod
    def get_artifacts(self, artifact_name: str, search_query: str) -> List[str]:
        pass


