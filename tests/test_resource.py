def test_frame(resource):
    res = resource()

    assert res.payload.get("start_time") == res.frame.start
    assert res.payload.get("end_time") == res.frame.end
