"""AirTouch 2 component to control AirTouch 2 Climate Device."""
from __future__ import annotations

import logging

from homeassistant.components.climate import ClimateEntity

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN

from airtouch2 import At2Client
from homeassistant.components.airtouch2.Airtouch2ClimateEntity import Airtouch2ClimateEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Airtouch 2."""
    airtouch2_client: At2Client = hass.data[DOMAIN][config_entry.entry_id]
    entities: list[ClimateEntity] = [
        Airtouch2ClimateEntity(ac) for ac in airtouch2_client.aircons
    ]

    _LOGGER.debug(" Found entities %s", entities)
    async_add_entities(entities)
