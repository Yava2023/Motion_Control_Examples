# xa_sdk/devices/base.py
from __future__ import annotations

from contextlib import AbstractContextManager
from types import TracebackType
from typing import Any, List, Optional, Tuple

from xa_sdk.native_sdks.xa_sdk import XASDK
from xa_sdk.shared.xa_error_factory import XADeviceException
from xa_sdk.shared.tlmc_type_structures import (
    TLMC_OperatingModes,
    TLMC_EndOfMoveMessagesModes,
    TLMC_SettingStringFormat,
)


class XADevice(AbstractContextManager):
    """
    Minimal, device-agnostic base class.

    Contains only functionality common to *all* devices:
      - lifecycle (open/close/disconnect, identify, logging)
      - device/hardware info
      - settings (get, set, list, and string formats)
      - operating modes / end-of-move messages
      - unit conversions (device <-> physical)
    Device- or family-specific methods go into subclasses (e.g., KDC101, BPC30XChannel).
    """

    # ---------- lifecycle ----------

    def __init__(
        self,
        device: str,
        transport: Optional[str] = "",
        operating_mode: int | TLMC_OperatingModes = TLMC_OperatingModes.Default,
        sdk: Optional[XASDK] = None,
        auto_open: bool = True,
    ):
        self._device_id: str = str(device)
        self._transport: str = "" if transport is None else str(transport)
        self._operating_mode: int = int(operating_mode)
        self._sdk: XASDK = sdk or XASDK()
        self._handle: Optional[int] = None

        if auto_open:
            self.open()

    def __enter__(self) -> "XADevice":
        self.open()
        return self

    # mypy-friendly: returning None = do not suppress exceptions
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        self.close()

    # ---------- properties ----------

    @property
    def device_id(self) -> str:
        return self._device_id

    @property
    def transport(self) -> str:
        return self._transport

    @property
    def device_handle(self) -> int:
        if self._handle is None:
            raise XADeviceException("Device not opened", error_code=-1)
        return self._handle

    @property
    def native_api(self) -> XASDK:
        """Back-compat alias used in older classes."""
        return self._sdk

    # ---------- subclass hook ----------

    def product_name(self) -> str:
        """Optional friendly name for UI/logging; subclasses may override."""
        return self.__class__.__name__

    # ---------- connection / session ----------

    def open(self) -> int:
        """Open/attach; returns integer handle."""
        if self._handle is not None:
            return self._handle
        h = self._sdk.open(self._device_id, self._transport, self._operating_mode)
        self._handle = h
        return h

    def close(self) -> None:
        """Close the session."""
        if self._handle is not None:
            try:
                self._sdk.close(self._handle)
            finally:
                self._handle = None

    def disconnect(self) -> None:
        """Drop the transport link (USB/TCP)."""
        self._sdk.disconnect(self.device_handle)

    # ---------- diagnostics / logging ----------

    def add_user_message_to_log(self, user_message: str) -> None:
        self._sdk.add_user_message_to_log(user_message)

    def identify(self) -> None:
        """Blink LEDs to prove connection."""
        self._sdk.identify(self.device_handle)

    # ---------- device / hardware info ----------

    def get_device_info(self, max_wait_in_milliseconds: int | None = None):
        # Some stacks ignore the wait here; keep signature for compatibility.
        return self._sdk.get_device_info(self.device_handle)

    def get_hardware_info(self, max_wait_in_milliseconds: int):
        return self._sdk.get_hardware_info(self.device_handle, max_wait_in_milliseconds)

    # ---------- settings (single & bulk) ----------

    def get_setting(self, settings_name: str, max_wait_in_milliseconds: int):
        return self._sdk.get_setting(self.device_handle, settings_name, max_wait_in_milliseconds)

    def get_setting_as_string(
        self,
        buffer_length: int = 4096,
        setting_string_format: TLMC_SettingStringFormat | int =
            TLMC_SettingStringFormat.TLMC_SettingStringFormat_SemiStructured,
        include_read_only_items: bool = True,
    ) -> Tuple[str, int]:
        """Return (text, length); internal allocation—no caller-provided buffer needed."""
        return self._sdk.get_settings_as_string(
            self.device_handle, buffer_length, int(setting_string_format), include_read_only_items
        )

    # Convenience alias (plural form seen in older code)
    def get_settings_as_string(
        self,
        buffer_length: int = 4096,
        setting_string_format: TLMC_SettingStringFormat | int =
            TLMC_SettingStringFormat.TLMC_SettingStringFormat_SemiStructured,
        include_read_only_items: bool = True,
    ) -> Tuple[str, int]:
        return self.get_setting_as_string(buffer_length, setting_string_format, include_read_only_items)

    def get_setting_count(self) -> int:
        return self._sdk.get_setting_count(self.device_handle)

    def get_setting_discrete_values(self, settings_name: str, buffer_length: int = 2048) -> Tuple[str, int]:
        """Return (text, length) for the setting's discrete values."""
        return self._sdk.get_setting_discrete_values(self.device_handle, settings_name, buffer_length)

    def get_settings(self, source_start_index: int, number_of_items: int) -> List[Any]:
        """Return a list of TLMC_Setting (ctypes) objects."""
        return self._sdk.get_settings(self.device_handle, source_start_index, number_of_items)

    def set_setting(self, settings_name: str, tlmc_value: Any) -> None:
        """Set a single setting using a TLMC_Value union (ctypes)."""
        if tlmc_value is None:
            raise ValueError("tlmc_value (TLMC_Value) is required")
        self._sdk.set_setting(self.device_handle, settings_name, tlmc_value)

    def set_settings_from_string(self, settings_text: str) -> None:
        """Apply settings from a JSON or semi-structured string."""
        self._sdk.set_settings_from_string(self.device_handle, settings_text)

    # ---------- operating / messaging modes ----------

    def set_end_of_message_mode(self, mode: TLMC_EndOfMoveMessagesModes | int) -> None:
        self._sdk.set_end_of_message_mode(self.device_handle, int(mode))

    def set_status_mode(self, operating_mode: TLMC_OperatingModes | int) -> None:
        self._sdk.set_status_mode(self.device_handle, int(operating_mode))

    # ---------- conversions ----------

    def convert_from_device_units_to_physical(self, tlmc_scale_type: int, device_value: int) -> float:
        return self._sdk.convert_from_device_units_to_physical(self.device_handle, tlmc_scale_type, device_value)

    def convert_from_physical_to_device(self, tlmc_scale_type: int, tlmc_unit_type: int, physical_value: float) -> int:
        return self._sdk.convert_from_physical_to_device(self.device_handle, tlmc_scale_type, tlmc_unit_type, physical_value)

    # ---------- misc helper ----------

    def get_method_list(self, cls: type | None = None) -> List[str]:
        """List public methods on the class (compat helper)."""
        target = cls or self.__class__
        names = []
        for name, attr in target.__dict__.items():
            if name.startswith("_"):
                continue
            if callable(attr):
                names.append(name)
        names.sort()
        return names