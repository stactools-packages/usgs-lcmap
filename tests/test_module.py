import stactools.usgs_lcmap


def test_version() -> None:
    assert stactools.usgs_lcmap.__version__ is not None
