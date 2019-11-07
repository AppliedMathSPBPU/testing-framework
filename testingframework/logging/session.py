class Session:
    @staticmethod
    def __check_empty(string: str, default: str = "Default") -> str:
        if string is None or string == "":
            return default
        return string
    # end of '__check_empty' function

    def __init__(self, experiment_name: str = "", project_name: str = "",
                 storage_path: str = "") -> None:
        self.project_name = project_name
        self.experiment_name = experiment_name
        self.storage_path = storage_path
    # end of '__init__' function

    @property
    def project_name(self):
        return self.__project_name
    # end of 'project_name.getter' function

    @project_name.setter
    def project_name(self, name: str):
        self.__project_name = Session.__check_empty(name)
    # end of 'project_name.setter' function

    @property
    def experiment_name(self):
        return self.__experiment_name
    # end of 'experiment_name.getter' function

    @experiment_name.setter
    def experiment_name(self, name: str):
        self.__experiment_name = Session.__check_empty(name)
    # end of 'experiment_name.setter' function

    @property
    def storage_path(self):
        return self.__storage_path
    # end of 'storage_path.getter' function

    @storage_path.setter
    def storage_path(self, name: str):
        self.__storage_path = Session.__check_empty(name, "./projects")
    # end of 'storage_path.setter' function
# end of 'Session' class
