from typing import List

from testingframework.datagenerator.units.unit import Unit, FileNameType


class CrossValidationUnit(Unit):
    def __init__(self, fold_size: int):
        self.fold_size = fold_size
    # end of '__init__' function

    def process(self, file_names: List[FileNameType]) -> None:
        """Separate file names into folds of 'fold_size' length and
        separately pass each fold forward.

        Args:
            file_names (list): Input list of strings or lists of strings.
        """
        fold = []
        for name in file_names:
            fold.append(name)
            if len(fold) == self.fold_size:
                self.next_unit.process(fold)
                fold = []
        if len(fold) != 0:
            self.next_unit.process(fold)
    # end of 'process' function
# end of 'CrossValidationUnit' class
