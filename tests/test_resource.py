import pytest

from check_aws.consts import NAME
from check_aws.exceptions import (
    InvalidDimension,
    InvalidMetricNamespace,
    InvalidMetricType,
)


def test_resource_session_type(resource):
    res = resource(dict(region="test"))

    assert hasattr(res.session.client("cloudwatch"), "get_metric_statistics")


def test_resource_name(resource):
    res = resource()

    assert res.name == NAME


def test_validation_invalid_metric_namespace(resource):
    metrics_available = [
        {"Metrics": []},  # First request
        {  # Second request
            "Metrics": [
                {
                    "Namespace": "AWS/EC2",
                    "MetricName": "CPUCreditUsage",
                    "Dimensions": [
                        {"Name": "InstanceId", "Value": "i-123454ec7eaad629c"}
                    ],
                },
            ]
        },
    ]
    res = resource(metrics_available=metrics_available)

    with pytest.raises(InvalidMetricNamespace):
        res._query_make(res.cmdargs)


def test_validation_invalid_type(resource):
    metrics_available = dict(Metrics=[])
    res = resource(metrics_available=metrics_available)

    with pytest.raises(InvalidMetricType):
        res._query_make(res.cmdargs)


def test_validation_invalid_dimensions(resource):
    metrics_available = [
        {
            "Metrics": [
                {
                    "Namespace": "AWS/EC2",
                    "MetricName": "CPUCreditUsage",
                    "Dimensions": [
                        {"Name": "InstanceId", "Value": "i-123454ec7eaad629c"}
                    ],
                },
            ]
        },
    ]
    res = resource(
        cmdargs={
            "metric": "CPUCreditUsage",
            "dimensions": [dict(Name="InstanceId", Value="invalid")],
        },
        metrics_available=metrics_available,
    )

    with pytest.raises(InvalidDimension):
        res._query_make(res.cmdargs)


def test_validation_invalid_dimension_subset(resource):
    metrics_available = [
        {
            "Metrics": [
                {
                    "Namespace": "AWS/EC2",
                    "MetricName": "CPUCreditUsage",
                    "Dimensions": [
                        {"Name": "InstanceId", "Value": "i-123454ec7eaad629c"},
                        {"Name": "InstanceId", "Value": "i-123454ec7eaad629d"},
                        {"Name": "InstanceId", "Value": "i-123454ec7eaad629e"},
                    ],
                },
            ]
        },
    ]
    res = resource(
        cmdargs={
            "metric": "CPUCreditUsage",
            "dimensions": [
                dict(Name="InstanceId", Value="i-123454ec7eaad629c"),
                dict(Name="InstanceId", Value="i-123454ec7eaad629f"),
            ],
        },
        metrics_available=metrics_available,
    )

    with pytest.raises(InvalidDimension):
        res._query_make(res.cmdargs)


def test_validation_valid_dimensions_subset(resource):
    metrics_available = [
        {
            "Metrics": [
                {
                    "Namespace": "AWS/EC2",
                    "MetricName": "CPUCreditUsage",
                    "Dimensions": [
                        {"Name": "InstanceId", "Value": "i-123454ec7eaad629c"},
                        {"Name": "InstanceId", "Value": "i-123454ec7eaad629d"},
                        {"Name": "InstanceId", "Value": "i-123454ec7eaad629e"},
                    ],
                },
            ]
        },
    ]
    res = resource(
        cmdargs={
            "metric": "CPUCreditUsage",
            "dimensions": [
                dict(Name="InstanceId", Value="i-123454ec7eaad629c"),
                dict(Name="InstanceId", Value="i-123454ec7eaad629d"),
            ],
        },
        metrics_available=metrics_available,
    )

    assert res._query_make(res.cmdargs)


def test_validation_empty_dimensions_subset(resource):
    metrics_available = [
        {
            "Metrics": [
                {
                    "Namespace": "AWS/EC2",
                    "MetricName": "CPUCreditUsage",
                    "Dimensions": [
                        {"Name": "InstanceId", "Value": "i-123454ec7eaad629c"},
                        {"Name": "InstanceId", "Value": "i-123454ec7eaad629d"},
                        {"Name": "InstanceId", "Value": "i-123454ec7eaad629e"},
                    ],
                },
            ]
        },
    ]
    res = resource(
        cmdargs={
            "metric": "CPUCreditUsage",
            "dimensions": [],
        },
        metrics_available=metrics_available,
    )

    assert res._query_make(res.cmdargs)
