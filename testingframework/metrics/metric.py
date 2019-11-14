from abc import ABC, abstractmethod
from typing import Union, List
from sklearn.metrics import f1_score
from sklearn.metrics import mutual_info_score
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from statistics import mean
import numpy as np

DataType = Union[np.ndarray, List[np.ndarray]]


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

class NegativeJacobianDet(Metric):
    def name(self) -> str:
        return "Negative Jacobian Det"

    def jacobian_det(self, displacements):
        # Source: https://github.com/dykuang/Medical-image-registration/blob/master/source/losses.py
        dvf = np.expand_dims(displacements, 0)
        D_y = (dvf[:, 1:, :-1, :-1, :] - dvf[:, :-1, :-1, :-1, :])
        D_x = (dvf[:, :-1, 1:, :-1, :] - dvf[:, :-1, :-1, :-1, :])
        D_z = (dvf[:, :-1, :-1, 1:, :] - dvf[:, :-1, :-1, :-1, :])

        D1 = (D_x[..., 0] + 1) * ( (D_y[..., 1] + 1) * (D_z[..., 2] + 1) - D_z[..., 1] * D_y[..., 2])
        D2 = (D_x[..., 1]) * (D_y[..., 0] * (D_z[..., 2] + 1) - D_y[..., 2] * D_x[..., 0])
        D3 = (D_x[..., 2]) * (D_y[..., 0] * D_z[..., 1] - (D_y[..., 1] + 1) * D_z[..., 0])

        return D1 - D2 + D3  

    def calculate(self, data: DataType) -> float:
        return (self.jacobian_det(data) <= 0).sum()  

    
class NormalizedCrossCorrelation(Metric):
    def name(self) -> str:
        return "Normalized Cross Correlation"

    def calculate(self, data: DataType) -> float:
        #reshape to vector
        y_true = data[0].ravel()
        y_pred = data[1].ravel()
        #normalize
        y_true = (y_true - np.mean(y_true)) / np.std(y_true)
        y_pred = (y_pred - np.mean(y_pred)) / np.std(y_pred)

        return np.correlate(y_true, y_pred)/len(y_true)


class  MeanDice(Metric):
    def name(self) -> str:
        return "Mean Dice"

    def calculate(self, data: DataType) -> float:
        fixed_segm = data[0].flatten()
        moved_segm = data[1].flatten()
        array = f1_score(fixed_segm,  moved_segm, average=None)
        dice_pair_segments = [dice for dice in array]
        dice_pair_mean = mean(dice_pair_segments)
        return dice_pair_mean


class MeanSquaredError(Metric):
    def name(self) -> str:
        return "Mean Squared Error"

    def calculate(self, data: DataType) -> float:
        fixed = data[0]
        moved = data[1]
        mse_pair = mean_squared_error(fixed.flatten(), moved.flatten())
        return mse_pair

class MeanAbsoluteError(Metric):
    def name(self) -> str:
        return "Mean Absolute Error" 

    def calculate(self, data: DataType) -> float:
        fixed = data[0]
        moved = data[1]
        mae_pair = mean_absolute_error(fixed.flatten(), moved.flatten())
        return mae_pair       