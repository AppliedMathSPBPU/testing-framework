from typing import Tuple, List, Union

import numpy as np
import logging

from testingframework.datagenerator.data_generator import PredictDataGenerator
from testingframework.datagenerator.units.unit import FileNameType


class FitDataGenerator(DataGenerator):
    def __init__(self, input_generator: DataGenerator, target_generator: DataGenerator,
                 shuffle: bool = True) -> None:
        self._input_generator = input_generator
        self._target_generator = target_generator
        self.shuffle = shuffle

        if len(input_generator) != len(target_generator):
            # TODO: custom exception here
            raise Exception("Different target and input generator length!"
                            " len(input_generator) = " + str(len(input_generator)) +
                            " and len(target_generator) = " + str(len(target_generator)))
    # end of '__init__' function

    def __getitem__(self, index) -> Tuple[np.array, np.array]:
        inputs: np.array = self._input_generator[index]
        targets: np.array = self._target_generator[index]

        if len(inputs) != len(targets):
            logging.error("Different target and input batch length! Index = " + str(index))
            return np.zeros(0), np.zeros(0)

        return inputs, targets
    # end of '__getitem__' function

    def __len__(self) -> int:
        return len(self._input_generator)
    # end of '__len__' function

    def on_epoch_end(self) -> None:
        if self.shuffle:
            self._shuffle()
    # end of 'on_epoch_end' function

    def get_batches(self) -> Tuple[List[FileNameType], List[FileNameType]]:
        return self._input_generator.get_batches(), \
               self._target_generator.get_batches()
    # end of 'get_batches' function

    def _shuffle(self, shuffled_indices: List[int] = None) -> None:
        # TODO: once you figured out shuffling, figure this out as well. thanks!
        # # generate shuffled indices
        # indices: List[int] = list(range(len(self._input_generator)))
        # random.shuffle(indices)

        # #  shuffle input and target generators
        # self._input_generator._shuffle(shuffled_indices=indices)
        # self._target_generator._shuffle(shuffled_indices=indices)
        pass
    # end of '_shuffle' function

    def get_raw_file_names(self) -> Tuple[List[str], ...]:
        return self._input_generator.get_raw_file_names(), \
               self._target_generator.get_raw_file_names()
    # end of 'get_raw_file_names' function
# end of 'FitDataGenerator' class
