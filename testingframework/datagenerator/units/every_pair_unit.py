from typing import List
from itertools import combinations

from testingframework.datagenerator.units.unit import Unit, FileNameType


class EveryPairUnit(Unit):
    def process(self, file_names: List[FileNameType]) -> None:
        """Stack images into pairs and pass forward.
        Args:
            file_names (list): Input list of strings or lists of strings.
        """
        output = []

        for ind in combinations(range(len(file_names)), 2):
            output.append([file_names[ind[0]], file_names[ind[1]]])
            output.append([file_names[ind[1]], file_names[ind[0]]])

        self.next_unit.process(output)
    # end of 'process' function
# end of 'EveryPairUnit' class
