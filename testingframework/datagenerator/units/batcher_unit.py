from typing import List, Union

from testingframework.datagenerator.units.unit import Unit


class BatcherUnit(Unit):
    def __init__(self, batch_size: int, output_list: list):
        self.batch_size = batch_size
        self.output_list = output_list
    # end of '__init__' function

    def process(self, file_names: List[Union[str, List[str]]]) -> None:
        """Separate file names into batches of 'batch_size' length and
        append those batches to 'output_list'.

        Args:
            file_names (list): Input list of strings or lists of strings.
        """
        pass
