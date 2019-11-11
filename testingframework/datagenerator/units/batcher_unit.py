from typing import List, Union

from testingframework.datagenerator.units.unit import Unit, FileNameType

BatchType = List[FileNameType]
PreBatchType = List[FileNameType]


class BatcherUnit(Unit):
    def __init__(self, batch_size: int, output_batch_list: List[BatchType],
                 output_prebatch_list: List[PreBatchType]):
        self._batch_size = batch_size
        self._output_batch_list = output_batch_list
        self._output_prebatch_list = output_prebatch_list
    # end of '__init__' function

    def process(self, file_names: List[FileNameType]) -> None:
        """Separate file names into batches of 'batch_size' length and
        append those batches to 'output_list'.

        Args:
            file_names (list): Input list of strings or lists of strings.
        """
        # save entire pre-batched chunk of files
        self._output_prebatch_list.append(file_names)

        # batch files
        batch = []
        for name in file_names:
            batch.append(name)
            if len(batch) == self._batch_size:
                self._output_batch_list.append(batch)
                batch = []
        if len(batch) != 0:
            self._output_batch_list.append(batch)
    # end of 'process' function
# end of 'BatcherUnit' class
