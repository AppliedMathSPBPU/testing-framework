from typing import List, Union

from testingframework.datagenerator.units.unit import Unit, FileNameType

BatchType = List[FileNameType]


class BatcherUnit(Unit):
    def __init__(self, batch_size: int, output_list: List[BatchType]):
        self.batch_size = batch_size
        self.output_list = output_list
    # end of '__init__' function

    def process(self, file_names: List[FileNameType]) -> None:
        """Separate file names into batches of 'batch_size' length and
        append those batches to 'output_list'.

        Args:
            file_names (list): Input list of strings or lists of strings.
        """
        batch = []
        for name in file_names:
            batch.append(name)
            if len(batch) == self.batch_size:
                self.output_list.append(batch)
                batch = []
        if len(batch) != 0:
            self.output_list.append(batch)
    # end of 'process' function
# end of 'BatcherUnit' class
