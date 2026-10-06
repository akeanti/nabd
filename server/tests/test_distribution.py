from importlib.metadata import version

import nabd
import nabd_collector
import nabd_events


def test_all_packages_ship_in_the_nabd_distribution() -> None:
    distribution_version = version("nabd")

    assert nabd.__version__ == distribution_version
    assert nabd_collector.__version__ == distribution_version
    assert nabd_events.__version__ == distribution_version
