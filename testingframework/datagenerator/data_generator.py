from typing import List, Union

import numpy as np
import nibabel as nib
from nibabel.filebasedimages import ImageFileError
import logging
from keras.utils import Sequence
import random

from testingframework.datagenerator.units.unit import Unit
from testingframework.datagenerator.units.batcher_unit import BatcherUnit
from testingframework.datagenerator.units.preprocessor_unit import PreprocessorUnit


class DataGenerator(Sequence):
    batches = []

    def __init__(self, units: List[Unit], file_names: Union[str, List[str]],
                 files_path: str = "", batch_size: int = 3, shuffle: bool = True):
        # insert preprocessor and batcher units
        units.insert(0, PreprocessorUnit())
        units.append(BatcherUnit(batch_size, self.batches))

        # assign next_unit
        for i in range(len(units) - 1):
            units[i].next_unit = units[i + 1]

        # concatenate to files path to file names
        if files_path != "":
            if isinstance(file_names, list):
                for i, name in enumerate(file_names):
                    file_names[i] = files_path + "/" + name
            else:
                file_names = files_path + "/" + file_names

        # process file names to generate batches
        if isinstance(file_names, list):
            units[0].process(file_names)
        else:
            units[0].process([file_names])

        # save additional configurations
        self.shuffle = shuffle
    # end of '__init__' function

    @staticmethod
    def __load_image(image_name: str) -> np.ndarray:
        return nib.load(image_name).get_fdata()
    # end of '_load_image' function

    def __len__(self) -> int:
        return len(self.batches)
    # end of '__len__' function

    def __getitem__(self, index) -> np.array:
        # load batch
        batch = []
        for image in self.batches[index]:
            try:
                # check if images are "stacked"
                if isinstance(image, list):
                    # load all images
                    stack = []
                    for name in image:
                        stack.append(self.__load_image(name))
                    batch.append(stack)

                # load single image
                batch.append(self.__load_image(image))
            except (FileNotFoundError, ImageFileError):
                logging.exception("Caught image load exception")

        return batch
    # end of '__getitem__' function

    def on_epoch_end(self):
        if self.shuffle:
            random.shuffle(self.batches)
    # end of 'on_epoch_end' function
# end of 'DataGenerator' class
