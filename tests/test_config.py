def test_section_exists(resource):
    options = resource(cli_overrides={
        "--credentials": "tests/config/credentials",
        "--profile": "default"
    }).get_config()

    assert all([opt for opt in options.values()])


def test_non_section(resource):
    options = resource(cli_overrides={"--profile": "test"}).get_config()
    assert not all([opt for opt in options.values()])
