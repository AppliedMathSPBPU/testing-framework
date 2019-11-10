from keras.utils import Sequence
import numpy as np
import logging

from testingframework.datagenerator.data_generator import DataGenerator


class FitDataGenerator(Sequence):
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

    def __getitem__(self, index):
        inputs: np.array = self._input_generator[index]
        targets: np.array = self._target_generator[index]

        if len(inputs) != len(targets):
            logging.error("Different target and input batch length! Index = " + str(index))
            return np.zeros(0), np.zeros(0)

        return inputs, targets
    # end of '__getitem__' function

    def __len__(self):
        return len(self._input_generator)
    # end of '__len__' function

    def on_epoch_end(self):
        super().on_epoch_end()
    # end of '__len__' function
# end of 'FitDataGenerator' class
