from check_aws.summary import CloudWatchSummary


def test_probe_result():
    summary = CloudWatchSummary("n", "m")
    msg = summary.get_message()

    assert summary.ok(None) == msg
    assert summary.problem(None) == msg


def test_dimensional_probe_result():
    summary = CloudWatchSummary("n", "m", dimensions=[dict(Name="foo", Value="bar")])

    assert "foo=bar" in summary.ok(None)
    assert "foo=bar" in summary.problem(None)
