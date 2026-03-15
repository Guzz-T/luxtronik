"""Helper for luxtronik heatpump module."""

# region Imports
from __future__ import annotations

import socket
import struct
import threading
import time

from luxtronik import (
    discover,
    Calculations,
    Parameters,
    Visibilities,
    Luxtronik,
)

from .const import (
    LOGGER,
    LUX_MODELS_ALPHA_INNOTEC,
    LUX_MODELS_NOVELAN,
    LUX_MODELS_OTHER,
)

# endregion Imports


def get_manufacturer_by_model(model: str) -> str | None:
    """Return the manufacturer."""
    if model is None:
        return None
    if model.startswith(tuple(LUX_MODELS_NOVELAN)):
        return "Novelan"
    if model.startswith(tuple(LUX_MODELS_ALPHA_INNOTEC)):
        return "Alpha Innotec"
    return None


def get_firmware_download_id(installed_version: str | None) -> int | None:
    """Return the heatpump firmware id for the download portal."""
    if installed_version is None:
        return None
    if installed_version.startswith("V1."):
        return 0
    if installed_version.startswith("V2."):
        return 1
    if installed_version.startswith("V3."):
        return 2
    if installed_version.startswith("V4."):
        return 3
    if installed_version.startswith("F1."):
        return 4
    if installed_version.startswith("WWB1."):
        return 5
    if installed_version.startswith("smo"):
        return 6
    return None


def get_manufacturer_firmware_url_by_model(model: str, default_id: int) -> str:
    """Return the manufacturer firmware download url."""
    layout_id = 0

    if model is None:
        layout_id = default_id
    elif model.startswith(tuple(LUX_MODELS_ALPHA_INNOTEC)):
        layout_id = 1
    elif model.startswith(tuple(LUX_MODELS_NOVELAN)):
        layout_id = 2
    elif model.startswith(tuple(LUX_MODELS_OTHER)):
        layout_id = 3
    return f"https://www.heatpump24.com/DownloadArea.php?layout={layout_id}"
