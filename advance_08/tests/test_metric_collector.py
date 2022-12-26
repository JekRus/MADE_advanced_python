import math
from time import perf_counter, sleep
from typing import Any, Tuple, Union
from unittest.mock import Mock
import pytest

from metric_collector import MetricTimer, MetricAvg, MetricCount, Stats


@pytest.mark.parametrize("metric_name", ["some_name", "another_name", "foobar"])
def test_metric_get_name(metric_name):
    metric_count = MetricCount(metric_name)
    assert metric_count.get_name() == f"{metric_name}.count"
    metric_avg = MetricAvg(metric_name)
    assert metric_avg.get_name() == f"{metric_name}.avg"
    metric_timer = MetricTimer(metric_name)
    assert metric_timer.get_name() == f"{metric_name}.timer"


@pytest.mark.parametrize("metric_name", [10, -12.3, [1, 2, 3], set()])
def test_metric_get_name_wrong_type(metric_name: Any):
    with pytest.raises(TypeError):
        MetricCount(metric_name)
    with pytest.raises(TypeError):
        MetricAvg(metric_name)
    with pytest.raises(TypeError):
        MetricTimer(metric_name)


def test_count_workflow():
    metric_name = "some_name"
    metric_count = MetricCount(metric_name)
    assert metric_count.get_value() is None

    metric_count.add()
    assert metric_count.get_value() == 1
    metric_count.add()
    assert metric_count.get_value() == 2
    metric_count.clear()
    assert metric_count.get_value() is None

    # idempotency
    metric_count.clear()
    metric_count.clear()
    assert metric_count.get_value() is None

    # big number
    val = 10_000
    for _ in range(val):
        metric_count.add()
    assert metric_count.get_value() == val

    with pytest.raises(TypeError):
        metric_count.add(12)


def test_avg_workflow():
    metric_name = "some_name"
    metric_avg = MetricAvg(metric_name)
    assert metric_avg.get_value() is None

    metric_avg.add(4)
    assert math.isclose(metric_avg.get_value(), 4.0)
    metric_avg.add(3)
    assert math.isclose(metric_avg.get_value(), 3.5)
    metric_avg.clear()
    assert metric_avg.get_value() is None

    # idempotency
    metric_avg.clear()
    metric_avg.clear()
    assert metric_avg.get_value() is None
    assert metric_avg._sum == 0.0
    assert metric_avg._count == 0


@pytest.mark.parametrize("param", ["some_string", [1, 2, 3], set(), dict(), None])
def test_avg_add_wrong_type(param: Any):
    metric_avg = MetricAvg("some_name")
    with pytest.raises(TypeError):
        metric_avg.add(param)


@pytest.mark.parametrize(
    "elems,result",
    [
        ((1, 2, 3, 4, 5), 3.0),
        ((0,), 0),
        ((0, 0, 0, 0), 0.0),
        ((1, 1, 1, 1, 1), 1.0),
        ((22, -235, 12, 12, 4353.5), 832.9),
    ],
)
def test_avg_calculation(elems: Tuple[Union[float, int]], result: float):
    metric_avg = MetricAvg("some_name")
    for elem in elems:
        metric_avg.add(elem)
    assert math.isclose(metric_avg.get_value(), result)


def test_timer_workflow():
    metric_timer = MetricTimer("some_name")
    assert metric_timer.get_value() is None
    t1 = 0.02
    metric_timer.add(t1)
    assert metric_timer.get_value() == t1
    t2 = 0.23
    metric_timer.add(t2)
    assert math.isclose(metric_timer.get_value(), t1 + t2)

    # context manager check could be unstable
    # because of sleep
    sleep_time = 0.7
    with metric_timer:
        t_start = perf_counter()
        sleep(sleep_time)
        t_end = perf_counter()
    t_res = t_end - t_start

    assert math.isclose(metric_timer.get_value(), t1 + t2 + t_res, abs_tol=1e-1)

    metric_timer.clear()
    assert metric_timer.get_value() is None

    # idempotency
    metric_timer.clear()
    metric_timer.clear()
    assert metric_timer.get_value() is None
    t4 = 22.222
    metric_timer.add(t4)
    assert metric_timer.get_value() == t4

    # negative argument
    with pytest.raises(ValueError):
        metric_timer.add(-42.2)


def test_stats():
    metrics = Stats.collect()
    assert metrics == {}

    sleep_time = 0.3
    calc = Mock()
    calc.side_effect = [3, 4]
    with Stats.timer("calc"):
        res = calc()
        sleep(sleep_time)

    Stats.count("calc").add()
    Stats.avg("calc").add(res)

    t1 = perf_counter()
    res = calc()
    sleep(0.1)
    t2 = perf_counter()
    Stats.timer("calc").add(t2 - t1)
    Stats.count("calc").add()
    Stats.avg("calc").add(res)

    Stats.count("http_get_data").add()
    Stats.avg("http_get_data").add(0.7)

    Stats.count("no_used")

    metrics = Stats.collect()

    check = {
        "calc.count": 2,
        "calc.avg": 3.5,
        "calc.timer": 0.4,
        "http_get_data.count": 1,
        "http_get_data.avg": 0.7,
    }

    assert check.keys() == metrics.keys()

    for key, check_val in check.items():
        if isinstance(check_val, float):
            assert math.isclose(check_val, metrics[key], abs_tol=1e-1)
        else:
            assert check_val == metrics[key]

    metrics = Stats.collect()
    assert metrics == {}

    # idempotency
    metrics = Stats.collect()
    assert metrics == {}
