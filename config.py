# Environment configuration for the login-flow suite.
#
# Centralises all environment-specific values (URLs, timeouts) in one place.
# Tests receive an EnvironmentConfig instance via the `env_config` fixture
# rather than reading raw JSON themselves.
#
# Usage:
#   pytest --env staging     # run against staging
#   pytest                   # defaults to production
#
# Adding a new environment:
#   1. Add an entry to _CONFIGS below.
#   2. No test code needs to change.

from dataclasses import dataclass


@dataclass(frozen=True)
class EnvironmentConfig:
    env: str
    base_url: str
    login_url: str
    home_url: str
    # Timeouts in milliseconds
    page_load_timeout: int
    element_wait_timeout: int


_CONFIGS: dict[str, EnvironmentConfig] = {
    "production": EnvironmentConfig(
        env="production",
        base_url="https://www.hudl.com",
        login_url="https://www.hudl.com/login",
        home_url="https://www.hudl.com/home",
        page_load_timeout=15000,
        element_wait_timeout=10000,
    ),
    "staging": EnvironmentConfig(
        env="staging",
        base_url="https://www.hudl.com",
        login_url="https://www.hudl.com/login",
        home_url="https://www.hudl.com/home",
        page_load_timeout=20000,
        element_wait_timeout=15000,
    ),
}


def get_config(env: str = "production") -> EnvironmentConfig:
    if env not in _CONFIGS:
        valid = ", ".join(_CONFIGS)
        raise ValueError(f"Unknown environment '{env}'. Valid options: {valid}")
    return _CONFIGS[env]
