from typing import List, Union
import pathlib as pth

from testingframework.datagenerator.units.unit import Unit, FileNameType


class PreprocessorUnit(Unit):
    def process(self, file_names: List[FileNameType]) -> None:
        """Unravel directory names into contained file names. Sort file names.

        Args:
            file_names (list): Input list of strings or lists of strings.
        """
        # unravel directories
        for name in list(file_names):
            path = pth.Path(name)

            # check path exists
            if not path.exists():
                file_names.remove(name)
                continue

            # check if directory
            if path.is_dir():
                # remove directory from 'file_names'
                file_names.remove(name)

                # find contained files with unique name stems
                file_stems = []
                for child in path.iterdir():
                    if not child.is_file():
                        continue
                    # add to file_names if unique name stem
                    if child.stem not in file_stems:
                        file_stems.append(child.stem)
                        file_names.append(str(child))

        # sort 'file_names'
        file_names.sort()

        self.next_unit.process(file_names)
    # end of 'process' function
# end of 'PreprocessorUnit' class
