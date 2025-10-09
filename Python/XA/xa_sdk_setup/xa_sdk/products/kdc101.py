# xa_sdk/devices/kdc101.py
from __future__ import annotations

from typing import Optional

from xa_sdk.products.base import XADevice
from xa_sdk.shared.tlmc_type_structures import (
    TLMC_OperatingModes,
    TLMC_EnableStates,
    TLMC_MoveModes,
    TLMC_MoveDirection,
    TLMC_StopModes,
)


class KDC101(XADevice):
    """
    Thorlabs KDC101 (brushed DC) — device-specific methods live here.
    The base class stays generic so other devices can define their own APIs.
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
        return "KDC101"

    # -------- connected product --------

    def get_connected_product(self) -> str:
        return self.native_api.get_connected_product(self.device_handle)

    def get_connected_product_info(self):
        return self.native_api.get_connected_product_info(self.device_handle)

    def get_connected_products_supported(self) -> str:
        return self.native_api.get_connected_products_supported(self.device_handle)

    def set_connected_product(self, product_name: str) -> None:
        self.native_api.set_connected_product(self.device_handle, product_name)

    def set_connected_product_info(
        self,
        product_name: str,
        axis_type: int,
        movement_type: int,
        unit_type: int,
        distance_scale_factor: float,
        velocity_scale_factor: float,
        acceleration_scale_factor: float,
        min_position: float,
        max_position: float,
        max_velocity: float,
        max_acceleration: float,
    ) -> None:
        self.native_api.set_connected_product_info(
            self.device_handle,
            product_name,
            axis_type,
            movement_type,
            unit_type,
            distance_scale_factor,
            velocity_scale_factor,
            acceleration_scale_factor,
            min_position,
            max_position,
            max_velocity,
            max_acceleration,
        )

    # -------- digital IO / enable --------

    def get_digital_output_params(self, max_wait_ms: int) -> int:
        return self.native_api.get_digital_output_params(self.device_handle, max_wait_ms)

    def set_digital_output_params(self, new_output_state: int) -> None:
        self.native_api.set_digital_output_params(self.device_handle, new_output_state)

    def get_enable_state(self, max_wait_ms: int) -> int:
        return self.native_api.get_enable_state(self.device_handle, max_wait_ms)

    def set_enable_state(self, enable_state: TLMC_EnableStates | int) -> None:
        self.native_api.set_enable_state(self.device_handle, int(enable_state))

    # -------- motion parameters --------

    def get_general_move_params(self, max_wait_ms: int):
        return self.native_api.get_general_move_params(self.device_handle, max_wait_ms)

    def set_general_move_params(self, backlash_distance: int) -> None:
        self.native_api.set_general_move_params(self.device_handle, backlash_distance)

    def get_home_params(self, max_wait_ms: int):
        return self.native_api.get_home_params(self.device_handle, max_wait_ms)

    def set_home_params(self, direction: int, limit_switch: int, velocity: int, offset_distance: int) -> None:
        self.native_api.set_home_params(self.device_handle, direction, limit_switch, velocity, offset_distance)

    def get_limit_switch_params(self, max_wait_ms: int):
        return self.native_api.get_limit_switch_params(self.device_handle, max_wait_ms)

    def set_limit_switch_params(
        self,
        clockwise_limit_mode: int,
        counter_clockwise_mode: int,
        clockwise_soft_limit: int,
        counter_clockwise_soft_limit: int,
        soft_limit_operating_mode: int,
    ) -> None:
        self.native_api.set_limit_switch_params(
            self.device_handle,
            clockwise_limit_mode,
            counter_clockwise_mode,
            clockwise_soft_limit,
            counter_clockwise_soft_limit,
            soft_limit_operating_mode,
        )

    def get_move_absolute_params(self, max_wait_ms: int):
        return self.native_api.get_move_absolute_params(self.device_handle, max_wait_ms)

    def set_move_absolute_params(self, absolute_position: int) -> None:
        self.native_api.set_move_absolute_params(self.device_handle, absolute_position)

    def get_move_relative_params(self, max_wait_ms: int):
        return self.native_api.get_move_relative_params(self.device_handle, max_wait_ms)

    def set_move_relative_params(self, move_relative_distance: int) -> None:
        self.native_api.set_move_relative_params(self.device_handle, move_relative_distance)

    def get_move_jog_params(self, max_wait_ms: int):
        return self.native_api.get_move_jog_params(self.device_handle, max_wait_ms)

    def set_move_jog_params(
        self,
        jog_mode: int,
        step_size: int,
        min_velocity: int,
        max_velocity: int,
        acceleration: int,
        stop_mode: int,
    ) -> None:
        self.native_api.set_move_jog_params(
            self.device_handle,
            jog_mode,
            step_size,
            min_velocity,
            max_velocity,
            acceleration,
            stop_mode,
        )

    def get_velocity_params(self, max_wait_ms: int):
        return self.native_api.get_velocity_params(self.device_handle, max_wait_ms)

    def set_velocity_params(self, min_velocity: int, acceleration: int, max_velocity: int) -> None:
        self.native_api.set_velocity_params(self.device_handle, min_velocity, acceleration, max_velocity)

    def get_position_counter(self, max_wait_ms: int) -> int:
        return self.native_api.get_position_counter(self.device_handle, max_wait_ms)

    def set_position_counter(self, new_position_counter: int) -> None:
        self.native_api.set_position_counter(self.device_handle, new_position_counter)

    # -------- motion commands --------

    def home(self, timeout_ms: int) -> None:
        self.native_api.home(self.device_handle, timeout_ms)

    def move_absolute(self, position: int, wait_ms: int) -> None:
        self.native_api.move_absolute(self.device_handle, TLMC_MoveModes.MoveMode_Absolute, position, wait_ms)

    def move_relative(self, step: int, wait_ms: int) -> None:
        self.native_api.move_relative(self.device_handle, TLMC_MoveModes.MoveMode_Relative, step, wait_ms)

    def move_continuous(self, direction: TLMC_MoveDirection | int, wait_ms: int) -> None:
        self.native_api.move_continuous(self.device_handle, int(direction), wait_ms)

    def move_jog_dir(self, direction: TLMC_MoveDirection | int, wait_ms: int) -> None:
        """Directional jog (explicit); 'move_jog' convenience is also available."""
        self.native_api.move_jog(self.device_handle, int(direction), wait_ms)

    def move_jog(self, forward: bool = True, wait_ms: int = 3000) -> None:
        direction = (
            TLMC_MoveDirection.Move_Direction_Forward
            if forward else TLMC_MoveDirection.Move_Direction_Reverse
        )
        self.native_api.move_jog(self.device_handle, direction, wait_ms)

    def stop(self, profiled: bool, wait_ms: int) -> None:
        mode = TLMC_StopModes.StopMode_Profiled if profiled else TLMC_StopModes.StopMode_Immediate
        self.native_api.stop(self.device_handle, mode, wait_ms)

    # -------- DC PID --------

    def get_dc_pid_params(self, max_wait_ms: int):
        return self.native_api.get_dc_pid_params(self.device_handle, max_wait_ms)

    def set_dc_pid_params(self, proportional: int, integral: int, derivative: int, integral_limit: int, filter_control: int) -> None:
        self.native_api.set_dc_pid_params(
            self.device_handle, proportional, integral, derivative, integral_limit, filter_control
        )

    # -------- K-Cube specifics: IO trigger / MMI --------

    def get_kcube_io_trigger_params(self, max_wait_ms: int):
        return self.native_api.get_kcube_io_trigger_params(self.device_handle, max_wait_ms)

    def set_kcube_io_trigger_params(
        self,
        trigger_one_mode: int,
        trigger_one_polarity: int,
        trigger_two_mode: int,
        trigger_two_polarity: int,
    ) -> None:
        self.native_api.set_kcube_io_trigger_params(
            self.device_handle, trigger_one_mode, trigger_one_polarity, trigger_two_mode, trigger_two_polarity
        )

    def get_kcube_mmi_lock_state(self, max_wait_ms: int) -> int:
        return self.native_api.get_kcube_mmi_lock_state(self.device_handle, max_wait_ms)

    def set_kcube_mmi_lock_state(self, lock_state: int) -> None:
        self.native_api.set_kcube_mmi_lock_state(self.device_handle, lock_state)

    def get_kcube_mmi_params(self, max_wait_ms: int):
        return self.native_api.get_kcube_mmi_params(self.device_handle, max_wait_ms)

    def set_kcube_mmi_params(
        self,
        joystick_mode: int,
        joystick_velocity: int,
        joystick_acceleration: int,
        joystick_direction_sense: int,
        position_one: int,
        position_two: int,
        display_brightness: int,
        display_timeout: int,
        display_dim_level: int,
        position_three: int,
        joystick_sensitivity: int,
    ) -> None:
        self.native_api.set_kcube_mmi_params(
            self.device_handle,
            joystick_mode,
            joystick_velocity,
            joystick_acceleration,
            joystick_direction_sense,
            position_one,
            position_two,
            display_brightness,
            display_timeout,
            display_dim_level,
            position_three,
            joystick_sensitivity,
        )

    # -------- status --------

    def get_rich_response(self):
        return self.native_api.get_rich_response(self.device_handle)

    def get_status_item(self, status_item_id: int):
        return self.native_api.get_status_item(self.device_handle, status_item_id)

    def get_status_item_count(self) -> int:
        return self.native_api.get_status_item_count(self.device_handle)

    def get_status_items(self, start_index: int, number_of_items: int):
        return self.native_api.get_status_items(self.device_handle, start_index, number_of_items)

    def get_universal_status(self, max_wait_ms: int):
        return self.native_api.get_universal_status(self.device_handle, max_wait_ms)

    def get_universal_status_bits(self, max_wait_ms: int) -> int:
        return self.native_api.get_universal_status_bits(self.device_handle, max_wait_ms)

    # -------- maintenance --------

    def restore_to_factory_defaults(self) -> None:
        self.native_api.restore_to_factory_defaults(self.device_handle)