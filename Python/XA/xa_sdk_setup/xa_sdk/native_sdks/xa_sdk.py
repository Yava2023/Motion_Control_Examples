from ctypes import c_uint32
from xa_sdk.native_sdks.tlmc_core_interface import NativeSDKInterface
from xa_sdk.native_sdks.tlmc_core import TLMC_SDK
from xa_sdk.shared.xa_error_factory import XAErrorFactory

# The SDK for XA. This implements the native interface and contains the calls to the static functions


class XASDK(NativeSDKInterface):
    """
    Main wrapper class. Used to call methods that are not accesible to devices.
    """

    def add_user_message_to_log(self, user_message):
        message_return = TLMC_SDK.add_user_message_to_log(user_message)
        if message_return != 0:
            ex = XAErrorFactory.convert_return(
                message_return)
            raise ex

    def close(self, handle):
        close_return = TLMC_SDK.close(handle)
        if close_return != 0:
            ex = XAErrorFactory.convert_return(
                close_return)
            raise ex

    def convert_from_device_units_to_physical(self, handle, TLMC_scale_type, device_value):
        physical_value = [0]
        converter_return = TLMC_SDK.convert_from_device_units_to_physical(
            handle, TLMC_scale_type, device_value, physical_value)
        if converter_return != 0:
            ex = XAErrorFactory.convert_return(
                converter_return)
            raise ex
        return physical_value[0]

    def convert_from_physical_to_device(self, handle, TLMC_scale_type, TLMC_unit_type, physical_value):
        device_value = [0]
        converter_return = TLMC_SDK.convert_from_physical_to_device(
            handle, TLMC_scale_type, TLMC_unit_type, physical_value, device_value)
        if converter_return != 0:
            ex = XAErrorFactory.convert_return(
                converter_return)
            raise ex
        return device_value[0]

    @staticmethod
    def create_simulation(description: dict):
        """
        Creates an instance of the XA device simulator. 
        
        Description is a python dictionary that should contatain a JSON string with the properties for the device. 

        EX: {"PartNumber":"KDC101","SerialNumber":"27265111","ActuatorType":"Z825"}

            {"PartNumber": "BBD303", "SerialNumber": "103000123", "Channels": [
            {"BayNumber": "1", "SerialNumber": "104000124", "ActuatorType": "DDR100"},
            {"BayNumber": "2", "SerialNumber": "104000125", "ActuatorType": "DDR100"},
            {"BayNumber": "3", "SerialNumber": "104000126", "ActuatorType": "DDR100"}]}
        """
        simulation_return = TLMC_SDK.create_simulation(description)
        if simulation_return != 0:
            ex = XAErrorFactory.convert_return(
                simulation_return)
            raise ex

    def disconnect(self, handle):
        disconnect_return = TLMC_SDK.disconnect(handle)
        if (disconnect_return != 0):
            ex = XAErrorFactory.convert_return(
                disconnect_return)
            raise ex

    def get_adc_inputs(self, handle, max_wait_in_milliseconds):
        adc_params = [None]
        adc_return = TLMC_SDK.get_adc_inputs(
            handle, adc_params, max_wait_in_milliseconds)
        if adc_params != 0:
            ex = XAErrorFactory.convert_return(adc_return)
            raise ex
        return adc_params[0]

    def get_analog_monitor_configuration_params(self, handle, monitor_number, max_wait_in_milliseconds):
        configuration_params = [None]
        params_return = TLMC_SDK.get_analog_monitor_configuration_params(
            handle, monitor_number, configuration_params, max_wait_in_milliseconds)
        if params_return != 0:
            ex = XAErrorFactory.convert_return(
                params_return)
            raise ex
        return configuration_params[0]

    def get_api_version(self):
        api_version = [None]
        api_return = TLMC_SDK.get_api_version(api_version)
        if api_return != 0:
            ex = XAErrorFactory.convert_return(api_return)
            raise ex
        return api_version[0]

    def get_aux_io_port_mode(self, handle, port_number, max_wait_in_milliseconds):
        port_mode = [None]
        mode_return = TLMC_SDK.get_aux_io_port_mode(
            handle, port_number, port_mode, max_wait_in_milliseconds)
        if mode_return != 0:
            ex = XAErrorFactory.convert_return(mode_return)
            raise ex
        return port_mode[0]

    def get_aux_io_software_states(self, handle, max_wait_in_milliseconds):
        software_states = [None]
        state_return = TLMC_SDK.get_aux_io_software_states(
            handle, software_states, max_wait_in_milliseconds)
        if state_return != 0:
            ex = XAErrorFactory.convert_return(
                state_return)
            raise ex
        return software_states[0]

    def get_bow_index(self, handle, index_val , max_wait_in_milliseconds):
        bow_index = [None]
        index_return = TLMC_SDK.get_bow_index(
            handle, bow_index, index_val, max_wait_in_milliseconds)
        if index_return != 0:
            ex = XAErrorFactory.convert_return(
                index_return)
            raise ex
        return bow_index[0]

    def get_connected_product(self, handle):
        connected_product = [None]
        product_buffer = [0] * 6
        product_return = TLMC_SDK.get_connected_product(
            handle, connected_product, product_buffer)
        if product_return != 0:
            ex = XAErrorFactory.convert_return(
                product_return)
            raise ex
        return connected_product[0]

    def get_connected_product_info(self, handle):
        product_info = [None]
        product_return = TLMC_SDK.get_connected_product_info(
            handle, product_info)
        if product_return != 0:
            ex = XAErrorFactory.convert_return(
                product_return)
            raise ex
        return product_info[0]

    def get_connected_products_supported(self, handle):
        connected_products = [None]
        product_return = TLMC_SDK.get_connected_products_supported(
            handle, connected_products)
        if product_return != 0:
            ex = XAErrorFactory.convert_return(
                product_return)
            raise ex
        return connected_products[0]

    def get_current_loop_params(self, handle, loop_scenario, max_wait_in_milliseconds):
        loop_params = [None]
        loop_return = TLMC_SDK.get_current_loop_params(
            handle, loop_scenario, loop_params, max_wait_in_milliseconds)
        if loop_return != 0:
            ex = XAErrorFactory.convert_return(loop_return)
            raise ex
        return loop_params[0]

    def get_dc_pid_params(self, handle, max_wait_in_milliseconds):
        pid_params = [None]
        pid_return = TLMC_SDK.get_dc_pid_params(
            handle, pid_params, max_wait_in_milliseconds)
        if pid_return != 0:
            ex = XAErrorFactory.convert_return(pid_return)
            raise ex
        return pid_params[0]

    def get_device_info(self, handle, max_wait_in_milliseconds):
        device_info = [None]
        info_return = TLMC_SDK.get_device_info(
            handle, device_info, max_wait_in_milliseconds)
        if info_return != 0:
            ex = XAErrorFactory.convert_return(info_return)
            raise ex
        return device_info[0]

    def get_device_list_item_count(self):
        count = [None]
        list_return = TLMC_SDK.get_device_list_item_count(count)
        if list_return != 0:
            ex = XAErrorFactory.convert_return(list_return)
            raise ex
        return count[0]

    def get_device_list_items(self, source_start_index, number_of_items, number_of_items_copied):
        TLMC_device_info = [0]
        list_return = TLMC_SDK.get_device_list_items(
            source_start_index, number_of_items, TLMC_device_info, number_of_items_copied)
        if list_return != 0:
            ex = XAErrorFactory.convert_return(list_return)
            raise ex
        return TLMC_device_info

    def get_digital_input_states(self, handle, max_wait_in_milliseconds):
        input_state = [None]
        digital_return = TLMC_SDK.get_digital_output_params(
            handle, input_state, max_wait_in_milliseconds)
        if digital_return != 0:
            ex = XAErrorFactory.convert_return(
                digital_return)
            raise ex
        return input_state[0]

    def get_digital_output_params(self, handle, max_wait_in_milliseconds):
        output_params = [None]
        digital_return = TLMC_SDK.get_digital_output_params(
            handle, output_params, max_wait_in_milliseconds)
        if digital_return != 0:
            ex = XAErrorFactory.convert_return(
                digital_return)
            raise ex
        return output_params[0]

    def get_enable_state(self, handle, max_wait_in_milliseconds):
        channel_enable_state = [None]
        enable_return = TLMC_SDK.get_enable_state(
            handle, channel_enable_state, max_wait_in_milliseconds)
        if enable_return != 0:
            ex = XAErrorFactory.convert_return(
                enable_return)
            raise ex
        return channel_enable_state[0]

    def get_encoder_counter(self, handle, max_wait_in_milliseconds):
        encoder_counter = [None]
        encoder_return = TLMC_SDK.get_encoder_counter(
            handle, encoder_counter, max_wait_in_milliseconds)
        if encoder_return != 0:
            ex = XAErrorFactory.convert_return(
                encoder_return)
            raise ex
        return encoder_counter[0]

    def get_general_move_params(self, handle, max_wait_in_milliseconds):
        general_move_params = [None]
        settings_return = TLMC_SDK.get_general_move_params(
            handle, general_move_params, max_wait_in_milliseconds)
        if settings_return != 0:
            ex = XAErrorFactory.convert_return(
                settings_return)
            raise ex
        return general_move_params[0]

    def get_hardware_info(self, handle, max_wait_in_milliseconds):
        hardware_info = [None]
        info_return = TLMC_SDK.get_hardware_info(
            handle, hardware_info, max_wait_in_milliseconds)
        if info_return != 0:
            ex = XAErrorFactory.convert_return(info_return)
            raise ex
        return hardware_info[0]

    def get_home_params(self, handle, max_wait_in_milliseconds):
        home_params = [None]
        home_params_return = TLMC_SDK.get_home_params(
            handle, home_params, max_wait_in_milliseconds)
        if home_params_return != 0:
            ex = XAErrorFactory.convert_return(
                home_params_return)
            raise ex
        return home_params[0]

    def get_io_configuration_number_of_ports_supported(self, handle):
        number_of_ports = 0
        ports_return = TLMC_SDK.get_io_configuration_number_of_ports_supported(
            handle, number_of_ports)
        if ports_return != 0:
            ex = XAErrorFactory.convert_return(
                ports_return)
            raise ex
        return number_of_ports

    def get_io_configuration_params(self, handle, port_number, max_wait_in_milliseconds):
        configuration_params = [None]
        params_return = TLMC_SDK.get_io_configuration_params(
            handle, port_number, configuration_params, max_wait_in_milliseconds)
        if params_return != 0:
            ex = XAErrorFactory.convert_return(
                params_return)
            raise ex
        return configuration_params[0]

    def get_io_position_trigger_enable_state(self, handle, max_wait_in_milliseconds):
        enable_state = [None]
        enable_state_return = TLMC_SDK.get_io_position_trigger_enable_state(
            handle, enable_state, max_wait_in_milliseconds)
        if enable_state_return != 0:
            ex = XAErrorFactory.convert_return(
                enable_state_return)
            raise ex
        return enable_state[0]

    def get_io_trigger_params(self, handle, max_wait_in_milliseconds):
        io_trigger_params = [None]
        io_trigger_return = TLMC_SDK.get_io_trigger_params(
            handle, io_trigger_params, max_wait_in_milliseconds)
        if io_trigger_return != 0:
            ex = XAErrorFactory.convert_return(
                io_trigger_return)
            raise ex
        return io_trigger_params[0]

    def get_joystick_params(self, handle, max_wait_in_milliseconds):
        joystick_params = [None]
        joystick_return = TLMC_SDK.get_joystick_params(
            handle, joystick_params, max_wait_in_milliseconds)
        if joystick_return != 0:
            ex = XAErrorFactory.convert_return(
                joystick_return)
            raise ex
        return joystick_params[0]

    def get_kcube_io_trigger_params(self, handle, max_wait_in_milliseconds):
        kcube_io_params = [None]
        kcube_trigger_return = TLMC_SDK.get_kcube_io_trigger_params(
            handle, kcube_io_params, max_wait_in_milliseconds)
        if kcube_trigger_return != 0:
            ex = XAErrorFactory.convert_return(
                kcube_io_params)
            raise ex
        return kcube_io_params[0]

    def get_kcube_mmi_lock_state(self, handle, max_wait_in_milliseconds):
        lock_state = [None]
        lock_state_return = TLMC_SDK.get_kcube_mmi_lock_state(
            handle, lock_state, max_wait_in_milliseconds)
        if lock_state_return != 0:
            ex = XAErrorFactory.convert_return(
                lock_state_return)
            raise ex
        return lock_state[0]

    def get_kcube_mmi_params(self, handle, max_wait_in_milliseconds):
        kcube_mmi_params = [None]
        mmi_params_return = TLMC_SDK.get_kcube_mmi_params(
            handle, kcube_mmi_params, max_wait_in_milliseconds)
        if mmi_params_return != 0:
            ex = XAErrorFactory.convert_return(
                mmi_params_return)
            raise ex
        return kcube_mmi_params[0]

    def get_kcube_position_trigger_params(self, handle, max_wait_in_milliseconds):
        kcube_trigger_params = [None]
        kcube_trigger_return = TLMC_SDK.get_kcube_position_trigger_params(
            handle, kcube_trigger_params, max_wait_in_milliseconds)
        if kcube_trigger_return != 0:
            ex = XAErrorFactory.convert_return(
                kcube_trigger_return)
            raise ex
        return kcube_trigger_params[0]

    def get_lcd_display_params(self, handle, max_wait_in_milliseconds):
        lcd_display_params = [None]
        lcd_display_return = TLMC_SDK.get_lcd_display_params(
            handle, lcd_display_params, max_wait_in_milliseconds)
        if lcd_display_return != 0:
            ex = XAErrorFactory.convert_return(
                lcd_display_return)
            raise ex
        return lcd_display_params[0]

    def get_lcd_move_params(self, handle, max_wait_in_milliseconds):
        lcd_params = [None]
        lcd_move_return = TLMC_SDK.get_lcd_move_params(
            handle, lcd_params, max_wait_in_milliseconds)
        if lcd_move_return != 0:
            ex = XAErrorFactory.convert_return(
                lcd_move_return)
            raise ex
        return lcd_move_return[0]

    def get_limit_switch_params(self, handle, max_wait_in_milliseconds):
        limit_switch_params = [None]
        settings_return = TLMC_SDK.get_limit_switch_params(
            handle, limit_switch_params, max_wait_in_milliseconds)
        if settings_return != 0:
            ex = XAErrorFactory.convert_return(
                settings_return)
            raise ex
        return limit_switch_params[0]

    def get_motor_output_params(self, handle, max_wait_in_milliseconds):
        motor_output_params = [None]
        output_return = TLMC_SDK.get_motor_output_params(
            handle, motor_output_params, max_wait_in_milliseconds)
        if output_return != 0:
            ex = XAErrorFactory.convert_return(
                output_return)
            raise ex
        return motor_output_params[0]

    def get_move_absolute_params(self, handle, max_wait_in_milliseconds):
        move_absolute_params = [None]
        settings_return = TLMC_SDK.get_move_absolute_params(
            handle, move_absolute_params, max_wait_in_milliseconds)
        if settings_return != 0:
            ex = XAErrorFactory.convert_return(
                settings_return)
            raise ex
        return move_absolute_params[0]

    def get_move_jog_params(self, handle, max_wait_in_milliseconds):
        jog_params = [None]
        settings_return = TLMC_SDK.get_jog_params(
            handle, jog_params, max_wait_in_milliseconds)
        if settings_return != 0:
            ex = XAErrorFactory.convert_return(
                settings_return)
            raise ex
        return jog_params[0]

    def get_move_relative_params(self, handle, max_wait_in_milliseconds):
        move_relative_params = [None]
        get_params_return = TLMC_SDK.get_move_relative_params(
            handle, move_relative_params, max_wait_in_milliseconds)
        if get_params_return != 0:
            ex = XAErrorFactory.convert_return(
                get_params_return)
            raise ex
        return move_relative_params[0]

    def get_position_counter(self, handle, max_wait_in_milliseconds):
        position_counter = [None]
        counter_return = TLMC_SDK.get_position_counter(
            handle, position_counter, max_wait_in_milliseconds)
        if counter_return != 0:
            ex = XAErrorFactory.convert_return(
                counter_return)
            raise ex
        return position_counter[0]

    def get_position_loop_params(self, handle, position_loop_scenario, max_wait_in_milliseconds):
        position_loop_params = [None]
        loop_return = TLMC_SDK.get_position_loop_params(
            handle, position_loop_scenario, position_loop_params, max_wait_in_milliseconds)
        if loop_return != 0:
            ex = XAErrorFactory.convert_return(loop_return)
            raise ex
        return position_loop_params[0]

    def get_power_params(self, handle, max_wait_in_milliseconds):
        power_params = [None]
        power_return = TLMC_SDK.get_power_params(
            handle, power_params, max_wait_in_milliseconds)
        if power_return != 0:
            ex = XAErrorFactory.convert_return(
                power_return)
            raise ex
        return power_params[0]

    def get_profiled_mode_params(self, handle, max_wait_in_milliseconds):
        profiled_params = [None]
        profiled_return = TLMC_SDK.get_profiled_mode_params(
            handle, profiled_params, max_wait_in_milliseconds)
        if profiled_return != 0:
            ex = XAErrorFactory.convert_return(
                profiled_return)
            raise ex
        return profiled_params[0]

    def get_rack_bay_occupied_state(self, handle, bay_number, max_wait_in_milliseconds):
        occupied_state = [None]
        occupied_return = TLMC_SDK.get_rack_bay_occupied_state(
            handle, bay_number, occupied_state, max_wait_in_milliseconds)
        if occupied_return != 0:
            ex = XAErrorFactory.convert_return(occupied_return)
            raise ex
        return occupied_state[0]

    def get_rich_response(self, handle):
        rich_response = [None]
        response_return = TLMC_SDK.get_rich_response(handle, rich_response)
        if response_return != 0:
            ex = XAErrorFactory.convert_return(
                response_return)
            raise ex
        return rich_response[0]

    def get_setting(self, handle, settings_name, max_wait_in_milliseconds):
        TLMC_setting = [None]
        settings_return = TLMC_SDK.get_setting(
            handle, settings_name, TLMC_setting, max_wait_in_milliseconds)
        if settings_return != 0:
            ex = XAErrorFactory.convert_return(
                settings_return)
            raise ex
        return TLMC_setting[0]

    def get_setting_count(self, handle):
        count = [None]
        settings_return = TLMC_SDK.get_setting_count(handle, count)
        if settings_return != 0:
            ex = XAErrorFactory.convert_return(
                settings_return)
            raise ex
        return count[0]

    def get_setting_discrete_values(self, handle, buffer, buffer_length, result_length):
        settings_name = [None]
        settings_return = TLMC_SDK.get_setting_discrete_values(
            handle, settings_name, buffer, buffer_length, result_length)
        if settings_return != 0:
            ex = XAErrorFactory.convert_return
            raise ex
        return settings_name[0]

    def get_settings(self, handle, source_start_index, number_of_items, number_of_items_copied):
        TLMC_setting = [0] * 47
        settings_return = TLMC_SDK.get_settings(
            handle, source_start_index, number_of_items, TLMC_setting, number_of_items_copied)
        if settings_return != 0:
            ex = XAErrorFactory.convert_return(
                settings_return)
            raise ex
        return TLMC_setting

    def get_settings_as_string(self, handle, buffer, buffer_length, pResult_length, TLMC_setting_string_format, include_read_only_items):
        buffer = [None]
        settings_return = TLMC_SDK.get_settings_as_string(
            handle, buffer, buffer_length, pResult_length, TLMC_setting_string_format, include_read_only_items)
        if settings_return != 0:
            ex = XAErrorFactory.convert_return(
                settings_return)
            raise ex
        return buffer[0]

    def get_status_item(self, handle, status_item_id):
        status_item = [None]
        status_return = TLMC_SDK.get_status_item(
            handle, status_item_id, status_item)
        if status_return != 0:
            ex = XAErrorFactory.convert_return(
                status_return)
            raise ex
        return status_item[0]

    def get_status_item_count(self, handle):
        count = [None]
        status_return = TLMC_SDK.get_status_item_count(handle, count)
        if status_return != 0:
            ex = XAErrorFactory.convert_return(
                status_return)
            raise ex
        return count[0]

    def get_status_items(self, handle, start_index, number_of_items,
                         number_of_items_copied):
        status_items = [0] * 27
        status_return = TLMC_SDK.get_status_items(handle, start_index, number_of_items,
                                                  status_items, number_of_items_copied)
        if status_return != 0:
            ex = XAErrorFactory.convert_return(
                status_return)
            raise ex
        return status_items

    def get_stage_axis_params(self, handle, max_wait_in_milliseconds):
        stage_axis_params = [None]
        stage_axis_return = TLMC_SDK.get_stage_axis_params(
            handle, stage_axis_params, max_wait_in_milliseconds)
        if stage_axis_return != 0:
            ex = XAErrorFactory.convert_return(
                stage_axis_return)
            raise ex
        return stage_axis_params[0]

    def get_stepper_loop_params(self, handle, max_wait_in_milliseconds):
        stepper_loop_params = [None]
        loop_return = TLMC_SDK.get_stepper_loop_params(
            handle, stepper_loop_params, max_wait_in_milliseconds)
        if loop_return != 0:
            ex = XAErrorFactory.convert_return(loop_return)
            raise ex
        return stepper_loop_params[0]

    def get_stepper_status(self, handle, max_wait_in_milliseconds):
        stepper_status = [None]
        status_return = TLMC_SDK.get_stepper_status(
            handle, stepper_status, max_wait_in_milliseconds)
        if status_return != 0:
            ex = XAErrorFactory.convert_return(
                status_return)
            raise ex
        return stepper_status[0]

    def get_track_settle_params(self, handle, max_wait_in_milliseconds):
        track_params = [None]
        track_return = TLMC_SDK.get_track_settle_params(
            handle, track_params, max_wait_in_milliseconds)
        if track_return != 0:
            ex = XAErrorFactory.convert_return(
                track_return)
            raise ex
        return track_params[0]

    def get_trigger_params_for_dc_brushless(self, handle, max_wait_in_milliseconds):
        trigger_params = [None]
        trigger_return = TLMC_SDK.get_trigger_params_for_dc_brushless(
            handle, trigger_params, max_wait_in_milliseconds)
        if trigger_return != 0:
            ex = XAErrorFactory.convert_return(
                trigger_return)
            raise ex
        return trigger_params[0]

    def get_trigger_params_for_stepper(self, handle, max_wait_in_milliseconds):
        trigger_params = [None]
        trigger_return = TLMC_SDK.get_trigger_params_for_stepper(
            handle, trigger_params, max_wait_in_milliseconds)
        if trigger_return != 0:
            ex = XAErrorFactory.convert_return(
                trigger_return)
            raise ex
        return trigger_params[0]

    def get_universal_status(self, handle, max_wait_in_milliseconds):
        universal_status = [None]
        status_return = TLMC_SDK.get_universal_status(
            handle, universal_status, max_wait_in_milliseconds)
        if status_return != 0:
            ex = XAErrorFactory.convert_return(
                status_return)
            raise ex
        return universal_status[0]

    def get_universal_status_bits(self, handle, max_wait_in_milliseconds):
        status_bits = [None]
        status_bits_return = TLMC_SDK.get_universal_status_bits(
            handle, status_bits, max_wait_in_milliseconds)
        if status_bits_return != 0:
            ex = XAErrorFactory.convert_return(
                status_bits_return)
            raise ex
        return status_bits[0]

    def get_velocity_params(self, handle, max_wait_in_milliseconds):
        velocity_params = [None]
        settings_return = TLMC_SDK.get_velocity_params(
            handle, velocity_params, max_wait_in_milliseconds)
        if settings_return != 0:
            ex = XAErrorFactory.convert_return(
                settings_return)
            raise ex
        return velocity_params[0]

    def home(self, handle, wait_timeout):
        home_return = TLMC_SDK.home(handle, wait_timeout)
        if home_return != 0:
            ex = XAErrorFactory.convert_return(home_return)
            raise ex

    def identify(self, handle):
        ident_return = TLMC_SDK.identify(handle)
        if ident_return != 0:
            ex = XAErrorFactory.convert_return(
                ident_return)
            raise ex

    def move_absolute(self, handle, move_mode, position, max_wait_in_milliseconds):
        move_return = TLMC_SDK.move_absolute(handle, move_mode, position, max_wait_in_milliseconds)
        if move_return != 0:
            ex = XAErrorFactory.convert_return(move_return)
            raise ex
        
    def move_continuous(self, handle, direction, max_wait_in_milliseconds):
        move_return = TLMC_SDK.move_continuous(handle, direction, max_wait_in_milliseconds)
        if move_return != 0:
            ex = XAErrorFactory.convert_return(move_return)
            raise ex

    def move_jog(self, handle, direction, max_wait_in_milliseconds):
        move_return = TLMC_SDK.move_jog(handle, direction, max_wait_in_milliseconds)
        if move_return != 0:
            ex = XAErrorFactory.convert_return(move_return)
            raise ex

    def move_relative(self, handle, move_mode, step_size, max_wait_in_milliseconds):
        move_return = TLMC_SDK.move_relative(handle, move_mode, step_size, max_wait_in_milliseconds)
        if move_return != 0:
            ex = XAErrorFactory.convert_return(move_return)
            raise ex

    def open(self, device, transportType, operatingMode):
        device_handle = c_uint32(0)
        open_return = TLMC_SDK.open(device, transportType, operatingMode, device_handle)
        tmp_device_handle = device_handle
        if (open_return != 0):
            tmp_device_handle = -1
            ex = XAErrorFactory.convert_return(open_return)
            raise ex
        return tmp_device_handle

    def persist_params(self, handle, parameter_group_id):
        params_return = TLMC_SDK.persist_params(handle, parameter_group_id)
        if params_return != 0:
            ex = XAErrorFactory.convert_return(
                params_return)
            raise ex

    def pz_get_max_output_voltage_params(self, handle, max_wait_in_milliseconds):
        max_output_voltage = [None]
        params_return = TLMC_SDK.pz_get_max_output_voltage_params(
            handle, max_output_voltage, max_wait_in_milliseconds)
        if params_return != 0:
            ex = XAErrorFactory.convert_return(
                params_return)
            raise ex
        return max_output_voltage[0]

    def pz_get_max_travel(self, handle, max_wait_in_milliseconds):
        max_travel = [None]
        params_return = TLMC_SDK.pz_get_max_travel(
            handle, max_travel, max_wait_in_milliseconds)
        if params_return != 0:
            ex = XAErrorFactory.convert_return(
                params_return)
            raise ex
        return max_travel[0]

    def pz_get_output_voltage(self, handle, max_wait_in_milliseconds):
        output_voltage = [None]
        params_return = TLMC_SDK.pz_get_output_voltage(
            handle, output_voltage, max_wait_in_milliseconds)
        if params_return != 0:
            ex = XAErrorFactory.convert_return(
                params_return)
            raise ex
        return output_voltage[0]

    def pz_get_output_voltage_control_source_params(self, handle, max_wait_in_milliseconds):
        source_params = [None]
        source_return = TLMC_SDK.pz_get_output_voltage_control_source_params(
            handle, source_params, max_wait_in_milliseconds)
        if source_return != 0:
            ex = XAErrorFactory.convert_return(source_return)
            raise ex
        return source_params[0]

    def pz_get_output_waveform_params(self, handle, max_wait_in_millisecconds):
        waveform_params = [None]
        params_return = TLMC_SDK.pz_get_output_waveform_params(
            handle, waveform_params, max_wait_in_millisecconds)
        if params_return != 0:
            ex = XAErrorFactory.convert_return(
                params_return)
            raise ex
        return waveform_params[0]

    def pz_get_position(self, handle, position, max_wait_in_milliseconds):
        position = [None]
        position_return = TLMC_SDK.pz_get_position(
            handle, position, max_wait_in_milliseconds)
        if position_return != 0:
            ex = XAErrorFactory.convert_return(position_return)
            raise ex
        return position[0]

    def pz_get_position_control_mode(self, handle, max_wait_in_milliseconds):
        control_mode = [None]
        control_mode_return = TLMC_SDK.pz_get_position_control_mode(
            handle, control_mode, max_wait_in_milliseconds)
        if control_mode_return != 0:
            ex = XAErrorFactory.convert_return(control_mode_return)
            raise ex
        return control_mode[0]

    def pz_get_position_loop_params(self, handle, max_wait_in_milliseconds):
        position_loop_params = [None]
        params_return = TLMC_SDK.pz_get_position_loop_params(
            handle, position_loop_params, max_wait_in_milliseconds)
        if params_return != 0:
            ex = XAErrorFactory.convert_return(
                params_return)
            raise ex
        return position_loop_params[0]

    def pz_get_slew_rate_params(self, handle, max_wait_in_milliseconds):
        slew_rate_params = [None]
        params_return = TLMC_SDK.pz_get_slew_rate_params(
            handle, slew_rate_params, max_wait_in_milliseconds)
        if params_return != 0:
            ex = XAErrorFactory.convert_return(
                params_return)
            raise ex
        return slew_rate_params[0]

    def pz_get_status(self, handle, max_wait_in_milliseconds):
        status = [None]
        params_return = TLMC_SDK.pz_get_status(
            handle, status, max_wait_in_milliseconds)
        if params_return != 0:
            ex = XAErrorFactory.convert_return(
                params_return)
            raise ex
        return status[0]

    def pz_get_status_bits(self, handle, max_wait_in_milliseconds):
        status_bits = [None]
        params_return = TLMC_SDK.pz_get_status_bits(
            handle, status_bits, max_wait_in_milliseconds)
        if params_return != 0:
            ex = XAErrorFactory.convert_return(
                params_return)
            raise ex
        return status_bits[0]

    def pz_set_max_output_voltage(self, handle, max_output_voltage):
        max_voltage_return = TLMC_SDK.pz_set_max_output_voltage(
            handle, max_output_voltage)
        if max_voltage_return != 0:
            ex = XAErrorFactory.convert_return(
                max_voltage_return)
            raise ex

    def pz_set_output_voltage(self, handle, new_output_voltage):
        set_voltage_return = TLMC_SDK.pz_set_output_voltage(handle, new_output_voltage)
        if set_voltage_return != 0:
            ex = XAErrorFactory.convert_return(
                set_voltage_return)
            raise ex
        
    def pz_set_output_voltage_control_source_params(self, handle, voltage_source):
        params_return = TLMC_SDK.pz_set_output_voltage_control_source_params(
            handle, voltage_source)
        if params_return != 0:
            ex = XAErrorFactory.convert_return(
                params_return)
            raise ex

    def pz_set_output_waveform_lookup_table_sample(self, handle, index, voltage):
        params_return = TLMC_SDK.pz_set_output_waveform_lookup_table_sample(
            handle, index, voltage)
        if params_return != 0:
            ex = XAErrorFactory.convert_return(
                params_return)
            raise ex

    def pz_set_output_waveform_params(self, handle, mode, num_of_samples_per_cycle,
                                      num_of_cycles, sample_delay, pre_cycle_delay,
                                      post_cycle_delay, output_trigger_start_index,
                                      output_trigger_width, num_of_samples_between_triggers):
        params_return = TLMC_SDK.pz_set_output_waveform_params(handle, mode, num_of_samples_per_cycle,
                                                               num_of_cycles, sample_delay, pre_cycle_delay,
                                                               post_cycle_delay, output_trigger_start_index,
                                                               output_trigger_width, num_of_samples_between_triggers)
        if params_return != 0:
            ex = XAErrorFactory.convert_return(
                params_return)
            raise ex

    def pz_set_position(self, handle, new_position):
        params_return = TLMC_SDK.pz_set_position(handle, new_position)
        if params_return != 0:
            ex = XAErrorFactory.convert_return(
                params_return)
            raise ex

    def pz_set_position_control_mode(self, handle, new_control_mode):
        params_return = TLMC_SDK.pz_set_position_control_mode(
            handle, new_control_mode)
        if params_return != 0:
            ex = XAErrorFactory.convert_return(
                params_return)
            raise ex

    def pz_set_position_loop_params(self, handle, proportional, integral):
        params_return = TLMC_SDK.pz_set_position_loop_params(
            handle, proportional, integral)
        if params_return != 0:
            ex = XAErrorFactory.convert_return(
                params_return)
            raise ex

    def pz_set_slew_rate_params(self, handle, open_slew_rate, closed_slew_rate):
        params_return = TLMC_SDK.pz_set_slew_rate_params(
            handle, open_slew_rate, closed_slew_rate)
        if params_return != 0:
            ex = XAErrorFactory.convert_return(
                params_return)
            raise ex

    def pz_set_zero(self, handle, max_wait_in_milliseconds):
        params_return = TLMC_SDK.pz_set_zero(handle, max_wait_in_milliseconds)
        if params_return != 0:
            ex = XAErrorFactory.convert_return(
                params_return)
            raise ex

    def pz_start_output_waveform(self, handle):
        params_return = TLMC_SDK.pz_start_output_waveform(handle)
        if params_return != 0:
            ex = XAErrorFactory.convert_return(
                params_return)
            raise ex

    def pz_stop_output_waveform(self, handle):
        params_return = TLMC_SDK.pz_stop_output_waveform(handle)
        if params_return != 0:
            ex = XAErrorFactory.convert_return(
                params_return)
            raise ex

    def rack_identify(self, handle, channel):
        rack_return = TLMC_SDK.rack_identify(handle, channel)
        if rack_return != 0:
            ex = XAErrorFactory.convert_return(rack_return)
            raise ex

    @staticmethod
    def remove_simulation(description: dict):
        simulation_return = TLMC_SDK.remove_simulation(description)
        if simulation_return != 0:
            ex = XAErrorFactory.convert_return(
                simulation_return)
            raise ex

    def restore_to_factory_defaults(self, handle):
        defaults_return = TLMC_SDK.restore_factory_defaults(handle)
        if defaults_return != 0:
            ex = XAErrorFactory.convert_return(
                defaults_return)
            raise ex

    def set_analog_monitor_configuration_params(self, handle, monitor_number, motor_channel, system_variable, scale, offset):
        params_return = TLMC_SDK.set_analog_monitor_configuration_params(
            handle, monitor_number, motor_channel, system_variable, scale, offset)
        if params_return != 0:
            ex = XAErrorFactory.convert_return(
                params_return)
            raise ex

    def set_aux_io_port_mode(self, handle, port_number, new_mode):
        mode_return = TLMC_SDK.set_aux_io_port_mode(
            handle, port_number, new_mode)
        if mode_return != 0:
            ex = XAErrorFactory.convert_return(mode_return)
            raise ex

    def set_aux_io_software_states(self, handle, new_state):
        state_return = TLMC_SDK.set_aux_io_software_states(handle, new_state)
        if state_return != 0:
            ex = XAErrorFactory.convert_return(
                state_return)
            raise ex

    def set_bow_index(self, handle, new_bow_index):
        index_return = TLMC_SDK.set_bow_index(handle, new_bow_index)
        if index_return != 0:
            ex = XAErrorFactory.convert_return(
                index_return)
            raise ex

    def set_connected_product(self, handle, product_name):
        product_return = TLMC_SDK.set_connected_product(handle, product_name)
        if product_return != 0:
            ex = XAErrorFactory.convert_return(
                product_return)
            raise ex

    def set_connected_product_info(self, handle, product_name, axis_type, movement_type, unit_type,
                                   distance_scale_factor, velocity_scale_factor,
                                   acceleration_scale_factor, min_position, max_position,
                                   max_velocity, max_acceleration):
        info_return = TLMC_SDK.set_connected_product_info(handle, product_name, axis_type, movement_type, unit_type,
                                                          distance_scale_factor, velocity_scale_factor,
                                                          acceleration_scale_factor, min_position, max_position,
                                                          max_velocity, max_acceleration)
        if info_return != 0:
            ex = XAErrorFactory.convert_return(info_return)
            raise ex

    def set_current_loop_params(self, handle, loop_scenario, phase, proportional, integral,
                                integral_limit, integral_dead_band, feed_fwrd):
        loop_return = TLMC_SDK.set_current_loop_params(handle, loop_scenario, phase, proportional, integral,
                                                       integral_limit, integral_dead_band, feed_fwrd)
        if loop_return != 0:
            ex = XAErrorFactory.convert_return(loop_return)
            raise ex

    def set_dc_pid_params(self, handle, proportional, integral, derivative, integral_limit, filter_control):
        pid_return = TLMC_SDK.set_dc_pid_params(
            handle, proportional, integral, derivative, integral_limit, filter_control)
        if pid_return != 0:
            ex = XAErrorFactory.convert_return(pid_return)
            raise ex

    def set_digital_output_params(self, handle, new_output_state):
        digital_return = TLMC_SDK.set_digital_output_states(
            handle, new_output_state)
        if digital_return != 0:
            ex = XAErrorFactory.convert_return(
                digital_return)
            raise ex

    def set_enable_state(self, handle, enable_state):
        enable_return = TLMC_SDK.set_enable_state(handle, enable_state)
        if enable_return != 0:
            ex = XAErrorFactory.convert_return(
                enable_return)
            raise ex

    def set_end_of_message_mode(self, handle, mode):
        mode_return = TLMC_SDK.set_end_of_message_mode(handle, mode)
        if mode_return != 0:
            ex = XAErrorFactory.convert_return(mode_return)
            raise ex

    def set_encoder_counter(self, handle, new_encoder_counter):
        encoder_return = TLMC_SDK.set_encoder_counter(
            handle, new_encoder_counter)
        if encoder_return != 0:
            ex = XAErrorFactory.convert_return(
                encoder_return)
            raise ex

    def set_general_move_params(self, handle, backlash_distance):
        settings_return = TLMC_SDK.set_general_move_params(
            handle, backlash_distance)
        if settings_return != 0:
            ex = XAErrorFactory.convert_return(
                settings_return)
            raise ex

    def set_home_params(self, handle, direction, limit_switch, velocity, offset_distance):
        home_params_return = TLMC_SDK.set_home_params(
            handle, direction, limit_switch, velocity, offset_distance)
        if home_params_return != 0:
            ex = XAErrorFactory.convert_return(
                home_params_return)
            raise ex

    def set_io_configuration_params(self, handle, port_number, mode, trigger_out_source):
        params_return = TLMC_SDK.set_io_configuration_params(
            handle, port_number, mode, trigger_out_source)
        if params_return != 0:
            ex = XAErrorFactory.convert_return(
                params_return)
            raise ex

    def set_io_position_trigger_enable_state(self, handle, new_enable_state, max_wait_in_milliseconds):
        enable_state_return = TLMC_SDK.set_io_position_trigger_enable_state(
            handle, new_enable_state, max_wait_in_milliseconds)
        if enable_state_return != 0:
            ex = XAErrorFactory.convert_return(
                enable_state_return)
            raise ex

    def set_io_trigger_params(self, handle, trigger_in_mode, trigger_in_polarity,
                              trigger_in_source, trigger_out_mode, trigger_out_polarity,
                              trigger_out_forward_start_position, trigger_out_forward_interval,
                              trigger_out_forward_number_of_pulses, trigger_out_reverse_start_position,
                              trigger_out_reverse_interval, trigger_out_reverse_number_of_pulses,
                              trigger_out_pulse_width, trigger_out_number_of_cycles):
        io_trigger_return = TLMC_SDK.set_io_trigger_params(handle, trigger_in_mode, trigger_in_polarity,
                                                           trigger_in_source, trigger_out_mode, trigger_out_polarity,
                                                           trigger_out_forward_start_position, trigger_out_forward_interval,
                                                           trigger_out_forward_number_of_pulses, trigger_out_reverse_start_position,
                                                           trigger_out_reverse_interval, trigger_out_reverse_number_of_pulses,
                                                           trigger_out_pulse_width, trigger_out_number_of_cycles)
        if io_trigger_return != 0:
            ex = XAErrorFactory.convert_return(
                io_trigger_return)
            raise ex

    def set_joystick_params(self, handle, low_gear_velocity, high_gear_velocity, low_gear_acceleration, high_gear_acceleration, direction_sense):
        joystick_return = TLMC_SDK.set_joystick_params(handle, low_gear_velocity, high_gear_velocity, low_gear_acceleration,
                                                       high_gear_acceleration, direction_sense)
        if joystick_return != 0:
            ex = XAErrorFactory.convert_return(
                joystick_return)
            raise ex

    def set_kcube_io_trigger_params(self, handle, trigger_one_mode, trigger_one_polarity,
                                    trigger_two_mode, trigger_two_polarity):
        kcube_trigger_return = TLMC_SDK.set_kcube_io_trigger_params(handle, trigger_one_mode, trigger_one_polarity,
                                                                    trigger_two_mode, trigger_two_polarity)
        if kcube_trigger_return != 0:
            ex = XAErrorFactory.convert_return(
                kcube_trigger_return)
            raise ex

    def set_kcube_mmi_lock_state(self, handle, lock_state):
        lock_state_return = TLMC_SDK.set_kcube_mmi_lock_state(
            handle, lock_state)
        if lock_state_return != 0:
            ex = XAErrorFactory.convert_return(
                lock_state_return)
            raise ex

    def set_kcube_mmi_params(self, handle, joystick_mode, joystick_velocity, joystick_acceleration,
                             joystick_direction_sense, position_one, position_two,
                             display_brightness, display_timeout, display_dim_level,
                             position_three, joystick_sensitivity):
        mmi_params_return = TLMC_SDK.set_kcube_mmi_params(handle, joystick_mode, joystick_velocity, joystick_acceleration,
                                                          joystick_direction_sense, position_one, position_two,
                                                          display_brightness, display_timeout, display_dim_level,
                                                          position_three, joystick_sensitivity)
        if mmi_params_return != 0:
            ex = XAErrorFactory.convert_return(
                mmi_params_return)
            raise ex

    def set_kcube_position_trigger_params(self, handle, fwrd_start_position, fwrd_interval,
                                          fwrd_number_of_pulses, rev_start_position,
                                          rev_interval, rev_number_of_pulses, pulse_width,
                                          number_of_cycles):
        kcube_trigger_return = TLMC_SDK.set_kcube_position_trigger_params(handle, fwrd_start_position, fwrd_interval,
                                                                          fwrd_number_of_pulses, rev_start_position,
                                                                          rev_interval, rev_number_of_pulses, pulse_width,
                                                                          number_of_cycles)
        if kcube_trigger_return != 0:
            ex = XAErrorFactory.convert_return(
                kcube_trigger_return)
            raise ex

    def set_lcd_display_params(self, handle, knob_sensitivity, display_brightness, display_timeout,
                               display_dim_level):
        lcd_display_return = TLMC_SDK.set_lcd_display_params(handle, knob_sensitivity, display_brightness, display_timeout,
                                                             display_dim_level)
        if lcd_display_return != 0:
            ex = XAErrorFactory.convert_return(
                lcd_display_return)
            raise ex

    def set_lcd_move_params(self, handle, knob_mode, jog_step_size, acceleration,
                            max_velocity, jog_stop_mode, preset_position):
        lcd_move_return = TLMC_SDK.set_lcd_move_params(handle, knob_mode, jog_step_size, acceleration,
                                                       max_velocity, jog_stop_mode, preset_position)
        if lcd_move_return != 0:
            ex = XAErrorFactory.convert_return(
                lcd_move_return)
            raise ex

    def set_limit_switch_params(self, handle, clockwise_limit_mode, counter_clockwise_mode,
                                clockwise_soft_limit, counter_clockwise_soft_limit, soft_limit_operating_mode):
        limit_return = TLMC_SDK.set_limit_switch_params(handle, clockwise_limit_mode,
                                                        counter_clockwise_mode, clockwise_soft_limit,
                                                        counter_clockwise_soft_limit, soft_limit_operating_mode)
        if limit_return != 0:
            ex = XAErrorFactory.convert_return(
                limit_return)
            raise ex

    def set_motor_output_params(self, handle, current_limit, energy_limit, motor_limit, motor_bias):
        output_return = TLMC_SDK.set_motor_output_params(
            handle, current_limit, energy_limit, motor_limit, motor_bias)
        if output_return != 0:
            ex = XAErrorFactory.convert_return(
                output_return)
            raise ex

    def set_move_absolute_params(self, handle, absolutePosition):
        set_params_return = TLMC_SDK.set_move_absolute_params(
            handle, absolutePosition)
        if set_params_return != 0:
            ex = XAErrorFactory.convert_return(
                set_params_return)
            raise ex

    def set_move_jog_params(self, handle, jog_mode, step_size, min_velocity, max_velocity, acceleration, stop_mode):
        settings_return = TLMC_SDK.set_move_jog_params(
            handle, jog_mode, step_size, min_velocity, max_velocity, acceleration, stop_mode)
        if settings_return != 0:
            ex = XAErrorFactory.convert_return(
                settings_return)
            raise ex

    def set_move_relative_params(self, handle, relative_distance):
        set_params_return = TLMC_SDK.set_move_relative_params(
            handle, relative_distance)
        if set_params_return != 0:
            ex = XAErrorFactory.ConvertReturnToExceptionOrPass(
                set_params_return)
            raise ex

    def set_position_counter(self, handle, new_position_counter):
        counter_return = TLMC_SDK.set_position_counter(
            handle, new_position_counter)
        if counter_return != 0:
            ex = XAErrorFactory.convert_return(
                counter_return)
            raise ex

    def set_position_loop_params(self, handle, position_loop_scenario, proportional, integral, integral_limit,
                                 derivative, servo_cycles, scale, velocity_feed_fwrd,
                                 acceleration_feed_fwrd, error_limit):
        loop_return = TLMC_SDK.set_position_loop_params(handle, position_loop_scenario, proportional, integral, integral_limit,
                                                        derivative, servo_cycles, scale, velocity_feed_fwrd,
                                                        acceleration_feed_fwrd, error_limit)
        if loop_return != 0:
            ex = XAErrorFactory.convert_return(loop_return)
            raise ex

    def set_power_params(self, handle, rest_factor, move_factor):
        power_return = TLMC_SDK.set_power_params(
            handle, rest_factor, move_factor)
        if power_return != 0:
            ex = XAErrorFactory.convert_return(
                power_return)
            raise ex

    def set_profiled_mode_params(self, handle, mode, jerk):
        profiled_return = TLMC_SDK.set_profiled_mode_params(handle, mode, jerk)
        if profiled_return != 0:
            ex = XAErrorFactory.convert_return(
                profiled_return)
            raise ex

    def set_setting(self, handle, settings_name):
        settings_return = TLMC_SDK.set_setting(handle, settings_name)
        if settings_return != 0:
            ex = XAErrorFactory.convert_return(
                settings_return)
            raise ex

    def set_settings_from_string(self, handle, settings_name):
        settings_return = TLMC_SDK.set_settings_from_string(
            handle, settings_name)
        if settings_return != 0:
            ex = XAErrorFactory.convert_return(
                settings_return)
            raise ex

    def set_stage_axis_params(self, handle, type_id, axis_id, part_number, serial_number,
                              counts_per_unit, min_position, max_position,
                              max_acceleration, max_decceleration, max_velcoity,
                              gear_box_ratio):
        stage_axis_return = TLMC_SDK.set_stage_axis_params(handle, type_id, axis_id, part_number, serial_number,
                                                           counts_per_unit, min_position, max_position,
                                                           max_acceleration, max_decceleration, max_velcoity,
                                                           gear_box_ratio)
        if stage_axis_return != 0:
            ex = XAErrorFactory.convert_return(
                stage_axis_return)
            raise ex

    def set_status_mode(self, handle, operating_mode):
        status_return = TLMC_SDK.set_status_mode(handle, operating_mode)
        if status_return != 0:
            ex = XAErrorFactory.convert_return(
                status_return)
            raise ex

    def set_stepper_loop_params(self, handle, loop_mode, proportional, integral,
                                differential, output_clip, output_tolerance,
                                microsteps_per_ecount):
        loop_return = TLMC_SDK.set_stepper_loop_params(handle, loop_mode, proportional, integral,
                                                       differential, output_clip, output_tolerance,
                                                       microsteps_per_ecount)
        if loop_return != 0:
            ex = XAErrorFactory.convert_return(loop_return)
            raise ex

    def set_track_settle_params(self, handle, settle_time, settle_window, track_window):
        track_return = TLMC_SDK.set_track_settle_params(
            handle, settle_time, settle_window, track_window)
        if track_return != 0:
            ex = XAErrorFactory.convert_return(
                track_return)
            raise ex

    def set_trigger_params_for_for_dc_brushless(self, handle, trigger_mode):
        trigger_return = TLMC_SDK.set_trigger_params_for_dc_brushless(
            handle, trigger_mode)
        if trigger_return != 0:
            ex = XAErrorFactory.convert_return(
                trigger_return)
            raise ex

    def set_trigger_params_for_stepper(self, handle, trigger_mode):
        trigger_return = TLMC_SDK.set_trigger_params_for_stepper(
            handle, trigger_mode)
        if trigger_return != 0:
            ex = XAErrorFactory.convert_return(
                trigger_return)
            raise ex

    def set_velocity_params(self, handle, min_velocity, acceleration, max_velocity):
        settings_return = TLMC_SDK.set_velocity_params(
            handle, min_velocity, acceleration, max_velocity)
        if settings_return != 0:
            ex = XAErrorFactory.convert_return(
                settings_return)
            raise ex

    @staticmethod
    def shutdown():
        startup_return = TLMC_SDK.shutdown()
        if startup_return != 0:
            ex = XAErrorFactory.convert_return(
                startup_return)
            raise ex
        pass
    
    @staticmethod
    def startup(settings_file_name: str):
        """
        Starts and initiates the XA system. Settings_file_name can be null or be used to initialise the XA logger. 
        """
        startup_return = TLMC_SDK.startup(settings_file_name)
        if startup_return != 0:
            ex = XAErrorFactory.convert_return(
                startup_return)
            raise ex
        pass

    def stop(self, handle, stop_mode, max_wait_in_milliseconds):
        stop_return = TLMC_SDK.stop(
            handle, stop_mode, max_wait_in_milliseconds)
        if stop_return != 0:
            ex = XAErrorFactory.convert_return(stop_return)
            raise ex

    @staticmethod
    def try_load_library(current_path):
        """
        Loads the tlmc_xa_native.dll. Copy this from the XA folder and pass in
        the scripts current path. 
        """
        TLMC_SDK.try_load_library(current_path)
