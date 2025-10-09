# xa_sdk/devices/bpc30x_channel.py
from __future__ import annotations

from typing import List, Optional, Sequence

from xa_sdk.products.base import XADevice
from xa_sdk.shared.tlmc_type_structures import (
    TLMC_OperatingModes,
    # IO & triggers
    TLMC_IoPortMode, TLMC_IoPortNumber, TLMC_IoPortSource,
    TLMC_IoTriggerInMode, TLMC_IoTriggerOutMode, TLMC_IoTriggerPolarity,
    TLMC_IoPositionTriggerEnableState,
    # Piezo (PZ)
    TLMC_PZ_OutputVoltageControlSources, TLMC_PZ_VoltageLimit,
    TLMC_PZ_PositionControlMode, TLMC_PZ_Status,
    TLMC_PZ_MaxOutputVoltageParams, TLMC_PZ_OutputVoltageControlSourceParams,
    TLMC_PZ_PositionLoopParams, TLMC_PZ_SlewRateParams,
    TLMC_PZ_OutputWaveformParams, TLMC_PZ_OutputWaveformLookupTableSample,
)


class BPC30XCHANNEL(XADevice):
    """
    Thorlabs benchtop piezo controller channel.

    This class preserves method names from your original file, including
    a few legacy misspellings as aliases (e.g., 'ouput' variants).
    """

    # ---------- lifecycle ----------

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
        return "BPC30XCHANNEL"

    # ---------- helpers for native name variants ----------

    def _call_native(self, candidates: Sequence[str], *args):
        """
        Try a sequence of native API function names and call the first that exists.
        """
        for name in candidates:
            if hasattr(self.native_api, name):
                return getattr(self.native_api, name)(self.device_handle, *args)
        raise AttributeError(f"None of the native candidates exist: {candidates}")

    # ---------- conversions (kept for parity with your original) ----------

    def convert_from_device_units_to_physical(self, tlmc_scale_type: int, device_value: int) -> float:
        return super().convert_from_device_units_to_physical(tlmc_scale_type, device_value)

    def convert_from_physical_to_device(self, tlmc_scale_type: int, tlmc_unit_type: int, physical_value: float) -> int:
        return super().convert_from_physical_to_device(tlmc_scale_type, tlmc_unit_type, physical_value)

    # ---------- AUX / IO ----------

    def get_aux_io_port_mode(self, port_number: int, max_wait_in_milliseconds: int) -> int:
        return self._call_native(
            ("get_aux_io_port_mode", "getAuxIoPortMode"),
            int(port_number), int(max_wait_in_milliseconds),
        )

    def get_aux_io_software_states(self, max_wait_in_milliseconds: int) -> int:
        return self._call_native(
            ("get_aux_io_software_states", "getAuxIoSoftwareStates"),
            int(max_wait_in_milliseconds),
        )

    def get_io_configuration_number_of_ports_supported(self) -> int:
        return self._call_native(
            ("get_io_configuration_number_of_ports_supported", "getIoConfigurationNumberOfPortsSupported"),
        )

    def get_io_configuration_params(self, port_number: int, max_wait_in_milliseconds: int):
        return self._call_native(
            ("get_io_configuration_params", "getIoConfigurationParams"),
            int(port_number), int(max_wait_in_milliseconds),
        )

    def set_io_configuration_params(self, port_number: TLMC_IoPortNumber | int,
                                    mode: TLMC_IoPortMode | int,
                                    trigger_out_source: TLMC_IoPortSource | int) -> None:
        self._call_native(
            ("set_io_configuration_params", "setIoConfigurationParams"),
            int(port_number), int(mode), int(trigger_out_source),
        )

    def get_io_position_trigger_enable_state(self, max_wait_in_milliseconds: int) -> int:
        return self._call_native(
            ("get_io_position_trigger_enable_state", "getIoPositionTriggerEnableState"),
            int(max_wait_in_milliseconds),
        )

    def set_io_position_trigger_enable_state(self, new_enable_state: TLMC_IoPositionTriggerEnableState | int,
                                             max_wait_in_milliseconds: int) -> None:
        self._call_native(
            ("set_io_position_trigger_enable_state", "setIoPositionTriggerEnableState"),
            int(new_enable_state), int(max_wait_in_milliseconds),
        )

    def get_io_trigger_params(self, max_wait_in_milliseconds: int):
        return self._call_native(
            ("get_io_trigger_params", "getIoTriggerParams"),
            int(max_wait_in_milliseconds),
        )

    def set_io_trigger_params(self,
                              trigger_in_mode: TLMC_IoTriggerInMode | int,
                              trigger_in_polarity: TLMC_IoTriggerPolarity | int,
                              trigger_in_source: int,
                              trigger_out_mode: TLMC_IoTriggerOutMode | int,
                              trigger_out_polarity: TLMC_IoTriggerPolarity | int,
                              trigger_out_forward_start_position: int,
                              trigger_out_forward_interval: int,
                              trigger_out_forward_number_of_pulses: int,
                              trigger_out_reverse_start_position: int,
                              trigger_out_reverse_interval: int,
                              trigger_out_reverse_number_of_pulses: int,
                              trigger_out_pulse_width: int,
                              trigger_out_number_of_cycles: int) -> None:
        self._call_native(
            ("set_io_trigger_params", "setIoTriggerParams"),
            int(trigger_in_mode), int(trigger_in_polarity), int(trigger_in_source),
            int(trigger_out_mode), int(trigger_out_polarity),
            int(trigger_out_forward_start_position), int(trigger_out_forward_interval), int(trigger_out_forward_number_of_pulses),
            int(trigger_out_reverse_start_position), int(trigger_out_reverse_interval), int(trigger_out_reverse_number_of_pulses),
            int(trigger_out_pulse_width), int(trigger_out_number_of_cycles),
        )

    # ---------- PZ: Max output voltage & limits ----------

    def get_max_output_voltage_params(self, max_wait_in_milliseconds: int) -> TLMC_PZ_MaxOutputVoltageParams:
        # Accept both modern and legacy native names
        return self._call_native(
            ("get_pz_max_output_voltage_params", "pz_get_max_output_voltage_params"),
            int(max_wait_in_milliseconds),
        )

    def set_max_output_voltage(self, max_output_voltage: int) -> None:
        # Legacy method: set only the numeric maximum
        self._call_native(
            ("set_pz_max_output_voltage", "pz_set_max_output_voltage"),
            int(max_output_voltage),
        )

    # Full pair (value + limit)
    def set_pz_max_output_voltage_params(self, max_output_voltage: int, voltage_limit: TLMC_PZ_VoltageLimit | int) -> None:
        self._call_native(
            ("set_pz_max_output_voltage_params", "pz_set_max_output_voltage_params"),
            int(max_output_voltage), int(voltage_limit),
        )

    # ---------- PZ: Output voltage & position ----------

    def get_output_voltage(self, max_wait_in_milliseconds: int) -> int:
        return self._call_native(
            ("get_pz_output_voltage", "pz_get_output_voltage"),
            int(max_wait_in_milliseconds),
        )

    def set_output_voltage(self, new_output_voltage: int) -> None:
        self._call_native(
            ("set_pz_output_voltage", "pz_set_output_voltage"),
            int(new_output_voltage),
        )

    def get_position(self, max_wait_in_milliseconds: int) -> int:
        return self._call_native(
            ("get_pz_position", "pz_get_position"),
            int(max_wait_in_milliseconds),
        )

    def set_position(self, new_position: int) -> None:
        self._call_native(
            ("set_pz_position", "pz_set_position"),
            int(new_position),
        )

    def set_zero(self, max_wait_in_milliseconds: int) -> None:
        self._call_native(
            ("set_pz_zero", "pz_set_zero"),
            int(max_wait_in_milliseconds),
        )

    # ---------- PZ: Control source ----------

    def get_output_voltage_control_source_params(self, max_wait_in_milliseconds: int) -> TLMC_PZ_OutputVoltageControlSourceParams:
        return self._call_native(
            ("get_pz_output_voltage_control_source_params",
             "pz_get_output_voltage_control_source_params",
             "pz_get_ouput_voltage_control_source_params"),  # legacy misspelling
            int(max_wait_in_milliseconds),
        )

    # Legacy alias with original misspelling kept (calls the corrected method)
    def get_ouput_voltage_control_source_params(self, max_wait_in_milliseconds: int) -> TLMC_PZ_OutputVoltageControlSourceParams:  # noqa: D401
        """Legacy alias: calls get_output_voltage_control_source_params()."""
        return self.get_output_voltage_control_source_params(max_wait_in_milliseconds)

    def set_output_voltage_source_params(self, voltage_source: TLMC_PZ_OutputVoltageControlSources | int) -> None:
        self._call_native(
            ("set_pz_output_voltage_source_params",
             "pz_set_output_voltage_source_params",
             "pz_set_ouput_voltage_source_params"),  # legacy misspelling
            int(voltage_source),
        )

    # ---------- PZ: Position control mode & loop ----------

    def get_position_control_mode(self, max_wait_in_milliseconds: int) -> TLMC_PZ_PositionControlMode | int:
        return self._call_native(
            ("get_pz_position_control_mode", "pz_get_position_control_mode"),
            int(max_wait_in_milliseconds),
        )

    def set_position_control_mode(self, new_control_mode: TLMC_PZ_PositionControlMode | int) -> None:
        self._call_native(
            ("set_pz_position_control_mode", "pz_set_position_control_mode"),
            int(new_control_mode),
        )

    def get_position_loop_params(self, max_wait_in_milliseconds: int) -> TLMC_PZ_PositionLoopParams:
        return self._call_native(
            ("get_pz_position_loop_params", "pz_get_position_loop_params"),
            int(max_wait_in_milliseconds),
        )

    def set_position_loop_params(self, proportional: int, integral: int) -> None:
        self._call_native(
            ("set_pz_position_loop_params", "pz_set_position_loop_params"),
            int(proportional), int(integral),
        )

    # ---------- PZ: Slew rate ----------

    def get_slew_rate_params(self, max_wait_in_milliseconds: int) -> TLMC_PZ_SlewRateParams:
        return self._call_native(
            ("get_pz_slew_rate_params", "pz_get_slew_rate_params"),
            int(max_wait_in_milliseconds),
        )

    def set_slew_rate_params(self, open_slew_rate: int, closed_slew_rate: int) -> None:
        # (Your struct field is openLoopSlewRate; we keep the public name unchanged)
        self._call_native(
            ("set_pz_slew_rate_params", "pz_set_slew_rate_params"),
            int(open_slew_rate), int(closed_slew_rate),
        )

    # ---------- PZ: Waveform ----------

    def get_output_waveform_params(self, max_wait_in_milliseconds: int) -> TLMC_PZ_OutputWaveformParams:
        return self._call_native(
            ("get_pz_output_waveform_params",
             "pz_get_output_waveform_params",
             "pz_get_ouput_waveform_params"),  # legacy misspelling
            int(max_wait_in_milliseconds),
        )

    # Legacy alias to match original misspelling
    def get_ouput_waveform_params(self, max_wait_in_milliseconds: int) -> TLMC_PZ_OutputWaveformParams:  # noqa: D401
        """Legacy alias: calls get_output_waveform_params()."""
        return self.get_output_waveform_params(max_wait_in_milliseconds)

    def set_output_waveform_params(self,
                                   mode: int,
                                   num_of_samples_per_cycle: int,
                                   num_of_cycles: int,
                                   sample_delay: int,
                                   pre_cycle_delay: int,
                                   post_cycle_delay: int,
                                   output_trigger_start_index: int,
                                   output_trigger_width: int,
                                   num_of_samples_between_triggers: int) -> None:
        self._call_native(
            ("set_pz_output_waveform_params",
             "pz_set_output_waveform_params",
             "pz_set_ouput_waveform_params"),  # legacy misspelling
            int(mode), int(num_of_samples_per_cycle), int(num_of_cycles),
            int(sample_delay), int(pre_cycle_delay), int(post_cycle_delay),
            int(output_trigger_start_index), int(output_trigger_width),
            int(num_of_samples_between_triggers),
        )

    def set_output_waveform_lookup_table_sample(self, index: int, voltage: int) -> None:
        self._call_native(
            ("set_pz_output_waveform_lookup_table_sample",
             "pz_set_output_waveform_lookup_table_sample"),
            int(index), int(voltage),
        )

    def start_output_waveform(self) -> None:
        self._call_native(
            ("start_pz_output_waveform", "pz_start_output_waveform"),
        )

    def stop_output_waveform(self) -> None:
        self._call_native(
            ("stop_pz_output_waveform", "pz_stop_output_waveform"),
        )

    # ---------- PZ: Status ----------

    def get_status(self, max_wait_in_milliseconds: int) -> TLMC_PZ_Status | int:
        return self._call_native(
            ("get_pz_status", "pz_get_status"),
            int(max_wait_in_milliseconds),
        )

    def get_status_bits(self, max_wait_in_milliseconds: int) -> int:
        # Prefer bit-only native if available; else derive from full status
        if hasattr(self.native_api, "get_pz_status_bits"):
            return self._call_native(("get_pz_status_bits", "pz_get_status_bits"), int(max_wait_in_milliseconds))
        st = self.get_status(max_wait_in_milliseconds)
        return int(st.statusBits) if hasattr(st, "statusBits") else int(st)