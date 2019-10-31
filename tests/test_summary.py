from nagios_aws.summary import CloudWatchSummary


def test_probe_result():
    summary = CloudWatchSummary("n", "m")
    msg = getattr(summary, "_msg")

    assert summary.ok(None) == msg
    assert summary.problem(None) == msg


def test_dimensional_probe_result():
    summary = CloudWatchSummary("n", "m", dimensions={"foo": "bar"})

    assert "foo=bar" in summary.ok(None)
    assert "foo=bar" in summary.problem(None)
