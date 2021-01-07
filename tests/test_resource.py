def test_frame(resource):
    res = resource()

    assert res.payload.get("StartTime") == res.frame.start
    assert res.payload.get("EndTime") == res.frame.end
