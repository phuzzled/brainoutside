"""Regression checks for the repository's Coolify Compose contract."""
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[3]
COMPOSE_PATH = REPO_ROOT / "docker-compose.yml"


def _compose() -> dict:
    return yaml.safe_load(COMPOSE_PATH.read_text(encoding="utf-8"))


def test_coolify_discovers_both_required_environment_variables() -> None:
    source = COMPOSE_PATH.read_text(encoding="utf-8")

    assert "${POSTGRES_PASSWORD:?" in source
    assert "${ALLOWED_HOSTS:?" in source


def test_optional_git_credentials_are_not_forced_into_a_fresh_deploy() -> None:
    compose = _compose()
    app = compose["x-app"]
    worker = compose["services"]["worker"]

    assert "BRAIN_GIT_SSH_KEY_PATH" not in app["environment"]
    assert "BRAIN_GIT_WRITE_PAT_PATH" not in worker["environment"]
    assert all("/run/secrets/" not in volume for volume in app["volumes"])
    assert all("/run/secrets/" not in volume for volume in worker["volumes"])


def test_env_file_uses_portable_short_syntax() -> None:
    compose = _compose()

    assert compose["x-app"]["env_file"] == [".env"]
