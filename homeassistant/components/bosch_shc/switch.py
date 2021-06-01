"""Platform for switch integration."""
from boschshcpy import (
    SHCCamera360,
    SHCCameraEyes,
    SHCSession,
    SHCSmartPlug,
    SHCSmartPlugCompact,
)

from homeassistant.components.switch import (
    DEVICE_CLASS_OUTLET,
    DEVICE_CLASS_SWITCH,
    SwitchEntity,
)

from .const import DATA_SESSION, DOMAIN
from .entity import SHCEntity


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the SHC switch platform."""

    entities = []
    session: SHCSession = hass.data[DOMAIN][config_entry.entry_id][DATA_SESSION]

    for switch in session.device_helper.smart_plugs:

        entities.append(
            SmartPlugSwitch(
                device=switch,
                parent_id=session.information.unique_id,
                entry_id=config_entry.entry_id,
            )
        )

    for switch in session.device_helper.smart_plugs_compact:

        entities.append(
            SmartPlugCompactSwitch(
                device=switch,
                parent_id=session.information.unique_id,
                entry_id=config_entry.entry_id,
            )
        )

    for switch in session.device_helper.camera_eyes:

        entities.append(
            CameraEyesSwitch(
                device=switch,
                parent_id=session.information.unique_id,
                entry_id=config_entry.entry_id,
            )
        )

    for switch in session.device_helper.camera_360:

        entities.append(
            Camera360Switch(
                device=switch,
                parent_id=session.information.unique_id,
                entry_id=config_entry.entry_id,
            )
        )

    if entities:
        async_add_entities(entities)


class SmartPlugSwitch(SHCEntity, SwitchEntity):
    """Representation of a SHC smart plug switch."""

    @property
    def device_class(self):
        """Return the class of this device."""
        return (
            DEVICE_CLASS_OUTLET
            if self._device.device_model == "PSM"
            else DEVICE_CLASS_SWITCH
        )

    @property
    def is_on(self):
        """Return the switch state is currently on or off."""
        return self._device.state == SHCSmartPlug.PowerSwitchService.State.ON

    @property
    def today_energy_kwh(self):
        """Total energy usage in kWh."""
        return self._device.energyconsumption / 1000.0

    @property
    def current_power_w(self):
        """Return the current power usage in W."""
        return self._device.powerconsumption

    def turn_on(self, **kwargs):
        """Turn the switch on."""
        self._device.state = True

    def turn_off(self, **kwargs):
        """Turn the switch off."""
        self._device.state = False

    def toggle(self, **kwargs):
        """Toggles the switch."""
        self._device.state = not self.is_on


class SmartPlugCompactSwitch(SHCEntity, SwitchEntity):
    """Representation of a smart plug compact switch."""

    @property
    def device_class(self):
        """Return the class of this device."""
        return DEVICE_CLASS_OUTLET

    @property
    def is_on(self):
        """Return the switch state is currently on or off."""
        return self._device.state == SHCSmartPlugCompact.PowerSwitchService.State.ON

    @property
    def today_energy_kwh(self):
        """Total energy usage in kWh."""
        return self._device.energyconsumption / 1000.0

    @property
    def current_power_w(self):
        """Return the current power usage in W."""
        return self._device.powerconsumption

    def turn_on(self, **kwargs):
        """Turn the switch on."""
        self._device.state = True

    def turn_off(self, **kwargs):
        """Turn the switch off."""
        self._device.state = False

    def toggle(self, **kwargs):
        """Toggles the switch."""
        self._device.state = not self.is_on

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return {
            "communication_quality": self._device.communicationquality.name,
        }


class CameraEyesSwitch(SHCEntity, SwitchEntity):
    """Representation of camera eyes as switch."""

    @property
    def should_poll(self):
        """Camera Eyes needs polling."""
        return True

    def update(self):
        """Trigger an update of the device."""
        self._device.update()

    @property
    def is_on(self):
        """Return the state of the switch."""
        return self._device.cameralight == SHCCameraEyes.CameraLightService.State.ON

    def turn_on(self, **kwargs):
        """Turn the switch on."""
        self._device.cameralight = True

    def turn_off(self, **kwargs):
        """Turn the switch off."""
        self._device.cameralight = False

    def toggle(self, **kwargs):
        """Toggles the switch."""
        self._device.cameralight = not self.is_on


class Camera360Switch(SHCEntity, SwitchEntity):
    """Representation of camera 360 as switch."""

    @property
    def should_poll(self):
        """Camera 360 needs polling."""
        return True

    def update(self):
        """Trigger an update of the device."""
        self._device.update()

    @property
    def is_on(self):
        """Return the state of the switch."""
        return (
            self._device.privacymode == SHCCamera360.PrivacyModeService.State.DISABLED
        )

    def turn_on(self, **kwargs):
        """Turn the switch on."""
        self._device.privacymode = False

    def turn_off(self, **kwargs):
        """Turn the switch off."""
        self._device.privacymode = True

    def toggle(self, **kwargs):
        """Toggles the switch."""
        self._device.privacymode = not self.is_on
