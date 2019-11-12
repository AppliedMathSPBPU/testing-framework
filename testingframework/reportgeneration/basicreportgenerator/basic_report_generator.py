import math

from matplotlib import pyplot as plt
import pathlib as pth
import time
import base64

from testingframework.logging.datacollector.data_collector import DataCollector
from testingframework.logging.datacollector.mlflow_data_collector import MLflowDataCollector
from testingframework.logging.session import Session


class BasicReportGenerator:
    def __init__(self):
        self.__save_path: str = ""

    def __get_boxplot_filename(self, title=""):
        filename = "boxplot_" + title + "_" + str(time.time())

        return filename + ".png"
    # end of 'get_boxplot_filename' function

    def __save_boxplots(self, data, save_path, title) -> str:
        filtered_data = [x for x in data if not math.isnan(x)]

        plt.boxplot(filtered_data)
        plt.title(title)
        plt.xticks(rotation=-45)
        plt.tight_layout()

        file_name = self.__get_boxplot_filename(title=title)
        plt.savefig(str(save_path / file_name))
        plt.close()

        return file_name
    # end of 'save_boxplots' function

    def __save_full_report(self, boxplot_names, save_path):
        html_text = "<html><body>"

        # insert boxplots
        for name in boxplot_names:
            image_path = pth.Path(self.__save_path, "boxplots", boxplot_names[name]).absolute()
            with open(image_path, "rb") as imageFile:
                image64 = base64.b64encode(imageFile.read()).decode("utf-8")
                html_text += '<img src="data:image/png;base64,' + image64 + '" /><br><br>'
        html_text += "</body></html>"

        file_name = str(save_path / ("full_report_" + str(time.time()) + ".html"))
        file = open(file_name, "w")
        file.write(html_text)
        file.close()

        print("saved full report to " + file_name)
    # end of 'save_full_report' function

    def generate_report(self, session: Session, save_path: str = "./reports/") -> None:
        self.__save_path = save_path
        data_collector: DataCollector = MLflowDataCollector(session)
        if not pth.Path(save_path).exists():
            pth.Path(save_path).mkdir()

        # extract runs
        runs = data_collector.get_runs()

        # extract metrics list
        metric_name_list = data_collector.list_metrics(runs)

        # generate boxplots
        def get_report_path(report_name):
            report_path = pth.Path(self.__save_path, report_name)
            # create report output directory if doesn't exist yet
            if not report_path.exists():
                report_path.mkdir()
            return report_path
        # end of 'get_path' function

        boxplots_path = get_report_path("boxplots")
        full_report_path = get_report_path("full_report")

        # render report
        print("export box plots")
        boxplot_filenames = {}
        data_boxplot = dict()
        for metric_name in metric_name_list:
            data_boxplot[metric_name] = data_collector.get_metric_values(metric_name, runs)
            filename = self.__save_boxplots(data=data_boxplot[metric_name],
                                            title=metric_name, save_path=boxplots_path)
            boxplot_filenames[metric_name] = filename

        # export full report
        print("export full report")
        self.__save_full_report(save_path=full_report_path,
                                boxplot_names=boxplot_filenames)
