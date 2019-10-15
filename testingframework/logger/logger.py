from abc import ABC, abstractmethod


class Logger(ABC):
    @abstractmethod
    def start_run(self):
        pass

    @abstractmethod
    def end_run(self):
        pass

    @abstractmethod
    def log_parameter(self, parameter_name: str, value: float):
        pass

    @abstractmethod
    def log_input_data(self, file_names: list):
        pass

    @abstractmethod
    def log_metric(self, metric_name: str, value: float):
        pass

    @abstractmethod
    def log_artifact(self, artifact_name: str, file_name: str):
        pass
