"""Shared test fixtures."""

from __future__ import annotations

import sys
from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture(autouse=True)
def mock_gpio() -> MagicMock:  # type: ignore[misc]
    """Mock RPi.GPIO for all tests."""
    mock_rpi = MagicMock()
    mock_gpio_module = MagicMock()
    mock_gpio_module.BCM = 11
    mock_gpio_module.OUT = 0
    mock_rpi.GPIO = mock_gpio_module

    with patch.dict(sys.modules, {"RPi": mock_rpi, "RPi.GPIO": mock_gpio_module}):
        yield mock_gpio_module
