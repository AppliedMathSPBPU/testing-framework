from abc import ABC, abstractmethod


class Unit(ABC):
    next_unit: 'Unit' = None

    @abstractmethod
    def process(self, file_names: list):
        """Process 'file_names' and pass them forward via 'next_unit.process'.

        Args:
            file_names (list): Input list of strings or lists of strings.
        """
        self.next_unit.process(file_names)
    # end of 'process' function
# end of 'Unit' class
