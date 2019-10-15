from typing import List

from testingframework.datagenerator.units.unit import Unit
from testingframework.datagenerator.units.batcher_unit import BatcherUnit
from testingframework.datagenerator.units.preprocessor_unit import PreprocessorUnit


class DataGenerator:
    batches = []
    index = 0

    def __init__(self, units: List[Unit], file_names: List[str], batch_size: int = 3):
        # insert preprocessor and batcher units
        units.insert(0, PreprocessorUnit())
        units.append(BatcherUnit(batch_size, self.batches))

        # assign next_unit
        for i in range(len(units) - 1):
            units[i].next_unit = units[i + 1]

        # generate batches
        units[0].process(file_names)
    # end of '__init__' function

    def __iter__(self):
        return self
    # end of '__iter__' function

    def __next__(self):
        if self.index == len(self.batches):
            raise StopIteration
        
        self.index = self.index + 1
        
        return self.batches[self.index]
    # end of '__next__' function
