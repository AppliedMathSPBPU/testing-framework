from abc import ABC, abstractmethod

from testingframework.datagenerator.data_generator import DataGenerator


class Logger(ABC):
    _experiment_name: str
    _project_name: str

    def __init__(self, experiment_name: str = "", project_name: str = "") -> None:
        super().__init__()
        self.set_project(project_name)
        self.set_experiment(experiment_name)

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
