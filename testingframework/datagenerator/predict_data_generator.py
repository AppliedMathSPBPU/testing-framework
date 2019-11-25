from typing import List, Union

import numpy as np
import nibabel as nib
from nibabel.filebasedimages import ImageFileError
import logging
import random

from testingframework.datagenerator.data_generator import DataGenerator
from testingframework.datagenerator.units.unit import Unit, FileNameType
from testingframework.datagenerator.units.batcher_unit import BatcherUnit, BatchType, PreBatchType
from testingframework.datagenerator.units.preprocessor_unit import PreprocessorUnit


class PredictDataGenerator(DataGenerator):
    def __init__(self, units: List[Unit], file_names: Union[str, List[str]],
                 files_path: str = "", batch_size: int = 3, shuffle: bool = True) -> None:
        self._batches: List[BatchType] = []
        self._prebatched: List[PreBatchType] = []
        self._raw_file_names: List[str] = []

        # insert preprocessor and batcher units
        self._units = list(units)
        self._units.insert(0, PreprocessorUnit(self._raw_file_names))
        self._units.append(BatcherUnit(batch_size=batch_size,
                                       output_batch_list=self._batches,
                                       output_prebatch_list=self._prebatched))

        # assign next_unit
        for i in range(len(self._units) - 1):
            self._units[i].next_unit = self._units[i + 1]

        # concatenate to files path to file names
        if files_path != "":
            if isinstance(file_names, list):
                for i, name in enumerate(file_names):
                    file_names[i] = files_path + "/" + name
            else:
                file_names = files_path + "/" + file_names

        # process file names to generate batches
        if isinstance(file_names, list):
            self._units[0].process(file_names)
        else:
            self._units[0].process([file_names])

        # save additional configurations
        self.shuffle = shuffle
    # end of '__init__' function

    @staticmethod
    def __load_image(image_name: str) -> np.ndarray:
        return nib.load(image_name).get_fdata()
    # end of '_load_image' function

    def __len__(self) -> int:
        return len(self._batches)
    # end of '__len__' function

    def __getitem__(self, index) -> np.array:
        # load batch
        batch = []
        for image in self._batches[index]:
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

    def on_epoch_end(self) -> None:
        if self.shuffle:
            self._shuffle()
    # end of 'on_epoch_end' function

    def get_batches(self) -> List[FileNameType]:
        return list(self._batches)
    # end of 'get_batches' function

    def _shuffle(self, shuffled_indices: List[int] = None) -> None:
        if shuffled_indices is None:
            # remove old batches
            self._batches.clear()

            # shuffle pre-batches and create new batches
            for prebatch in self._prebatched:
                random.shuffle(prebatch)
                self._units[-1].process(prebatch)
            return

        # TODO: figure out shuffling with indices
    # end of '_shuffle' function

    def get_raw_file_names(self) -> List[str]:
        return list(self._raw_file_names)
    # end of 'get_raw_file_names' function
# end of 'PredictDataGenerator' class
