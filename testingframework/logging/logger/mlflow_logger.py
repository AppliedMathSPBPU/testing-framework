import mlflow
import mlflow.entities

from testingframework.logging.logger.logger import Logger, MetricValueType
from testingframework.datagenerator.data_generator import DataGenerator
from testingframework.logging.session import Session


class MLflowLogger(Logger):
    def __init__(self, session: Session = Session()) -> None:
        super().__init__(session)

        self.__run: mlflow.entities.Run = None
    # end of '__init__' function

    def __set_uri(self):
        mlflow.set_tracking_uri(self._session.storage_path + "/" +
                                self._session.project_name)
    # end of '__set_uri' function

    def set_project(self, project_name: str = "") -> None:
        """Set active project. Creates new project if doesn't exist.

        Args:
            project_name (str): Project name.
        """
        self._session.project_name = project_name
        self.__set_uri()

        self.set_experiment()
    # end of 'set_project' function

    def set_experiment(self, experiment_name: str = "") -> None:
        """Set active experiment. Creates new experiment if doesn't exist.

        Args:
            experiment_name (str): Experiment name.

        Raises:
            mlflow.exceptions.MLflowException: If try to set deleted experiment.
        """
        self._session.experiment_name = experiment_name
        mlflow.set_experiment(self._session.experiment_name)
    # end of 'set_experiment' function

    def set_storage_path(self, storage_path: str = "") -> None:
        """Set logged data local storage path. Default: './projects'

        Args:
            storage_path (str): Local storage path.
        """
        self._session.storage_path = storage_path
        self.__set_uri()
    # end of 'set_storage_path' function

    def start_run(self, experiment_name: str = "", project_name: str = "") -> None:
        """Start run in the current experiment."""
        if not self._is_running:
            self.__run = mlflow.start_run()
            self._is_running = True
    # end of 'start_run' function

    def end_run(self) -> None:
        """End current active run."""
        if self._is_running:
            mlflow.end_run()
            self._is_running = False
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
        with open("input_data.txt", "w+") as file:
            file.write("raw file names:\n")
            file.write(str(data_generator.get_raw_file_names()))
            file.write("\n\nbatches names:\n")
            file.write(str(data_generator.get_batches()))

        self.log_artifact("input_data.txt")
    # end of 'log_input_data' function

    def log_metric(self, metric_name: str, value: MetricValueType) -> None:
        """Log metric to the current run.

        Args:
            metric_name (str): Logged metric name.
            value (MetricValueType): Logged metric value.
        """
        if isinstance(value, list):
            for single_value in value:
                mlflow.log_metric(metric_name, single_value)
            return

        if isinstance(value, tuple):
            for single_value in value:
                mlflow.log_metric(metric_name, single_value)
            return

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
