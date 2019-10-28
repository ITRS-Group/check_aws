def test_section_exists(resource):
    options = resource(overrides={
        "--credentials": "tests/input/credentials",
        "--profile": "default"
    }).get_config()

    assert all([opt for opt in options.values()])


def test_non_section(resource):
    options = resource(overrides={
        "--profile": "test_non_section",
        "--credentials": "tests/input/credentials"
    }).get_config()

    assert not all([opt for opt in options.values()])
