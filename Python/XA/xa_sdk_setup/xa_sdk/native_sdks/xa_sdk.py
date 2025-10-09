# xa_sdk.py — High-level wrapper patched to use corrected TLMC_SDK calls.
# - Properly checks return codes and raises via XAErrorFactory.
# - Returns the correct out-values (not return codes).
# - Aligns signatures with the header-based low-level functions.

from ctypes import c_uint32, create_string_buffer
from xa_sdk.native_sdks.tlmc_core_interface import NativeSDKInterface
from xa_sdk.native_sdks.tlmc_core import TLMC_SDK
from xa_sdk.shared.xa_error_factory import XAErrorFactory


class XASDK(NativeSDKInterface):
    """Main wrapper class calling TLMC_SDK (native DLL) with Python-friendly signatures."""

    # ---- System ----

    @staticmethod
    def startup(settings_file_name: str):
        rc = TLMC_SDK.startup(settings_file_name)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)

    @staticmethod
    def shutdown():
        rc = TLMC_SDK.shutdown()
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)

    @staticmethod
    def try_load_library(current_path):
        """Load tlmc_xa_native.dll from the supplied directory path."""
        TLMC_SDK.try_load_library(current_path)

    def add_user_message_to_log(self, user_message):
        rc = TLMC_SDK.add_user_message_to_log(user_message)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)

    # ---- Open/Close/Disconnect ----

    def open(self, device, transport, operating_mode):
        handle = c_uint32(0)
        rc = TLMC_SDK.open(device, transport, operating_mode, handle)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)
        return handle.value

    def close(self, handle):
        rc = TLMC_SDK.close(handle)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)

    def disconnect(self, handle):
        rc = TLMC_SDK.disconnect(handle)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)

    # ---- Conversion ----

    def convert_from_device_units_to_physical(self, handle, tlmc_scale_type, device_value):
        out = [None]
        rc = TLMC_SDK.convert_from_device_units_to_physical(handle, tlmc_scale_type, device_value, out)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)
        return out[0]  # physical value

    def convert_from_physical_to_device(self, handle, tlmc_scale_type, tlmc_unit_type, physical_value):
        out = [None]
        rc = TLMC_SDK.convert_from_physical_to_device(handle, tlmc_scale_type, tlmc_unit_type, physical_value, out)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)
        return out[0]  # device value

    # ---- Simulation ----

    @staticmethod
    def create_simulation(description: dict):
        rc = TLMC_SDK.create_simulation(description)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)

    @staticmethod
    def remove_simulation(description: dict):
        rc = TLMC_SDK.remove_simulation(description)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)

    # ---- Device list / info ----

    def get_device_list_item_count(self):
        count = [None]
        rc = TLMC_SDK.get_device_list_item_count(count)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)
        return count[0]

    def get_device_list_items(self, source_start_index, number_of_items):
        dest = [None] * number_of_items
        copied = [0]
        rc = TLMC_SDK.get_device_list_items(source_start_index, number_of_items, dest, copied)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)
        # Return only the filled slice
        return dest[:copied[0]]

    def get_device_info(self, handle):
        info = [None]
        rc = TLMC_SDK.get_device_info(handle, info)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)
        return info[0]

    # ---- Strings / Settings ----

    def get_connected_product(self, handle):
        prod = [None]
        rc = TLMC_SDK.get_connected_product(handle, prod)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)
        return prod[0]

    def get_connected_product_info(self, handle):
        info = [None]
        rc = TLMC_SDK.get_connected_product_info(handle, info)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)
        return info[0]

    def get_connected_products_supported(self, handle, buffer_length=256):
        out = [None]
        rc = TLMC_SDK.get_connected_products_supported(handle, out, buffer_length)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)
        return out[0]

    def get_setting(self, handle, settings_name, max_wait_in_milliseconds):
        st = [None]
        rc = TLMC_SDK.get_setting(handle, settings_name, st, max_wait_in_milliseconds)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)
        return st[0]

    def get_setting_count(self, handle):
        count = [None]
        rc = TLMC_SDK.get_setting_count(handle, count)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)
        return count[0]

    def get_setting_discrete_values(self, handle, settings_name, buffer_length=1024):
        buf = create_string_buffer(buffer_length)
        result_len = [0]
        rc = TLMC_SDK.get_setting_discrete_values(handle, settings_name, buf, buffer_length, result_len)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)
        return buf.value.decode('utf-8', errors='ignore'), result_len[0]

    def get_settings(self, handle, source_start_index, number_of_items):
        dest = [None] * number_of_items
        copied = [0]
        rc = TLMC_SDK.get_settings(handle, source_start_index, number_of_items, dest, copied)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)
        return dest[:copied[0]]

    def get_settings_as_string(self, handle, buffer_length, tlmc_setting_string_format, include_read_only_items):
        buf = create_string_buffer(buffer_length)
        result_len = [0]
        rc = TLMC_SDK.get_settings_as_string(handle, buf, buffer_length, result_len, tlmc_setting_string_format, include_read_only_items)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)
        return buf.value.decode('utf-8', errors='ignore'), result_len[0]

    def set_setting(self, handle, settings_name, tlmc_value):
        rc = TLMC_SDK.set_setting(handle, settings_name, tlmc_value)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)

    def set_settings_from_string(self, handle, settings_json):
        rc = TLMC_SDK.set_settings_from_string(handle, settings_json)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)

        # xa_sdk.py  (add inside XASDK class, in the Strings / Settings section)

    def set_connected_product(self, handle, product_name: str) -> None:
        if not product_name or not isinstance(product_name, str):
            raise ValueError("product_name must be a non-empty string")
        rc = TLMC_SDK.set_connected_product(handle, product_name)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)

    def set_connected_product_info(
            self,
            handle,
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
        if not product_name or not isinstance(product_name, str):
            raise ValueError("product_name must be a non-empty string")
        rc = TLMC_SDK.set_connected_product_info(
            handle,
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
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)

    # ---- Status ----

    def get_status_item(self, handle, status_item_id):
        st = [None]
        rc = TLMC_SDK.get_status_item(handle, status_item_id, st)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)
        return st[0]

    def get_status_item_count(self, handle):
        count = [None]
        rc = TLMC_SDK.get_status_item_count(handle, count)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)
        return count[0]

    def get_status_items(self, handle, start_index, number_of_items):
        dest = [None] * number_of_items
        copied = [0]
        rc = TLMC_SDK.get_status_items(handle, start_index, number_of_items, dest, copied)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)
        return dest[:copied[0]]

    # ---- Motion / General ----

    def get_adc_inputs(self, handle, max_wait_in_milliseconds):
        vals = [None]
        rc = TLMC_SDK.get_adc_inputs(handle, vals, max_wait_in_milliseconds)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)
        return vals[0]

    def get_aux_io_port_mode(self, handle, port_number, max_wait_in_milliseconds):
        mode = [None]
        rc = TLMC_SDK.get_aux_io_port_mode(handle, port_number, mode, max_wait_in_milliseconds)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)
        return mode[0]

    def set_aux_io_port_mode(self, handle, port_numbers_mask, new_mode):
        rc = TLMC_SDK.set_aux_io_port_mode(handle, port_numbers_mask, new_mode)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)

    def get_aux_io_software_states(self, handle, max_wait_in_milliseconds):
        st = [None]
        rc = TLMC_SDK.get_aux_io_software_states(handle, st, max_wait_in_milliseconds)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)
        return st[0]

    def set_aux_io_software_states(self, handle, new_state):
        rc = TLMC_SDK.set_aux_io_software_states(handle, new_state)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)

    def get_bow_index(self, handle, max_wait_in_milliseconds):
        idx = [None]
        rc = TLMC_SDK.get_bow_index(handle, idx, max_wait_in_milliseconds)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)
        return idx[0]

    def set_bow_index(self, handle, new_bow_index):
        rc = TLMC_SDK.set_bow_index(handle, new_bow_index)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)

    def get_current_loop_params(self, handle, loop_scenario, max_wait_in_milliseconds):
        params = [None]
        rc = TLMC_SDK.get_current_loop_params(handle, loop_scenario, params, max_wait_in_milliseconds)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)
        return params[0]

    def set_current_loop_params(self, handle, loop_scenario, phase, proportional, integral, integral_limit, integral_dead_band, feed_fwrd):
        rc = TLMC_SDK.set_current_loop_params(handle, loop_scenario, phase, proportional, integral, integral_limit, integral_dead_band, feed_fwrd)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)

    def get_dc_pid_params(self, handle, max_wait_in_milliseconds):
        params = [None]
        rc = TLMC_SDK.get_dc_pid_params(handle, params, max_wait_in_milliseconds)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)
        return params[0]

    def set_dc_pid_params(self, handle, proportional, integral, derivative, integral_limit, filter_control):
        rc = TLMC_SDK.set_dc_pid_params(handle, proportional, integral, derivative, integral_limit, filter_control)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)

    def get_digital_input_states(self, handle, max_wait_in_milliseconds):
        st = [None]
        rc = TLMC_SDK.get_digital_input_states(handle, st, max_wait_in_milliseconds)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)
        return st[0]

    def get_digital_output_params(self, handle, max_wait_in_milliseconds):
        st = [None]
        rc = TLMC_SDK.get_digital_output_states(handle, st, max_wait_in_milliseconds)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)
        return st[0]

    def set_digital_output_params(self, handle, new_output_state):
        rc = TLMC_SDK.set_digital_output_states(handle, new_output_state)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)

    def get_enable_state(self, handle, max_wait_in_milliseconds):
        st = [None]
        rc = TLMC_SDK.get_enable_state(handle, st, max_wait_in_milliseconds)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)
        return st[0]

    def set_enable_state(self, handle, enable_state):
        rc = TLMC_SDK.set_enable_state(handle, enable_state)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)

    def get_encoder_counter(self, handle, max_wait_in_milliseconds):
        val = [None]
        rc = TLMC_SDK.get_encoder_counter(handle, val, max_wait_in_milliseconds)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)
        return val[0]

    def set_encoder_counter(self, handle, new_encoder_counter):
        rc = TLMC_SDK.set_encoder_counter(handle, new_encoder_counter)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)

    def get_general_move_params(self, handle, max_wait_in_milliseconds):
        params = [None]
        rc = TLMC_SDK.get_general_move_params(handle, params, max_wait_in_milliseconds)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)
        return params[0]

    def set_general_move_params(self, handle, backlash_distance):
        rc = TLMC_SDK.set_general_move_params(handle, backlash_distance)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)

    def get_hardware_info(self, handle, max_wait_in_milliseconds):
        info = [None]
        rc = TLMC_SDK.get_hardware_info(handle, info, max_wait_in_milliseconds)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)
        return info[0]

    def get_home_params(self, handle, max_wait_in_milliseconds):
        params = [None]
        rc = TLMC_SDK.get_home_params(handle, params, max_wait_in_milliseconds)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)
        return params[0]

    def set_home_params(self, handle, direction, limit_switch, velocity, offset_distance):
        rc = TLMC_SDK.set_home_params(handle, direction, limit_switch, velocity, offset_distance)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)

    def get_io_configuration_number_of_ports_supported(self, handle):
        ports = [None]
        rc = TLMC_SDK.get_io_configuration_number_of_ports_supported(handle, ports)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)
        return ports[0]

    def get_io_configuration_params(self, handle, port_number, max_wait_in_milliseconds):
        params = [None]
        rc = TLMC_SDK.get_io_configuration_params(handle, port_number, params, max_wait_in_milliseconds)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)
        return params[0]

    def set_io_configuration_params(self, handle, port_number, mode, trigger_out_source):
        rc = TLMC_SDK.set_io_configuration_params(handle, port_number, mode, trigger_out_source)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)

    def get_io_position_trigger_enable_state(self, handle, max_wait_in_milliseconds):
        st = [None]
        rc = TLMC_SDK.get_io_position_trigger_enable_state(handle, st, max_wait_in_milliseconds)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)
        return st[0]

    def set_io_position_trigger_enable_state(self, handle, new_enable_state, max_wait_in_milliseconds):
        rc = TLMC_SDK.set_io_position_trigger_enable_state(handle, new_enable_state, max_wait_in_milliseconds)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)

    def get_io_trigger_params(self, handle, max_wait_in_milliseconds):
        params = [None]
        rc = TLMC_SDK.get_io_trigger_params(handle, params, max_wait_in_milliseconds)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)
        return params[0]

    def set_io_trigger_params(self, handle, *args):
        rc = TLMC_SDK.set_io_trigger_params(handle, *args)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)

    def get_jog_params(self, handle, max_wait_in_milliseconds):
        params = [None]
        rc = TLMC_SDK.get_jog_params(handle, params, max_wait_in_milliseconds)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)
        return params[0]

    def set_jog_params(self, handle, jog_mode, step_size, min_velocity, max_velocity, acceleration, stop_mode):
        rc = TLMC_SDK.set_jog_params(handle, jog_mode, step_size, min_velocity, max_velocity, acceleration, stop_mode)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)

    def get_joystick_params(self, handle, max_wait_in_milliseconds):
        params = [None]
        rc = TLMC_SDK.get_joystick_params(handle, params, max_wait_in_milliseconds)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)
        return params[0]

    def set_joystick_params(self, handle, low_gear_velocity, high_gear_velocity, low_gear_acceleration, high_gear_acceleration, direction_sense):
        rc = TLMC_SDK.set_joystick_params(handle, low_gear_velocity, high_gear_velocity, low_gear_acceleration, high_gear_acceleration, direction_sense)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)

    def get_kcube_io_trigger_params(self, handle, max_wait_in_milliseconds):
        params = [None]
        rc = TLMC_SDK.get_kcube_io_trigger_params(handle, params, max_wait_in_milliseconds)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)
        return params[0]

    def set_kcube_io_trigger_params(self, handle, trigger_one_mode, trigger_one_polarity, trigger_two_mode, trigger_two_polarity):
        rc = TLMC_SDK.set_kcube_io_trigger_params(handle, trigger_one_mode, trigger_one_polarity, trigger_two_mode, trigger_two_polarity)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)

    def get_kcube_mmi_lock_state(self, handle, max_wait_in_milliseconds):
        st = [None]
        rc = TLMC_SDK.get_kcube_mmi_lock_state(handle, st, max_wait_in_milliseconds)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)
        return st[0]

    def set_kcube_mmi_lock_state(self, handle, lock_state):
        rc = TLMC_SDK.set_kcube_mmi_lock_state(handle, lock_state)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)

    def get_kcube_mmi_params(self, handle, max_wait_in_milliseconds):
        params = [None]
        rc = TLMC_SDK.get_kcube_mmi_params(handle, params, max_wait_in_milliseconds)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)
        return params[0]

    def set_kcube_mmi_params(self, handle, joystick_mode, joystick_velocity, joystick_acceleration,
                             joystick_direction_sense, position_one, position_two,
                             display_brightness, display_timeout, display_dim_level,
                             position_three, joystick_sensitivity):
        rc = TLMC_SDK.set_kcube_mmi_params(handle, joystick_mode, joystick_velocity, joystick_acceleration,
                                           joystick_direction_sense, position_one, position_two,
                                           display_brightness, display_timeout, display_dim_level,
                                           position_three, joystick_sensitivity)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)

    def get_kcube_position_trigger_params(self, handle, max_wait_in_milliseconds):
        params = [None]
        rc = TLMC_SDK.get_kcube_position_trigger_params(handle, params, max_wait_in_milliseconds)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)
        return params[0]

    def set_kcube_position_trigger_params(self, handle, *args):
        rc = TLMC_SDK.set_kcube_position_trigger_params(handle, *args)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)

    def get_lcd_display_params(self, handle, max_wait_in_milliseconds):
        params = [None]
        rc = TLMC_SDK.get_lcd_display_params(handle, params, max_wait_in_milliseconds)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)
        return params[0]

    def set_lcd_display_params(self, handle, knob_sensitivity, display_brightness, display_timeout, display_dim_level):
        rc = TLMC_SDK.set_lcd_display_params(handle, knob_sensitivity, display_brightness, display_timeout, display_dim_level)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)

    def get_lcd_move_params(self, handle, max_wait_in_milliseconds):
        params = [None]
        rc = TLMC_SDK.get_lcd_move_params(handle, params, max_wait_in_milliseconds)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)
        return params[0]

    def set_lcd_move_params(self, handle, knob_mode, jog_step_size, acceleration, max_velocity, jog_stop_mode, preset_position):
        rc = TLMC_SDK.set_lcd_move_params(handle, knob_mode, jog_step_size, acceleration, max_velocity, jog_stop_mode, preset_position)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)

    def get_limit_switch_params(self, handle, max_wait_in_milliseconds):
        params = [None]
        rc = TLMC_SDK.get_limit_switch_params(handle, params, max_wait_in_milliseconds)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)
        return params[0]

    def set_limit_switch_params(self, handle, clockwise_limit_mode, counter_clockwise_mode, clockwise_soft_limit, counter_clockwise_soft_limit, soft_limit_operating_mode):
        rc = TLMC_SDK.set_limit_switch_params(handle, clockwise_limit_mode, counter_clockwise_mode, clockwise_soft_limit, counter_clockwise_soft_limit, soft_limit_operating_mode)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)

    def get_motor_output_params(self, handle, max_wait_in_milliseconds):
        params = [None]
        rc = TLMC_SDK.get_motor_output_params(handle, params, max_wait_in_milliseconds)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)
        return params[0]

    def set_motor_output_params(self, handle, current_limit, energy_limit, motor_limit, motor_bias):
        rc = TLMC_SDK.set_motor_output_params(handle, current_limit, energy_limit, motor_limit, motor_bias)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)

    def get_move_absolute_params(self, handle, max_wait_in_milliseconds):
        params = [None]
        rc = TLMC_SDK.get_move_absolute_params(handle, params, max_wait_in_milliseconds)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)
        return params[0]

    def set_move_absolute_params(self, handle, absolute_position):
        rc = TLMC_SDK.set_move_absolute_params(handle, absolute_position)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)

    def get_move_relative_params(self, handle, max_wait_in_milliseconds):
        params = [None]
        rc = TLMC_SDK.get_move_relative_params(handle, params, max_wait_in_milliseconds)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)
        return params[0]

    def set_move_relative_params(self, handle, relative_distance):
        rc = TLMC_SDK.set_move_relative_params(handle, relative_distance)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)

    def get_position_counter(self, handle, max_wait_in_milliseconds):
        val = [None]
        rc = TLMC_SDK.get_position_counter(handle, val, max_wait_in_milliseconds)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)
        return val[0]

    def set_position_counter(self, handle, new_position_counter):
        rc = TLMC_SDK.set_position_counter(handle, new_position_counter)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)

    def get_position_loop_params(self, handle, position_loop_scenario, max_wait_in_milliseconds):
        params = [None]
        rc = TLMC_SDK.get_position_loop_params(handle, position_loop_scenario, params, max_wait_in_milliseconds)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)
        return params[0]

    def set_position_loop_params(self, handle, position_loop_scenario, proportional, integral, integral_limit, derivative, servo_cycles, scale, velocity_feed_fwrd, acceleration_feed_fwrd, error_limit):
        rc = TLMC_SDK.set_position_loop_params(handle, position_loop_scenario, proportional, integral, integral_limit, derivative, servo_cycles, scale, velocity_feed_fwrd, acceleration_feed_fwrd, error_limit)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)

    def get_power_params(self, handle, max_wait_in_milliseconds):
        params = [None]
        rc = TLMC_SDK.get_power_params(handle, params, max_wait_in_milliseconds)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)
        return params[0]

    def set_power_params(self, handle, rest_factor, move_factor):
        rc = TLMC_SDK.set_power_params(handle, rest_factor, move_factor)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)

    def get_profiled_mode_params(self, handle, max_wait_in_milliseconds):
        params = [None]
        rc = TLMC_SDK.get_profiled_mode_params(handle, params, max_wait_in_milliseconds)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)
        return params[0]

    def set_profiled_mode_params(self, handle, mode, jerk):
        rc = TLMC_SDK.set_profiled_mode_params(handle, mode, jerk)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)

    # PZ

    def pz_get_max_output_voltage_params(self, handle, max_wait_in_milliseconds):
        params = [None]
        rc = TLMC_SDK.pz_get_max_output_voltage_params(handle, params, max_wait_in_milliseconds)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)
        return params[0]

    def pz_set_max_output_voltage(self, handle, max_output_voltage):
        rc = TLMC_SDK.pz_set_max_output_voltage(handle, max_output_voltage)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)

    def pz_get_max_travel(self, handle, max_wait_in_milliseconds):
        val = [None]
        rc = TLMC_SDK.pz_get_max_travel(handle, val, max_wait_in_milliseconds)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)
        return val[0]

    def pz_get_output_voltage(self, handle, max_wait_in_milliseconds):
        val = [None]
        rc = TLMC_SDK.pz_get_output_voltage(handle, val, max_wait_in_milliseconds)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)
        return val[0]

    def pz_set_output_voltage(self, handle, new_output_voltage):
        rc = TLMC_SDK.pz_set_output_voltage(handle, new_output_voltage)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)

    def pz_get_output_voltage_control_source_params(self, handle, max_wait_in_milliseconds):
        params = [None]
        rc = TLMC_SDK.pz_get_output_voltage_control_source_params(handle, params, max_wait_in_milliseconds)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)
        return params[0]

    def pz_set_output_voltage_control_source_params(self, handle, source):
        rc = TLMC_SDK.pz_set_output_voltage_control_source_params(handle, source)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)

    def pz_set_output_waveform_lookup_table_sample(self, handle, index, voltage):
        rc = TLMC_SDK.pz_set_output_waveform_lookup_table_sample(handle, index, voltage)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)

    def pz_get_output_waveform_params(self, handle, max_wait_in_milliseconds):
        params = [None]
        rc = TLMC_SDK.pz_get_output_waveform_params(handle, params, max_wait_in_milliseconds)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)
        return params[0]

    def pz_set_output_waveform_params(self, handle, *args):
        rc = TLMC_SDK.pz_set_output_waveform_params(handle, *args)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)

    def pz_start_output_waveform(self, handle):
        rc = TLMC_SDK.pz_start_output_waveform(handle)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)

    def pz_stop_output_waveform(self, handle):
        rc = TLMC_SDK.pz_stop_output_waveform(handle)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)

    def pz_get_position(self, handle, max_wait_in_milliseconds):
        pos = [None]
        rc = TLMC_SDK.pz_get_position(handle, pos, max_wait_in_milliseconds)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)
        return pos[0]

    def pz_set_position(self, handle, new_position):
        rc = TLMC_SDK.pz_set_position(handle, new_position)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)

    def pz_get_position_control_mode(self, handle, max_wait_in_milliseconds):
        cm = [None]
        rc = TLMC_SDK.pz_get_position_control_mode(handle, cm, max_wait_in_milliseconds)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)
        return cm[0]

    def pz_set_position_control_mode(self, handle, new_control_mode):
        rc = TLMC_SDK.pz_set_position_control_mode(handle, new_control_mode)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)

    def pz_get_position_loop_params(self, handle, max_wait_in_milliseconds):
        params = [None]
        rc = TLMC_SDK.pz_get_position_loop_params(handle, params, max_wait_in_milliseconds)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)
        return params[0]

    def pz_set_position_loop_params(self, handle, proportional, integral):
        rc = TLMC_SDK.pz_set_position_loop_params(handle, proportional, integral)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)

    def pz_get_slew_rate_params(self, handle, max_wait_in_milliseconds):
        params = [None]
        rc = TLMC_SDK.pz_get_slew_rate_params(handle, params, max_wait_in_milliseconds)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)
        return params[0]

    def pz_set_slew_rate_params(self, handle, open_slew_rate, closed_slew_rate):
        rc = TLMC_SDK.pz_set_slew_rate_params(handle, open_slew_rate, closed_slew_rate)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)

    def pz_get_status(self, handle, max_wait_in_milliseconds):
        st = [None]
        rc = TLMC_SDK.pz_get_status(handle, st, max_wait_in_milliseconds)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)
        return st[0]

    def pz_get_status_bits(self, handle, max_wait_in_milliseconds):
        bits = [None]
        rc = TLMC_SDK.pz_get_status_bits(handle, bits, max_wait_in_milliseconds)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)
        return bits[0]

    def pz_set_zero(self, handle, max_wait_in_milliseconds):
        rc = TLMC_SDK.pz_set_zero(handle, max_wait_in_milliseconds)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)

    # Rack / Stage / Universal

    def rack_identify(self, handle, channel):
        rc = TLMC_SDK.rack_identify(handle, channel)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)

    def get_rack_bay_occupied_state(self, handle, bay_number, max_wait_in_milliseconds):
        st = [None]
        rc = TLMC_SDK.get_rack_bay_occupied_state(handle, bay_number, st, max_wait_in_milliseconds)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)
        return st[0]

    def get_stage_axis_params(self, handle, max_wait_in_milliseconds):
        params = [None]
        rc = TLMC_SDK.get_stage_axis_params(handle, params, max_wait_in_milliseconds)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)
        return params[0]

    def set_stage_axis_params(self, handle, *args):
        rc = TLMC_SDK.set_stage_axis_params(handle, *args)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)

    def get_stepper_loop_params(self, handle, max_wait_in_milliseconds):
        params = [None]
        rc = TLMC_SDK.get_stepper_loop_params(handle, params, max_wait_in_milliseconds)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)
        return params[0]

    def set_stepper_loop_params(self, handle, *args):
        rc = TLMC_SDK.set_stepper_loop_params(handle, *args)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)

    def get_stepper_status(self, handle, max_wait_in_milliseconds):
        st = [None]
        rc = TLMC_SDK.get_stepper_status(handle, st, max_wait_in_milliseconds)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)
        return st[0]

    def get_track_settle_params(self, handle, max_wait_in_milliseconds):
        params = [None]
        rc = TLMC_SDK.get_track_settle_params(handle, params, max_wait_in_milliseconds)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)
        return params[0]

    def set_track_settle_params(self, handle, settle_time, settle_window, track_window):
        rc = TLMC_SDK.set_track_settle_params(handle, settle_time, settle_window, track_window)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)

    def get_trigger_params_for_dc_brushless(self, handle, max_wait_in_milliseconds):
        params = [None]
        rc = TLMC_SDK.get_trigger_params_for_dc_brushless(handle, params, max_wait_in_milliseconds)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)
        return params[0]

    def set_trigger_params_for_dc_brushless(self, handle, modes):
        rc = TLMC_SDK.set_trigger_params_for_dc_brushless(handle, modes)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)

    def get_trigger_params_for_stepper(self, handle, max_wait_in_milliseconds):
        params = [None]
        rc = TLMC_SDK.get_trigger_params_for_stepper(handle, params, max_wait_in_milliseconds)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)
        return params[0]

    def set_trigger_params_for_stepper(self, handle, modes):
        rc = TLMC_SDK.set_trigger_params_for_stepper(handle, modes)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)

    def get_universal_status(self, handle, max_wait_in_milliseconds):
        st = [None]
        rc = TLMC_SDK.get_universal_status(handle, st, max_wait_in_milliseconds)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)
        return st[0]

    def get_universal_status_bits(self, handle, max_wait_in_milliseconds):
        bits = [None]
        rc = TLMC_SDK.get_universal_status_bits(handle, bits, max_wait_in_milliseconds)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)
        return bits[0]

    def get_velocity_params(self, handle, max_wait_in_milliseconds):
        params = [None]
        rc = TLMC_SDK.get_velocity_params(handle, params, max_wait_in_milliseconds)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)
        return params[0]

    def set_velocity_params(self, handle, min_velocity, acceleration, max_velocity):
        rc = TLMC_SDK.set_velocity_params(handle, min_velocity, acceleration, max_velocity)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)

    # ---- Motion commands ----

    def home(self, handle, wait_timeout):
        rc = TLMC_SDK.home(handle, wait_timeout)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)

    def identify(self, handle):
        rc = TLMC_SDK.identify(handle)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)

    def move_absolute(self, handle, move_mode, position, max_wait_in_milliseconds):
        rc = TLMC_SDK.move_absolute(handle, move_mode, position, max_wait_in_milliseconds)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)

    def move_continuous(self, handle, direction, max_wait_in_milliseconds):
        rc = TLMC_SDK.move_continuous(handle, direction, max_wait_in_milliseconds)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)

    def move_jog(self, handle, direction, max_wait_in_milliseconds):
        rc = TLMC_SDK.move_jog(handle, direction, max_wait_in_milliseconds)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)

    def move_relative(self, handle, move_mode, step_size, max_wait_in_milliseconds):
        rc = TLMC_SDK.move_relative(handle, move_mode, step_size, max_wait_in_milliseconds)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)

    def stop(self, handle, stop_mode, max_wait_in_milliseconds):
        rc = TLMC_SDK.stop(handle, stop_mode, max_wait_in_milliseconds)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)

    # ---- Misc ----

    def persist_params(self, handle, parameter_group_id):
        rc = TLMC_SDK.persist_params(handle, parameter_group_id)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)

    def restore_to_factory_defaults(self, handle):
        rc = TLMC_SDK.restore_factory_defaults(handle)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)

    def get_rich_response(self, handle):
        rr = [None]
        rc = TLMC_SDK.get_rich_response(handle, rr)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)
        return rr[0]

    def set_end_of_message_mode(self, handle, mode):
        rc = TLMC_SDK.set_end_of_move_messages_mode(handle, mode)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)

    def set_status_mode(self, handle, operating_mode):
        rc = TLMC_SDK.set_status_mode(handle, operating_mode)
        if rc != 0:
            raise XAErrorFactory.convert_return(rc)