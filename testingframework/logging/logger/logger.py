from abc import ABC, abstractmethod

from testingframework.datagenerator.data_generator import DataGenerator
from testingframework.logging.session import Session


class Logger(ABC):
    def __init__(self, session: Session = Session()) -> None:
        super().__init__()

        self._session: Session = Session(session.experiment_name, session.project_name,
                                         session.storage_path)
        
        self.set_storage_path(session.storage_path)
        self.set_project(session.project_name)
        self.set_experiment(session.experiment_name)

        self._is_running: bool = False
    # end of '__init__' function

    def __enter__(self) -> 'Logger':
        self.start_run()
        return self
    # end of '__enter__' function

    def __exit__(self, exc_type, exc_val, exc_tb):
        # TODO: various exception handling
        self.end_run()
    # end of '__exit__' function

    @abstractmethod
    def set_project(self, project_name: str = "") -> None:
        """Set active project. Creates new project if doesn't exist.

        Args:
            project_name (str): Project name.
        """
        pass

    @abstractmethod
    def set_experiment(self, experiment_name: str = "") -> None:
        """Set active experiment. Creates new experiment if doesn't exist.

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
    def start_run(self) -> None:
        """Start run in the current experiment."""
        pass

    @abstractmethod
    def end_run(self) -> None:
        """End current active run."""
        pass

    @abstractmethod
    def log_parameter(self, parameter_name: str, value: float) -> None:
        """Log parameter to the current run.

        Args:
            parameter_name (str): Logged parameter name.
            value (float): Logged parameter value.
        """
        pass

    @abstractmethod
    def log_input_data(self, data_generator: DataGenerator) -> None:
        """Log input data used in run.

        Args:
            data_generator (DataGenerator): Data generator to extract input data from.
        """
        pass

    @abstractmethod
    def log_metric(self, metric_name: str, value: float) -> None:
        """Log metric to the current run.

        Args:
            metric_name (str): Logged metric name.
            value (float): Logged metric value.
        """
        pass

    @abstractmethod
    def log_artifact(self, file_path: str, save_path: str = "") -> None:
        """Log artifact to the current run.

        Args:
            file_path (str): Local path to logged artifact file.
            save_path (float): Save path within the run artifact storage.
        """
        pass
# end of 'Logger' class
