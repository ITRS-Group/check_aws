from nagiosplugin import Range


def test_probe_context_thresholds(target):
    ctx = target(dict(warning=10, critical=15)).context

    assert ctx.warning == Range(10)
    assert ctx.critical == Range(15)


def test_probe_context_no_thresholds(target):
    ctx = target().context

    assert ctx.warning == ctx.critical == Range(0)


def test_probe_context_metric_name(target):
    ctx = target(dict(metric="test")).context

    assert ctx.name == "test"
