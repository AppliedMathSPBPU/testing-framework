import mlflow
import mlflow.entities

from testingframework.logger.logger import Logger
from testingframework.datagenerator.data_generator import DataGenerator


class MLflowLogger(Logger):
    __run: mlflow.entities.Run

    def set_project(self, project_name: str = "", storage_path: str = "./projects") -> None:
        """Set active project. Creates new project if doesn't exist.

        Args:
            project_name (str): Project name.
            storage_path (str_: Logged data storage path.
        """
        if project_name == "":
            project_name = "Default"

        # set correct tracking uri
        mlflow.set_tracking_uri(storage_path + "/" + project_name)

        self._project_name = project_name
    # end of 'set_project' function

    def set_experiment(self, experiment_name: str = "") -> None:
        """Set active experiment. Creates new experiment if doesn't exist.

        Args:
            experiment_name (str): Experiment name.

        Raises:
            mlflow.exceptions.MLflowException: If try to set deleted experiment.
        """
        if experiment_name == "":
            experiment_name = "default"
            
        mlflow.set_experiment(experiment_name)
        self._experiment_name = experiment_name
    # end of 'set_experiment' function

    def start_run(self, experiment_name: str = "", project_name: str = "") -> None:
        """Start run in the current experiment."""
        self.__run = mlflow.start_run()
    # end of 'start_run' function

    def end_run(self) -> None:
        """End current active run."""
        mlflow.end_run()
    # end of 'end_run' function

    def log_parameter(self, parameter_name: str, value: float) -> None:
        """Log parameter to the current run.

        Args:
            parameter_name (str): Logged parameter name.
            value (float): Logged parameter value.
        """
        mlflow.log_param(parameter_name, value)
    # end of 'log_parameter' function

    def log_input_data(self, data_generator: DataGenerator) -> None:
        """Log input data used in run.

        Args:
            data_generator (DataGenerator): Data generator to extract input data from.
        """
        # TODO
        pass
    # end of 'log_input_data' function

    def log_metric(self, metric_name: str, value: float) -> None:
        """Log metric to the current run.

        Args:
            metric_name (str): Logged metric name.
            value (float): Logged metric value.
        """
        mlflow.log_metric(metric_name, value)
    # end of 'log_metric' function

    def log_artifact(self, file_path: str, save_path: str = "") -> None:
        """Log artifact to the current run.

        Args:
            file_path (str): Local path to logged artifact file.
            save_path (float): Save path within the run artifact storage.
        """
        mlflow.log_artifact(file_path, save_path)
    # end of 'log_artifact' function
# end of 'MLflowLogger' class
