from typing import List, Dict, Union, Tuple
from testingframework.metrics.metric import Metric, DataType


def calculate_metrics(metrics_data: List[Tuple[Metric, DataType]]) -> List[float]:
    """Calculate metrics in parallel.

    Args:
        metrics_data (List[Tuple[Metric, DataType]]): Metric and respective data pair list.

    Returns:
        (List[float]): List of calculated metrics (i-th value for i-th metric).
    """
    pass
