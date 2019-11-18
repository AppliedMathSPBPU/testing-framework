from typing import List, Dict, Union, Tuple
from testingframework.metrics.metric import Metric, DataType


def calculate_metrics(metrics_data: List[Tuple[Metric, DataType]]) -> List[float]:
    """Calculate metrics in parallel.

    Args:
        metrics_data (List[Tuple[Metric, DataType]]): Metric and respective data pair list.

    Returns:
        (List[float]): List of calculated metrics (i-th value for i-th metric).
    """
    out_list = List()

    for pair in metrics_data:
        metric = pair[0]
        data = pair[1]
        out_list.append(metric.calculate(data))
    
    return out_list