from check_aws.consts import NAME


def test_resource_frame(resource):
    res = resource()

    assert res.payload.get("StartTime") == res.frame.start
    assert res.payload.get("EndTime") == res.frame.end


def test_resource_session_type(resource):
    res = resource(dict(region="test"))

    assert hasattr(res.connection, "get_metric_statistics")


def test_resource_identifier(resource):
    res = resource()

    assert res.name == NAME
