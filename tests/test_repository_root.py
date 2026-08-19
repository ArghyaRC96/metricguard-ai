from metricguard.application.bootstrap import (
    REPO_ROOT,
)


def test_production_repo_root_contains_settings():

    assert (
        REPO_ROOT
        / "configs"
        / "settings.yaml"
    ).exists()
