# xa_sdk/devices/bpc30x.py
from __future__ import annotations

from typing import Optional

from xa_sdk.products.base import XADevice
from xa_sdk.shared.tlmc_type_structures import (
    TLMC_OperatingModes,
)


class BPC30X(XADevice):
    """
    Thorlabs benchtop piezo controller (base unit).

    Backward-compatible with your original BPC30X class while using the
    modern XADevice base (no import cycles, deterministic cleanup).
    """

    def __init__(
        self,
        device: str,
        transport: Optional[str] = "",
        operating_mode: int | TLMC_OperatingModes = TLMC_OperatingModes.Default,
        *args,
        **kwargs,
    ):
        super().__init__(device, transport, operating_mode, *args, **kwargs)

    def product_name(self) -> str:
        return "BPC30X"

    # ---------- Base-unit specific ----------

    def rack_identify(self, channel: int) -> None:
        """
        Cause the base unit's LEDs to flash (channel index is passed to native call).
        """
        # Prefer 'rack_identify', but fall back to legacy names if needed.
        for candidate in ("rack_identify", "identify_rack", "rackIdentify"):
            if hasattr(self.native_api, candidate):
                getattr(self.native_api, candidate)(self.device_handle, int(channel))
                return
        raise AttributeError("Native API has no rack_identify/_legacy variants")

    # Digital output pass-throughs (present in your original class)
    def get_digital_output_params(self, max_wait_in_milliseconds: int) -> int:
        return super().get_digital_output_params(max_wait_in_milliseconds)

    # original typo: set_digital_ouput_params (we keep the correct name; add alias below)
    def set_digital_output_params(self, new_output_state: int) -> None:
        super().set_digital_output_params(new_output_state)

    # Legacy alias to preserve your original method spelling
    def set_digital_ouput_params(self, new_ouput_state: int) -> None:  # noqa: D401
        """Legacy alias: calls set_digital_output_params()."""
        self.set_digital_output_params(new_ouput_state)