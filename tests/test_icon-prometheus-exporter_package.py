"""Test the icon-prometheus-exporter package."""


def test_version_is_string():
    import icon-prometheus-exporter
    assert isinstance(icon-prometheus-exporter.__version__, str)
