"""The airtouch2 integration."""
from __future__ import annotations

from airtouch2 import At2Client

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .const import DOMAIN

PLATFORMS: list[Platform] = [Platform.CLIMATE, Platform.FAN]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up airtouch2 from a config entry."""

    hass.data.setdefault(DOMAIN, {})
    client = At2Client(entry.data[CONF_HOST])
    if not await client.connect():
        raise ConfigEntryNotReady("Airtouch2 client failed to connect")
    client.run()
    await client.wait_for_ac()
    if not client.aircons:
        raise ConfigEntryNotReady("No AC units were found")
    hass.data[DOMAIN][entry.entry_id] = client
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        client: At2Client = hass.data[DOMAIN][entry.entry_id]
        await client.stop()
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
