import pytest

from datetime import datetime

from nagiosplugin import Metric
from nagios_aws.exceptions import UnexpectedResponse


def test_probe_metrics_parsed_single(target):
    response = {
        "Label": "SingleTest",
        "Datapoints": [
            {
                "Timestamp": datetime(1970, 1, 1),
                "Average": 123,
                "Unit": "Count",
            },
        ],
    }

    t = target(dict(metric="SingleTest"), response)
    metrics = list(t.resource.probe())

    assert len(metrics) == 1
    assert metrics[0].name == "SingleTest"
    assert metrics[0].value == 123


def test_probe_metrics_parsed_multi(target):
    response = {
        "Label": "MultiTest",
        "Datapoints": [
            {
                "Timestamp": datetime(1970, 1, 1),
                "Average": 111,
                "Unit": "Count",
            },
            {
                "Timestamp": datetime(1975, 1, 1),
                "Average": 222,
                "Unit": "Bytes",
            },
        ],
    }

    t = target(dict(metric="MultiTest"), response)
    metrics = t.resource.probe()
    first = metrics.__next__()
    second = metrics.__next__()

    with pytest.raises(StopIteration):
        metrics.__next__()

    assert first.name == "MultiTest"
    assert first.value == 111
    assert second.name == "MultiTest"
    assert second.value == 222


def test_probe_valid_retval_type(target):
    response = {
        "Label": "Test",
        "Datapoints": [
            {
                "Timestamp": datetime(1980, 2, 2),
                "Average": 321,
                "Unit": "Count",
            },
        ],
    }

    t = target(dict(metric="Test"), response)
    res = t.resource.probe()

    assert isinstance(res.__next__(), Metric)


def test_probe_unexpected_response_metric(target):
    response = {
        "Label": "Test",
        "Datapoints": [
            {
                "Timestamp": datetime(1990, 3, 3),
                "Average": 555,
                "Unit": "Count",
            },
        ],
    }

    with pytest.raises(UnexpectedResponse):
        t = target(dict(metric="Uhh"), response)
        list(t.resource.probe())


def test_probe_empty_datapoints(target):
    response = {
        "Label": "Test",
        "Datapoints": [],
    }

    t = target(dict(metric="Test"), response)

    assert list(t.resource.probe()) == []


def test_probe_no_datapoints(target):
    response = {
        "Label": "Test",
    }

    t = target(dict(metric="Test"), response)

    assert list(t.resource.probe()) == []
