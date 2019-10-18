from abc import ABC, abstractmethod
from typing import Union, List
from numpy import ndarray

DataType = Union[ndarray, List[ndarray]]


class Metric(ABC):
    @abstractmethod
    def name(self) -> str:
        """Get metric name as a string.

        Returns:
            (str): Metric name.
        """
        pass

    @abstractmethod
    def calculate(self, data: DataType) -> float:
        """Calculate metric value.

        Args:
            data (Union[numpy.ndarray, List[numpy.ndarray]]): Image or set of images
                to calculate metric on.

        Returns:
            (float): Calculated metric value.
        """
        pass
