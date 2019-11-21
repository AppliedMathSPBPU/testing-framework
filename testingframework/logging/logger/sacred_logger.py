from testingframework.logging.logger.logger import Logger


class SacredLogger(Logger):
    def start_run(self):
        pass

    def end_run(self):
        pass

    def log_parameter(self, parameter_name: str, value: float):
        pass

    def log_input_data(self, file_names: list):
        pass

    def log_metric(self, metric_name: str, value: float):
        pass

    def log_artifact(self, artifact_name: str, file_name: str):
        pass
