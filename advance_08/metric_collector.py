from abc import ABC, abstractmethod
from time import perf_counter
from types import TracebackType
from typing import Type, Optional, Union, Any, Dict, ClassVar
from typing_extensions import Literal


class BaseMetric(ABC):
    _metric_type: ClassVar[str] = "base_metric"

    def __init__(self, name: str):
        if not isinstance(name, str):
            raise TypeError(
                f'Parameter "name" must have type str, '
                f'got {type(name)} instead.'
            )
        self._name: str = name
        self._value: Any = None

    def get_name(self) -> str:
        return f"{self._name}.{self._metric_type}"

    def get_value(self) -> Any:
        return self._value

    @abstractmethod
    def add(self, *args, **kwargs):
        ...

    def clear(self):
        self._value = None


class MetricTimer(BaseMetric):
    _metric_type: ClassVar[str] = "timer"

    def __init__(self, name: str):
        super().__init__(name)
        self._ctx_start: float = 0.0

    def add(self, value: float):
        if not isinstance(value, float):
            raise TypeError(
                f'Parameter "value" must have type float, '
                f'got {type(value)} instead.'
            )
        if value < 0.0:
            raise ValueError('Parameter "value" must be non-negative.')
        if self._value is not None:
            self._value += value
        else:
            self._value = value

    def __enter__(self):
        self._ctx_start = perf_counter()

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> Literal[False]:
        end = perf_counter()
        self.add(end - self._ctx_start)
        return False


class MetricAvg(BaseMetric):
    _metric_type: ClassVar[str] = "avg"

    def __init__(self, name: str):
        super().__init__(name)
        self._sum: float = 0.0
        self._count: int = 0

    def add(self, value: Union[int, float]):
        if not isinstance(value, (int, float)):
            raise TypeError(
                f'Parameter "value" must have type int or float, '
                f'got {type(value)} instead.'
            )
        self._sum += value
        self._count += 1
        self._value = self._sum / self._count

    def clear(self):
        super().clear()
        self._sum = 0.0
        self._count = 0


class MetricCount(BaseMetric):
    _metric_type: ClassVar[str] = "count"

    def add(self):
        if self._value is not None:
            self._value += 1
        else:
            self._value = 1


class Stats:
    metrics: ClassVar[Dict[str, BaseMetric]] = {}

    @classmethod
    def timer(cls, name: str) -> BaseMetric:
        metric_obj = MetricTimer(name)
        full_name = cls._register_metric(metric_obj)
        return cls.metrics[full_name]

    @classmethod
    def avg(cls, name: str) -> BaseMetric:
        metric_obj = MetricAvg(name)
        full_name = cls._register_metric(metric_obj)
        return cls.metrics[full_name]

    @classmethod
    def count(cls, name: str) -> BaseMetric:
        metric_obj = MetricCount(name)
        full_name = cls._register_metric(metric_obj)
        return cls.metrics[full_name]

    @classmethod
    def collect(cls) -> Dict[str, Union[int, float]]:
        collected_metrics = {}
        for metric_name, metric_obj in cls.metrics.items():
            metric_val = metric_obj.get_value()
            if metric_val is not None:
                collected_metrics[metric_name] = metric_val
            cls.metrics[metric_name].clear()
        return collected_metrics

    @classmethod
    def _register_metric(
        cls, metric_obj: Union[MetricTimer, MetricAvg, MetricCount]
    ) -> str:
        full_name = metric_obj.get_name()
        if full_name not in cls.metrics:
            cls.metrics[full_name] = metric_obj
        return full_name
