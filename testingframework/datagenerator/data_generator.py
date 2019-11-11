from abc import ABC, abstractmethod
from typing import List, Union, Tuple

from keras.utils import Sequence
from testingframework.datagenerator.units.unit import FileNameType


class DataGenerator(ABC, Sequence):
    @abstractmethod
    def get_batches(self) -> Union[List[FileNameType], Tuple[List[FileNameType], ...]]:
        """Get list of file name batches.
        Can be a tuple of lists, e.g. for FitDataGenerator.

        Returns:
            Union[List[str], Tuple[List[str], ...]]: List of file name batches.
        """
        pass

    @abstractmethod
    def _shuffle(self, shuffled_indices: List[int] = None) -> None:
        pass
# end of 'DataGenerator' class
