from ctypes import cdll, c_uint32, c_uint16, c_uint8, byref, c_bool, c_char, c_char_p, c_int16, c_double, sizeof
import os
import copy
import json

from ctypes import *
from xa_sdk.shared.tlmc_type_structures import *


# TLMC SDK main class.
class TLMC_SDK:
    is_load = False 
    xa_lib = None
    
    @staticmethod
    def try_load_library(__file__):
        absolute_path_to_file_directory = os.path.dirname(os.path.abspath(__file__))
        absolute_path_to_dlls = os.path.abspath(absolute_path_to_file_directory)
        os.environ['PATH'] = absolute_path_to_dlls + os.pathsep + os.environ['PATH']

        try:
            os.add_dll_directory(absolute_path_to_dlls)
            TLMC_SDK.xa_lib = cdll.LoadLibrary("./tlmc_xa_native.dll")
            TLMC_SDK.is_load = True

        except AttributeError:
            pass

    @staticmethod
    def add_user_message_to_log(user_message):
        message_val = c_char(user_message)
        ret = TLMC_SDK.xa_lib.TLMC_AddUserMessageToLog(message_val)
        return ret

    @staticmethod
    def close(handle):
        ret = TLMC_SDK.xa_lib.TLMC_Close(handle)
        return ret

    @staticmethod
    def convert_from_device_units_to_physical(handle, TLMC_scale_type, device_value, physical_value):
        device_val = c_int64(device_value).value
        physical_val = c_double(0)
        p_memory_block = c_int32(0)
        ret = TLMC_SDK.xa_lib.TLMC_ConvertFromDeviceToPhysical(
            handle, TLMC_scale_type, device_val, byref(physical_val), byref(p_memory_block))
        var2 = p_memory_block.value
        physical_value[0] = (physical_val.value, var2)
        return ret

    @staticmethod
    def convert_from_physical_to_device(handle, TLMC_scale_type, TLMC_unit_type, physical_value, device_value):
        device_val = c_int64(0)
        physical_val = c_double(physical_value)
        ret = TLMC_SDK.xa_lib.TLMC_ConvertFromPhysicalToDevice(
            handle, TLMC_scale_type, TLMC_unit_type, physical_val, byref(device_val))
        device_value[0] = device_val.value
        return ret

    @staticmethod
    def create_simulation(description):
        contents = json.dumps(description)
        ret = TLMC_SDK.xa_lib.TLMC_CreateSimulation(contents.encode('utf-8'))
        return ret

    @staticmethod
    def disconnect(handle):
        ret = TLMC_SDK.xa_lib.TLMC_Disconnect(handle)
        return ret

    @staticmethod
    def get_adc_inputs(handle, adc_inputs, max_wait_in_milliseconds):
        inputs_val = TLMC_AdcInputs()
        max_wait_val = c_int64(max_wait_in_milliseconds)
        ret = TLMC_SDK.xa_lib.TLMC_GetAdcInputs(
            handle, byref(inputs_val), max_wait_val)
        adc_inputs[0] = inputs_val
        return ret

    @staticmethod
    def get_analog_monitor_configuration_params(handle, monitor_number, configuration_params, max_wait_in_milliseconds):
        params_val = TLMC_AnalogMonitorConfigurationParams()
        monitor_val = monitor_number 
        max_wait_val = c_int64(max_wait_in_milliseconds)
        ret = TLMC_SDK.xa_lib.TLMC_GetAnalogMonitorConfigurationParams(
            handle, monitor_val, byref(params_val), max_wait_val)
        configuration_params[0] = params_val
        return ret

    @staticmethod
    def get_api_version(api_version):
        api_val = TLMC_ApiVersion()
        ret = TLMC_SDK.xa_lib.TLMC_GetApiVersion(byref(api_val))
        api_version[0] = api_val
        return ret

    @staticmethod
    def get_aux_io_port_mode(handle, port_number, port_mode, max_wait_in_milliseconds):
        port_number_val = port_number  
        mode_val = TLMC_AuxIoPortMode()
        max_wait_val = c_int64(max_wait_in_milliseconds)
        ret = TLMC_SDK.xa_lib.TLMC_GetAuxIoPortMode(
            handle, port_number_val, byref(mode_val), max_wait_val)
        port_mode[0] = mode_val
        return ret

    @staticmethod
    def get_aux_io_software_states(handle, software_states, max_wait_in_milliseconds):
        states_val = c_uint16(software_states)
        max_wait_val = c_int64(max_wait_in_milliseconds)
        ret = TLMC_SDK.xa_lib.TLMC_GetAuxIoSoftwareStates(
            handle, byref(states_val), max_wait_val)
        return ret

    @staticmethod
    def get_bow_index(handle, bow_index, index_val, max_wait_in_milliseconds):
        index_temp = c_uint16(index_val)
        max_wait_val = c_int64(max_wait_in_milliseconds)
        ret = TLMC_SDK.xa_lib.TLMC_GetBowIndex(
            handle, byref(index_temp), max_wait_val)
        bow_index[0] = index_temp.value
        return ret

    @staticmethod
    def get_connected_product(handle, connected_product, product_buffer):
        buffer_val = c_char(product_buffer)
        length_val = c_uint(len(buffer_val.value))
        ret = TLMC_SDK.xa_lib.TLMC_GetConnectedProduct(
            handle, byref(buffer_val), length_val)
        connected_product[0] = buffer_val
        return ret

    @staticmethod
    def get_connected_product_info(handle, product_info):
        info_val = TLMC_ConnectedProductInfo()
        ret = TLMC_SDK.xa_lib.TLMC_GetConnectedProductInfo(
            handle, byref(info_val))
        product_info[0] = info_val
        return ret

    @staticmethod
    def get_connected_products_supported(handle, connected_products):
        buffer_val = create_string_buffer(98)
        length_val = c_uint(len(buffer_val))
        result_length = c_int32(0)
        ret = TLMC_SDK.xa_lib.TLMC_GetConnectedProductsSupported(
            handle, byref(buffer_val), length_val, byref(result_length))
        connected_products[0] = buffer_val.value
        return ret

    @staticmethod
    def get_current_loop_params(handle, loop_scenario, loop_params, max_wait_in_milliseconds):
        params_val = TLMC_CurrentLoopParams()
        scenario_val = loop_scenario
        max_wait_val = c_int64(max_wait_in_milliseconds)
        ret = TLMC_SDK.xa_lib.TLMC_GetCurrentLoopParams(
            handle, scenario_val, byref(params_val), max_wait_val)
        loop_params[0] = params_val
        return ret

    @staticmethod
    def get_dc_pid_params(handle, pid_params, max_wait_in_milliseconds):
        params_val = TLMC_DcPidParams()
        max_wait_val = c_int64(max_wait_in_milliseconds)
        ret = TLMC_SDK.xa_lib.TLMC_GetDcPidParams(
            handle, byref(params_val), max_wait_val)
        pid_params[0] = params_val
        return ret

    @staticmethod
    def get_device_info(handle, device_info, max_wait_in_milliseconds):
        device_info_val = TLMC_DeviceInfo()
        max_wait_in_milliseconds_val = c_int64(max_wait_in_milliseconds)
        ret = TLMC_SDK.xa_lib.TLMC_GetDeviceInfo(handle, byref(
            device_info_val), max_wait_in_milliseconds_val)
        device_info[0] = device_info_val
        return ret

    @staticmethod
    def get_device_list_item_count(count):
        count_val = c_uint16(0)
        ret = TLMC_SDK.xa_lib.TLMC_GetDeviceListItemCount(byref(count_val))
        count[0] = count_val
        return ret

    @staticmethod
    def get_device_list_items(source_start_index, number_of_items, TLMC_device_info, number_of_items_copied):
        TLMC_device_list_struct = TLMC_DeviceInfo()
        start_index_val = c_uint16(source_start_index)
        memory_block_size = number_of_items * sizeof(TLMC_device_list_struct)
        p_memory_block = create_string_buffer(b"0", memory_block_size)
        items_copied_val = c_uint16(number_of_items_copied)
        new_block = create_string_buffer("0", sizeof(TLMC_DeviceInfo))
        ret = TLMC_SDK.xa_lib.TLMC_GetDeviceListItems(start_index_val, c_uint16(
            number_of_items), byref(p_memory_block), byref(items_copied_val))
        for i in range(items_copied_val.value):
            new_block = create_string_buffer(b"0", sizeof(TLMC_DeviceInfo))
            memmove(byref(new_block), (addressof(p_memory_block) +
                    i * sizeof(TLMC_DeviceInfo)), sizeof(new_block))
            var = cast(addressof(new_block), POINTER(TLMC_DeviceInfo))
            TLMC_device_info[i] = copy.copy(var.contents)
        return ret

    @staticmethod 
    def get_digital_input_states(handle, input_state, max_wait_in_milliseconds):
        state_val = c_uint8(0)
        max_wait_val = c_int64(max_wait_in_milliseconds)
        ret = TLMC_SDK.xa_lib.TLMC_GetDigitalInputStates(
            handle, byref(state_val), max_wait_val)
        input_state[0] = state_val
        return ret
    
    @staticmethod
    def get_digital_output_params(handle, output_state, max_wait_in_milliseconds):
        state_val = c_uint8(0)
        max_wait_val = c_int64(max_wait_in_milliseconds)
        ret = TLMC_SDK.xa_lib.TLMC_GetDigitalOutputStates(
            handle, byref(state_val), max_wait_val)
        output_state[0] = state_val
        return ret

    @staticmethod
    def get_enable_state(handle, channel_enable_state, max_wait_in_milliseconds):
        channel_enable_state_val = c_uint8(0)
        max_wait_in_milliseconds_val = c_int64(max_wait_in_milliseconds)
        ret = TLMC_SDK.xa_lib.TLMC_GetEnableState(handle, byref(
            channel_enable_state_val), max_wait_in_milliseconds_val)
        channel_enable_state[0] = channel_enable_state_val
        return ret

    @staticmethod
    def get_encoder_counter(handle, encoder_counter, max_wait_in_milliseconds):
        encoder_val = c_int32(0)
        max_wait_val = c_int64(max_wait_in_milliseconds)
        ret = TLMC_SDK.xa_lib.TLMC_GetEncoderCounter(
            handle, byref(encoder_val), max_wait_val)
        encoder_counter[0] = encoder_val
        return ret

    @staticmethod
    def get_general_move_params(handle, general_move_params, max_wait_in_milliseconds):
        general_move_params_val = TLMC_GeneralMoveParams()
        max_wait_in_milliseconds_val = c_int64(max_wait_in_milliseconds)
        ret = TLMC_SDK.xa_lib.TLMC_GetGeneralMoveParams(handle, byref(
            general_move_params_val), max_wait_in_milliseconds_val)
        general_move_params[0] = general_move_params_val
        return ret

    @staticmethod
    def get_hardware_info(handle, hardware_info, max_wait_in_milliseconds):
        hardware_info_val = TLMC_HardwareInfo()
        max_wait_in_milliseconds_val = c_int64(max_wait_in_milliseconds)
        ret = TLMC_SDK.xa_lib.TLMC_GetHardwareInfo(handle, byref(
            hardware_info_val), max_wait_in_milliseconds_val)
        hardware_info[0] = hardware_info_val
        return ret

    @staticmethod
    def get_home_params(handle, home_params, max_wait_in_milliseconds):
        home_params_val = TLMC_HomeParams()
        max_wait_in_milliseconds_val = c_int64(max_wait_in_milliseconds)
        ret = TLMC_SDK.xa_lib.TLMC_GetHomeParams(handle, byref(
            home_params_val), max_wait_in_milliseconds_val)
        home_params[0] = home_params_val
        return ret

    @staticmethod
    def get_io_configuration_number_of_ports_supported(handle, number_of_ports):
        ports_val = c_uint8(0)
        ret = TLMC_SDK.xa_lib.TLMC_GetIoConfigurationNumberOfPortsSupported(
            handle, byref(ports_val))
        number_of_ports[0] = ports_val
        return ret

    @staticmethod
    def get_io_configuration_params(handle, port_number, configuration_params, max_wait_in_milliseconds):
        port_val = port_number 
        params_val = TLMC_IoConfigurationParams()
        max_wait_val = c_int64(max_wait_in_milliseconds)
        ret = TLMC_SDK.xa_lib.TLMC_GetIoConfigurationParams(
            handle, port_val, byref(params_val), max_wait_val)
        configuration_params[0] = params_val
        return ret

    @staticmethod
    def get_io_position_trigger_enable_state(handle, pEnable_state, max_wait_in_milliseconds):
        enable_state_val = c_uint8(0)
        max_wait_in_milliseconds_val = c_int64(max_wait_in_milliseconds)
        ret = TLMC_SDK.xa_lib.TLMC_GetIoPositionTriggerEnableState(
            handle, byref(enable_state_val), max_wait_in_milliseconds_val)
        pEnable_state[0] = enable_state_val
        return ret

    @staticmethod
    def get_io_trigger_params(handle, io_trigger_params, max_wait_in_milliseconds):
        io_trigger_params_val = TLMC_IoTriggerParams()
        max_wait_in_milliseconds_val = c_int64(max_wait_in_milliseconds)
        ret = TLMC_SDK.xa_lib.TLMC_GetIoTriggerParams(handle, byref(
            io_trigger_params_val), max_wait_in_milliseconds_val)
        io_trigger_params[0] = io_trigger_params_val
        return ret

    @staticmethod
    def get_jog_params(handle, jog_params, max_wait_in_milliseconds):
        jog_params_val = TLMC_JogParams()
        max_wait_in_milliseconds_val = c_int64(max_wait_in_milliseconds)
        ret = TLMC_SDK.xa_lib.TLMC_GetJogParams(handle, byref(
            jog_params_val), max_wait_in_milliseconds_val)
        jog_params[0] = jog_params_val
        return ret

    @staticmethod
    def get_joystick_params(handle, joystick_params, max_wait_in_milliseconds):
        joystick_val = TLMC_JoystickParams()
        max_wait_val = c_int64(max_wait_in_milliseconds)
        ret = TLMC_SDK.xa_lib.TLMC_GetJoystickParams(
            handle, byref(joystick_val), max_wait_val)
        joystick_params[0] = joystick_val
        return ret

    @staticmethod
    def get_kcube_io_trigger_params(handle, kcube_io_params, max_wait_in_milliseconds):
        params_val = TLMC_KcubeIoTriggerParams()
        max_wait_val = c_int64(max_wait_in_milliseconds)
        ret = TLMC_SDK.xa_lib.TLMC_GetKcubeIoTriggerParams(
            handle, byref(params_val), max_wait_val)
        kcube_io_params[0] = params_val
        return ret

    @staticmethod
    def get_kcube_mmi_lock_state(handle, lock_state, max_wait_in_milliseconds):
        lock_state_val = [0]
        max_wait_val = c_int64(max_wait_in_milliseconds)
        ret = TLMC_SDK.xa_lib.TLMC_GetKcubeMmiLockState(
            handle, byref(lock_state_val), max_wait_val)
        lock_state[0] = lock_state_val
        return ret

    @staticmethod
    def get_kcube_mmi_params(handle, mmi_params, max_wait_in_milliseconds):
        params_val = TLMC_KcubeMmiParams()
        max_wait_val = c_int64(max_wait_in_milliseconds)
        ret = TLMC_SDK.xa_lib.TLMC_GetKcubeMmiParams(
            handle, byref(params_val), max_wait_val)
        mmi_params[0] = params_val
        return ret

    @staticmethod
    def get_kcube_position_trigger_params(handle, kcube_trigger_params, max_wait_in_milliseconds):
        params_val = TLMC_KcubePositionTriggerParams()
        max_wait_val = c_int64(max_wait_in_milliseconds)
        ret = TLMC_SDK.xa_lib.TLMC_GetKcubePositionTriggerParams(
            handle, byref(params_val), max_wait_val)
        kcube_trigger_params[0] = params_val
        return ret

    @staticmethod
    def get_lcd_display_params(handle, lcd_display_params, max_wait_in_milliseconds):
        lcd_params_val = TLMC_LcdDisplayParams()
        max_wait_val = c_int64(max_wait_in_milliseconds)
        ret = TLMC_SDK.xa_lib.TLMC_GetLcdDisplayParams(
            handle, byref(lcd_params_val), max_wait_val)
        lcd_display_params[0] = lcd_params_val
        return ret

    @staticmethod
    def get_lcd_move_params(handle, lcd_move_params, max_wait_in_milliseconds):
        lcd_params_val = TLMC_LcdMoveParams()
        max_wait_val = c_int64(max_wait_in_milliseconds)
        ret = TLMC_SDK.xa_lib.TLMC_GetLcdMoveParams(
            handle, byref(lcd_params_val), max_wait_val)
        lcd_move_params[0] = lcd_params_val
        return ret

    @staticmethod
    def get_limit_switch_params(handle, limit_switch_params, max_wait_in_milliseconds):
        limit_switch_params_val = TLMC_LimitSwitchParams()
        max_wait_in_milliseconds_val = c_int64(max_wait_in_milliseconds)
        ret = TLMC_SDK.xa_lib.TLMC_GetLimitSwitchParams(handle, byref(
            limit_switch_params_val), max_wait_in_milliseconds_val)
        limit_switch_params[0] = limit_switch_params_val
        return ret

    @staticmethod
    def get_motor_output_params(handle, motor_output_params, max_wait_in_miliseconds):
        output_params_val = TLMC_MotorOutputParams()
        max_wait_val = c_int64(max_wait_in_miliseconds)
        ret = TLMC_SDK.xa_lib.TLMC_GetMotorOutputParams(
            handle, byref(output_params_val), max_wait_val)
        motor_output_params[0] = output_params_val
        return ret

    @staticmethod
    def get_move_absolute_params(handle, move_absolute_params, max_wait_in_milliseconds):
        move_absolute_params_val = TLMC_MoveAbsoluteParams()
        max_wait_in_milliseconds_val = c_int64(max_wait_in_milliseconds)
        ret = TLMC_SDK.xa_lib.TLMC_GetMoveAbsoluteParams(handle, byref(
            move_absolute_params_val), max_wait_in_milliseconds_val)
        move_absolute_params[0] = move_absolute_params_val
        return ret

    @staticmethod
    def get_move_relative_params(handle, move_relative_params, max_wait_in_milliseconds):
        move_relative_params_val = TLMC_MoveRelativeParams()
        max_wait_in_milliseconds_val = c_int64(max_wait_in_milliseconds)
        ret = TLMC_SDK.xa_lib.TLMC_GetMoveRelativeParams(handle, byref(
            move_relative_params_val), max_wait_in_milliseconds_val)
        move_relative_params[0] = move_relative_params_val
        return ret

    @staticmethod
    def get_position_counter(handle, pPosition_counter, max_wait_in_milliseconds):
        position_val = c_int32(0)
        max_wait_in_milliseconds_val = c_int64(max_wait_in_milliseconds)
        ret = TLMC_SDK.xa_lib.TLMC_GetPositionCounter(
            handle, byref(position_val), max_wait_in_milliseconds_val)
        pPosition_counter[0] = position_val.value
        return ret

    @staticmethod
    def get_position_loop_params(handle, position_loop_scenario, position_loop_params, max_wait_in_milliseconds):
        scenario_val = position_loop_scenario
        loop_params = TLMC_PositionLoopParams()
        max_wait_val = c_int64(max_wait_in_milliseconds)
        ret = TLMC_SDK.xa_lib.TLMC_GetPositionLoopParams(
            handle, scenario_val, byref(loop_params), max_wait_val)
        position_loop_params[0] = loop_params
        return ret

    @staticmethod
    def get_power_params(handle, power_params, max_wait_in_milliseconds):
        power_params_val = TLMC_PowerParams()
        max_wait_val = c_int64(max_wait_in_milliseconds)
        ret = TLMC_SDK.xa_lib.TLMC_GetPowerParams(
            handle, byref(power_params_val, max_wait_val))
        power_params[0] = power_params_val
        return ret

    @staticmethod
    def get_profiled_mode_params(handle, profiled_params, max_wait_in_milliseconds):
        profiled_params_val = TLMC_ProfiledModeParams()
        max_wait_val = c_int64(max_wait_in_milliseconds)
        ret = TLMC_SDK.xa_lib.TLMC_GetProfiledModeParams(
            handle, byref(profiled_params_val), max_wait_val)
        profiled_params[0] = profiled_params_val
        return ret

    @staticmethod
    def get_rack_bay_occupied_state(handle, bay_number, occupied_state, max_wait_in_milliseconds):
        state_val = c_uint8[0]
        bay_number_val = bay_number 
        max_wait_val = c_int64(max_wait_in_milliseconds)
        ret = TLMC_SDK.xa_lib.TLMC_GetRackBayOccupiedState(
            handle, byref(bay_number_val), byref(state_val), max_wait_val)
        occupied_state[0] = state_val
        return ret

    @staticmethod
    def get_rich_response(handle, rich_response):
        response_val = TLMC_RichResponse()
        ret = TLMC_SDK.xa_lib.TLMC_GetRichResponse(handle, byref(response_val))
        rich_response[0] = response_val
        return ret

    @staticmethod
    def get_setting(handle, pSettings_name, TLMC_setting, max_wait_in_milliseconds):
        settings_val = TLMC_Setting()
        pSettings_name_val = create_string_buffer(
            pSettings_name.encode("utf-8"))
        max_wait_in_milliseconds = c_uint16(max_wait_in_milliseconds)
        ret = TLMC_SDK.xa_lib.TLMC_GetSetting(
            handle, pSettings_name_val, byref(settings_val), max_wait_in_milliseconds)
        TLMC_setting[0] = settings_val
        return ret

    @staticmethod
    def get_setting_count(handle, count):
        count_val = c_uint16(0)
        ret = TLMC_SDK.xa_lib.TLMC_GetSettingCount(handle, byref(count_val))
        count[0] = count_val
        return ret

    @staticmethod
    def get_setting_discrete_values(handle, pSettings_name, buffer, buffer_length, result_length):
        settings_name_val = create_string_buffer(
            pSettings_name.encode("utf-8"))
        buffer_val = create_string_buffer(buffer)
        buffer_length_val = c_uint(buffer_length)
        result_length_val = c_uint(result_length)
        ret = TLMC_SDK.xa_lib.TLMC_GetSettingCount(handle, byref(
            settings_name_val), buffer_val, buffer_length_val, result_length_val)
        return ret

    @staticmethod
    def get_settings(handle, source_start_index, number_of_items, TLMC_setting, number_of_items_copied):
        TLMC_setting_struct = TLMC_Setting()
        start_index_val = c_uint16(source_start_index)
        memory_block_size = number_of_items * sizeof(TLMC_setting_struct)
        p_memory_block = create_string_buffer(b"0", memory_block_size)
        items_copied_val = c_uint16(number_of_items_copied)
        ret = TLMC_SDK.xa_lib.TLMC_GetSettings(handle, start_index_val, c_uint16(
            number_of_items), byref(p_memory_block), byref(items_copied_val))
        for i in range(items_copied_val.value):
            new_block = create_string_buffer(b"0", sizeof(TLMC_Setting))
            memmove(byref(new_block), (addressof(p_memory_block) +
                    i * sizeof(TLMC_Setting)), sizeof(new_block))
            var = cast(addressof(new_block), POINTER(TLMC_Setting))
            TLMC_setting[i] = copy.copy(var.contents)
        return ret

    @staticmethod
    def get_settings_as_string(handle, buffer, buffer_length, result_length, TLMC_setting_string_format, include_read_only_items):
        buffer_val = create_string_buffer(buffer)
        buffer_length_val = c_uint(buffer_length)
        result_length_val = c_uint(result_length)
        read_only_items_val = c_bool(include_read_only_items)
        ret = TLMC_SDK.xa_lib.TLMC_GetSettingsAsString(handle, byref(buffer_val), buffer_length_val, result_length_val,
                                                       TLMC_setting_string_format, read_only_items_val)
        return ret

    @staticmethod
    def get_status_item(handle, status_item_id, status_item):
        status_item_val = TLMC_StatusItem()
        ret = TLMC_SDK.xa_lib.TLMC_GetStatusItem(
            handle, status_item_id, byref(status_item_val))
        status_item[0] = status_item_val
        return ret

    @staticmethod
    def get_status_item_count(handle, count):
        count_val = c_uint16(0)
        ret = TLMC_SDK.xa_lib.TLMC_GetStatusItemCount(
            handle, byref(count_val))
        count[0] = count_val.value
        return ret

    @staticmethod
    def get_status_items(handle, start_index, number_of_items, status_items, number_of_items_copied):
        TLMC_status_struct = TLMC_StatusItem()
        start_index_val = c_uint16(start_index)
        memory_block_size = number_of_items * sizeof(TLMC_status_struct)
        p_memory_block = create_string_buffer(b"0", memory_block_size)
        item_copied_val = c_uint16(number_of_items_copied)
        new_block = create_string_buffer(b"0", sizeof(TLMC_StatusItem))
        ret = TLMC_SDK.xa_lib.TLMC_GetStatusItems(handle, start_index_val, c_uint16(number_of_items), byref(p_memory_block),
                                                  byref(item_copied_val))
        for i in range(item_copied_val.value):
            new_block = create_string_buffer(b"0", sizeof(TLMC_StatusItem))
            memmove(byref(new_block), (addressof(p_memory_block) +
                    i * sizeof(TLMC_StatusItem)), sizeof(new_block))
            var = cast(addressof(new_block), POINTER(TLMC_StatusItem))
            status_items[i] = copy.copy(var.contents)
        return ret

    @staticmethod
    def get_stage_axis_params(handle, stage_axis_params, max_wait_in_milliseconds):
        axis_params_val = TLMC_StageAxisParams()
        max_wait_val = c_int64(max_wait_in_milliseconds)
        ret = TLMC_SDK.xa_lib.TLMC_GetStageAxisParams(
            handle, byref(axis_params_val), max_wait_val)
        stage_axis_params[0] = axis_params_val
        return ret

    @staticmethod
    def get_stepper_loop_params(handle, loop_params, max_wait_in_milliseconds):
        loop_params_val = TLMC_StepperLoopParams()
        max_wait_val = c_int64(max_wait_in_milliseconds)
        ret = TLMC_SDK.xa_lib.TLMC_GetStepperLoopParams(
            handle, byref(loop_params_val), max_wait_val)
        loop_params[0] = loop_params_val
        return ret

    @staticmethod
    def get_stepper_status(handle, stepper_status, max_wait_in_milliseconds):
        status_val = TLMC_StepperStatus()
        max_wait_val = c_int64(max_wait_in_milliseconds)
        ret = TLMC_SDK.xa_lib.TLMC_GetStepperStatus(
            handle, byref(status_val), max_wait_val)
        stepper_status[0] = status_val
        return ret

    @staticmethod
    def get_track_settle_params(handle, settle_params, max_wait_in_milliseconds):
        settle_params_val = TLMC_TrackSettleParams()
        max_wait_val = c_int64(max_wait_in_milliseconds)
        ret = TLMC_SDK.xa_lib.TLMC_GetTrackSettleParams(
            handle, byref(settle_params_val), max_wait_val)
        settle_params[0] = settle_params_val
        return ret

    @staticmethod
    def get_trigger_params_for_dc_brushless(handle, trigger_params, max_wait_in_milliseconds):
        trigger_params_val = TLMC_TriggerParamsForDcBrushless
        max_wait_val = c_int64(max_wait_in_milliseconds)
        ret = TLMC_SDK.xa_lib.TLMC_GetTriggerParamsForDcBrushless(
            handle, byref(trigger_params_val), max_wait_val)
        trigger_params[0] = trigger_params_val
        return ret

    @staticmethod
    def get_trigger_params_for_stepper(handle, trigger_params, max_wait_in_milliseconds):
        trigger_params_val = TLMC_TriggerParamsForStepper()
        max_wait_val = c_int64(max_wait_in_milliseconds)
        ret = TLMC_SDK.xa_lib.TLMC_GetTriggerParamsForStepper(
            handle, byref(trigger_params_val), max_wait_val)
        trigger_params[0] = trigger_params_val
        return ret

    @staticmethod
    def get_universal_status(handle, universal_status, max_wait_in_milliseconds):
        status_val = TLMC_UniversalStatus()
        max_wait_val = c_int64(max_wait_in_milliseconds)
        ret = TLMC_SDK.xa_lib.TLMC_GetUniversalStatus(
            handle, byref(status_val), max_wait_val)
        universal_status[0] = status_val
        return ret

    @staticmethod
    def get_universal_status_bits(handle, status_bits, max_wait_in_milliseconds):
        status_val = TLMC_UniversalStatusBits()
        max_wait_val = c_int64(max_wait_in_milliseconds)
        ret = TLMC_SDK.xa_lib.TLMC_GetUniversalStatusBits(
            handle, byref(status_bits), max_wait_val)
        status_bits[0] = status_val
        return ret

    @staticmethod
    def get_velocity_params(handle, velocity_params, max_wait_in_milliseconds):
        velocity_params_val = TLMC_VelocityParams()
        max_wait_in_milliseconds_val = c_int64(max_wait_in_milliseconds)
        ret = TLMC_SDK.xa_lib.TLMC_GetVelocityParams(handle, byref(
            velocity_params_val), max_wait_in_milliseconds_val)
        velocity_params[0] = velocity_params_val
        return ret

    @staticmethod
    def home(handle, maxWaitInMilliseconds):
        maxWaitInMilliseconds_val = c_int64(maxWaitInMilliseconds)
        ret = TLMC_SDK.xa_lib.TLMC_Home(handle, maxWaitInMilliseconds_val)
        return ret

    @staticmethod
    def identify(handle):
        ret = TLMC_SDK.xa_lib.TLMC_Identify(handle)
        return ret

    @staticmethod
    def move(handle, mode, param, max_wait_in_milliseconds):
        param_val = c_int32(param)
        max_wait_in_milliseconds_val = c_int64(max_wait_in_milliseconds)
        ret = TLMC_SDK.xa_lib.TLMC_Move(
            handle, mode, param_val, max_wait_in_milliseconds_val)
        return ret

    @staticmethod
    def move_absolute(handle, move_mode, position, max_wait_in_milliseconds):
        position_val = position
        if move_mode == TLMC_MoveModes.MoveMode_AbsoluteToProgrammedPosition:
            position_val = TLMC_Wait.TLMC_Unused
        else:
            move_mode = TLMC_MoveModes.MoveMode_Absolute
            pass
        ret = TLMC_SDK.move(handle, move_mode,
                            position_val, max_wait_in_milliseconds)
        return ret

    @staticmethod
    def move_continuous(handle, direction, max_wait_in_milliseconds):
        if direction == TLMC_MoveDirection.Move_Direction_Reverse:
            move_mode = TLMC_MoveModes.MoveMode_ContinuousReverse
        else:
            move_mode = TLMC_MoveModes.MoveMode_ContinuousForward
        ret = TLMC_SDK.move(handle, move_mode,
                            TLMC_Wait.TLMC_Unused, max_wait_in_milliseconds)
        return ret

    @staticmethod
    def move_jog(handle, direction, max_wait_in_milliseconds):
        if direction == TLMC_MoveDirection.Move_Direction_Reverse:
            move_mode = TLMC_MoveModes.MoveMode_JogReverse
        else:
            move_mode = TLMC_MoveModes.MoveMode_JogForward
        ret = TLMC_SDK.move(handle, move_mode,
                            TLMC_Wait.TLMC_Unused, max_wait_in_milliseconds)
        return ret

    @staticmethod
    def move_relative(handle, move_mode, step_size, max_wait_in_milliseconds):
        step_size_val = step_size
        if move_mode == TLMC_MoveModes.MoveMode_RelativeByProgrammedDistance:
            step_size_val = TLMC_Wait.TLMC_Unused
            pass
        else:
            move_mode == TLMC_MoveModes.MoveMode_Relative
        ret = TLMC_SDK.move(handle, move_mode,
                            step_size_val, max_wait_in_milliseconds)
        return ret
    
    @staticmethod 
    def open(device, transport_type, operating_mode, device_handle):
        transport = None
        if type(transport_type) == TLMC_TransportTypes:
                transport = transport_type
                pass
        else:
                pass
        
        if TLMC_SDK.is_load:
            operating_modes_val = TLMC_OperatingModes(operating_mode)
            result_code_val = TLMC_SDK.xa_lib.TLMC_Open(device.encode(
                'utf-8'), transport, operating_modes_val, byref(device_handle))
            return result_code_val
        else:
            return -1

    @staticmethod
    def persist_params(handle, parameter_group_id):
        param_val = parameter_group_id
        ret = TLMC_SDK.xa_lib.TLMC_PersistParams(handle, param_val)
        return ret

    @staticmethod
    def pz_get_max_output_voltage_params(handle, max_output_voltage_params,
                                         max_wait_in_milliseconds):
        output_voltage_params_val = TLMC_PZ_MaxOutputVoltageParams()
        max_wait_val = c_int64(max_wait_in_milliseconds)
        ret = TLMC_SDK.xa_lib.TLMC_PZ_GetMaxOutputVoltageParams(
            handle, byref(output_voltage_params_val), max_wait_val)
        max_output_voltage_params[0] = output_voltage_params_val
        return ret

    @staticmethod
    def pz_get_max_travel(handle, max_travel, max_wait_in_milliseconds):
        max_travel_val = c_uint16(0)
        max_wait_val = c_int64(max_wait_in_milliseconds)
        ret = TLMC_SDK.xa_lib.TLMC_PZ_GetMaxTravel(
            handle, byref(max_travel_val), max_wait_val)
        max_travel[0] = max_travel_val
        return ret

    @staticmethod
    def pz_get_output_voltage(handle, output_voltage, max_wait_in_milliseconds):
        voltage_val = c_int16(0)
        max_wait_val = c_int64(max_wait_in_milliseconds)
        ret = TLMC_SDK.xa_lib.TLMC_PZ_GetOutputVoltage(
            handle, byref(voltage_val), max_wait_val)
        output_voltage[0] = voltage_val
        return ret

    @staticmethod
    def pz_get_output_voltage_control_source_params(handle, voltage_source_params, max_wait_in_milliseconds):
        source_params_val = TLMC_PZ_OutputVoltageControlSourceParams()
        max_wait_val = c_int64(max_wait_in_milliseconds)
        ret = TLMC_SDK.xa_lib.TLMC_PZ_GetOutputVoltageSourceParams(
            handle, byref(source_params_val), max_wait_val)
        voltage_source_params[0] = source_params_val
        return ret

    @staticmethod
    def pz_get_output_waveform_params(handle, waveform_params, max_wait_in_milliseconds):
        waveform_val = TLMC_PZ_OutputWaveformParams()
        max_wait_val = c_int64(max_wait_in_milliseconds)
        ret = TLMC_SDK.xa_lib.TLMC_PZ_GetOutputWaveformParams(
            handle, byref(waveform_val), max_wait_val)
        waveform_params[0] = waveform_val
        return ret

    @staticmethod
    def pz_get_position(handle, position, max_wait_in_milliseconds):
        position_val = c_int16(0)
        max_wait_val = c_int64(max_wait_in_milliseconds)
        ret = TLMC_SDK.xa_lib.TLMC_PZ_GetPosition(
            handle, byref(position_val), max_wait_val)
        position[0] = position_val
        return ret

    @staticmethod
    def pz_get_position_control_mode(handle, control_mode, max_wait_in_milliseconds):
        control_mode_val = TLMC_PZ_PositionControlMode()
        max_wait_val = c_int64(max_wait_in_milliseconds)
        ret = TLMC_SDK.xa_lib.TLMC_PZ_GetPositionControlMode(
            handle, byref(control_mode_val), max_wait_val)
        control_mode[0] = control_mode_val
        return ret

    @staticmethod
    def pz_get_position_loop_params(handle, position_loop_params, max_wait_in_milliseconds):
        loop_params_val = TLMC_PZ_PositionLoopParams()
        max_wait_val = c_int64(max_wait_in_milliseconds)
        ret = TLMC_SDK.xa_lib.TLMC_PZ_GetPositionLoopParams(
            handle, byref(loop_params_val), max_wait_val)
        position_loop_params[0] = loop_params_val
        return ret

    @staticmethod
    def pz_get_slew_rate_params(handle, slew_rate_params, max_wait_in_milliseconds):
        slew_rate_params_val = TLMC_PZ_SlewRateParams()
        max_wait_val = c_int64(max_wait_in_milliseconds)
        ret = TLMC_SDK.xa_lib.TLMC_PZ_GetSlewRateParams(
            handle, byref(slew_rate_params_val), max_wait_val)
        slew_rate_params[0] = slew_rate_params_val
        return ret

    @staticmethod
    def pz_get_status(handle, status, max_wait_in_milliseconds):
        status_val = TLMC_PZ_Status()
        max_wait_val = c_int64(max_wait_in_milliseconds)
        ret = TLMC_SDK.xa_lib.TLMC_PZ_GetStatus(
            handle, byref(status_val), max_wait_val)
        status[0] = status_val
        return ret

    @staticmethod
    def pz_get_status_bits(handle, status_bits, max_wait_in_milliseconds):
        status_bits_val = TLMC_PZ_StatusBits()
        max_wait_val = c_int64(max_wait_in_milliseconds)
        ret = TLMC_SDK.xa_lib.TLMC_PZ.GetStatusBits(
            handle, byref(status_bits_val), max_wait_val)
        status_bits[0] = status_bits_val
        return ret

    @staticmethod
    def pz_set_max_output_voltage(handle, max_output_voltage):
        voltage_val = c_uint16(max_output_voltage)
        ret = TLMC_SDK.xa_lib.TLMC_PZ_SetMaxOutputVoltage(handle, voltage_val)
        return ret

    @staticmethod
    def pz_set_output_voltage(handle, new_output_voltage):
        voltage_val = c_int16(new_output_voltage)
        ret = TLMC_SDK.xa_lib.TLMC_PZ_SetMaxOutputVoltage(handle, voltage_val)
        return ret

    @staticmethod
    def pz_set_output_voltage_control_source_params(handle, voltage_source):
        source_val = voltage_source
        ret = TLMC_SDK.xa_lib.TLMC_PZ_SetOutputVoltageControlSourceParams(
            handle, source_val)

    @staticmethod
    def pz_set_output_waveform_lookup_table_sample(handle, index, voltage):
        params = TLMC_PZ_OutputWaveformLoopTableSample()
        params.index = c_uint16(index)
        params.voltage = c_int16(voltage)
        ret = TLMC_SDK.xa_lib.TLMC_PZ_SetOutputWaveformLookupTableSample(
            handle, byref(params))
        return ret

    @staticmethod
    def pz_set_output_waveform_params(handle, mode, num_of_samples_per_cycle,
                                      num_of_cycles, sample_delay, pre_cycle_delay,
                                      post_cycle_delay, output_trigger_start_index,
                                      output_trigger_width, num_of_samples_between_triggers):
        params = TLMC_PZ_OutputWaveformParams()
        params.mode = mode
        params.numberOfSamplesPerCycle = c_uint16(num_of_samples_per_cycle)
        params.numberOfCycles = c_uint16(num_of_cycles)
        params.interSampleDelay = c_int32(sample_delay)
        params.preCycleDelay = c_int32(pre_cycle_delay)
        params.postCycleDelay = c_int32(post_cycle_delay)
        params.outputTriggerStartIndex = c_uint16(output_trigger_start_index)
        params.outputTriggerWidth = c_int32(output_trigger_width)
        params.numberOfSamplesBetweenTriggerRepetition(
            num_of_samples_between_triggers)
        ret = TLMC_SDK.xa_lib.TLMC_PZ_SetOutputWaveformParams(
            handle, byref(params))
        return ret

    @staticmethod
    def pz_set_position(handle, new_position):
        position_val = c_int16(new_position)
        ret = TLMC_SDK.xa_lib.TLMC_PZ_SetPosition(handle, position_val)
        return ret

    @staticmethod
    def pz_set_position_control_mode(handle, new_control_mode):
        control_mode_val = new_control_mode
        ret = TLMC_SDK.xa_lib.TLMC_PZ_SetPositionControlMode(
            handle, control_mode_val)
        return ret

    @staticmethod
    def pz_set_position_loop_params(handle, proportional, integral):
        params = TLMC_PZ_PositionLoopParams()
        params.proportional = c_uint16(proportional)
        params.integral = c_uint16(integral)
        ret = TLMC_SDK.xa_lib.TLMC_PZ_SetPositionLoopParams(
            handle, byref(params))
        return ret

    @staticmethod
    def pz_set_slew_rate_params(handle, open_slew_rate, closed_slew_rate):
        params = TLMC_PZ_SlewRateParams()
        params.openSlewRate = c_uint16(open_slew_rate)
        params.closedSlewRate = c_uint16(closed_slew_rate)
        ret = TLMC_SDK.xa_lib.TLMC_PZ_SetSlewRateParams(handle, byref(params))
        return ret

    @staticmethod
    def pz_set_zero(handle, max_wait_in_milliseconds):
        max_wait_val = c_int64(max_wait_in_milliseconds)
        ret = TLMC_SDK.xa_lib.TLMC_PZ_SetZero(handle, max_wait_val)
        return ret

    @staticmethod
    def pz_start_output_waveform(handle):
        ret = TLMC_SDK.xa_lib.TLMC_PZ_StartOutputWaveform(handle)
        return ret

    @staticmethod
    def pz_stop_output_waveform(handle):
        ret = TLMC_SDK.xa_lib.TLMC_PZ_StopOutputWaveform(handle)
        return ret

    @staticmethod
    def rack_identify(handle, channel):
        channel_val = c_uint8(channel)
        ret = TLMC_SDK.xa_lib.TLMC_RackIdentify(handle, channel_val)
        return ret

    @staticmethod
    def remove_simulation(description):
        check = json.dumps(description)
        ret = TLMC_SDK.xa_lib.TLMC_RemoveSimulation(c_char_p(check.encode('utf-8')))
        return ret

    @staticmethod
    def restore_factory_defaults(handle):
        ret = TLMC_SDK.xa_lib.TLMC_RestoreFactoryDefaults(handle)
        return ret

    @staticmethod
    def set_analog_monitor_configuration_params(handle, monitor_number, motor_channel, system_variable, scale, offset):
        monitor_val = monitor_number
        params = TLMC_AnalogMonitorConfigurationParams
        params.motorChannel = motor_channel
        params.systemVariable = system_variable
        params.scale = c_int32(scale)
        params.offset = c_int32(offset)
        ret = TLMC_SDK.xa_lib.TLMC_SetAnalogMonitorConfigurationParams(
            handle, monitor_val, byref(params))
        return ret

    @staticmethod
    def set_aux_io_port_mode(handle, port_number, new_mode):
        mode_val = new_mode
        port_number_val = port_number
        ret = TLMC_SDK.xa_lib.SetAuxIoPortMode(
            handle, port_number_val, mode_val)
        return ret

    @staticmethod
    def set_aux_io_software_states(handle, new_state):
        states_val = c_uint16(new_state)
        ret = TLMC_SDK.xa_lib.TLMC_SetAuxIoSoftwareStates(handle, states_val)
        return ret

    @staticmethod
    def set_bow_index(handle, new_bow_index):
        index_val = new_bow_index 
        ret = TLMC_SDK.xa_lib.TLMC_SetBowIndex(handle, index_val)
        return ret

     
    @staticmethod
    def set_connected_product(handle, product_name):
        raw_val = product_name.encode('utf-8') 
        ret = TLMC_SDK.xa_lib.TLMC_SetConnectedProduct(handle, raw_val)
        return ret

    @staticmethod
    def set_connected_product_info(handle, product_name, axis_type, movement_type, unit_type,
                                   distance_scale_factor, velocity_scale_factor,
                                   acceleration_scale_factor, min_position, max_position,
                                   max_velocity, max_acceleration):
        params = TLMC_ConnectedProductInfo()
        params.productName = c_char(product_name)
        params.axisType = axis_type
        params.movementType = movement_type
        params.unitType = unit_type
        params.distanceScaleFactor = c_double(distance_scale_factor)
        params.velocityScaleFactor = c_double(velocity_scale_factor)
        params.accelerationScaleFactor = c_double(acceleration_scale_factor)
        params.minPosition = c_double(min_position)
        params.maxPosition = c_double(max_position)
        params.maxvelcoity = c_double(max_velocity)
        params.maxAcceleration = c_double(max_acceleration)
        ret = TLMC_SDK.xa_lib.TLMC_SetConnectedProductInfo(
            handle, byref(params))
        return ret

    @staticmethod
    def set_current_loop_params(handle, loop_scenario, phase, proportional, integral,
                                integral_limit, integral_dead_band, feed_fwrd):
        scenario_val = loop_scenario
        params = TLMC_CurrentLoopParams()
        params.phase = phase
        params.proportional = c_uint16(proportional)
        params.integral = c_uint16(integral)
        params.intgralLimit = c_uint16(integral_limit)
        params.integralDeadBand = c_uint16(integral_dead_band)
        params.feedForward = c_uint16(feed_fwrd)
        ret = TLMC_SDK.xa_lib.TLMC_SetCurrentLoopParams(
            handle, scenario_val, byref(params))
        return ret

    @staticmethod
    def set_dc_pid_params(handle, proportional, integral, derivative, integral_limit, filter_control):
        params = TLMC_DcPidParams()
        params.proportional = c_uint32(proportional)
        params.integral = c_uint32(integral)
        params.derivative = c_uint32(derivative)
        params.integralLimit = c_uint32(integral_limit)
        params.filterControl = filter_control
        ret = TLMC_SDK.xa_lib.TLMC_SetDcPidParams(handle, byref(params))
        return ret

    @staticmethod
    def set_digital_output_states(handle, new_output_state):
        output_state_val = new_output_state 
        ret = TLMC_SDK.xa_lib.TLMC_SetDigitalOutputStates(
            handle, output_state_val)
        return ret

    @staticmethod
    def set_enable_state(handle, channel_enable_state):
        channel_enable_state = TLMC_ChannelEnableStates.ChannelEnabled
        verification_max_wait_in_milliseconds_val = c_int64(
            TLMC_Wait.TLMC_InfiniteWait)
        ret = TLMC_SDK.xa_lib.TLMC_SetEnableState(
            handle, channel_enable_state, verification_max_wait_in_milliseconds_val)
        return ret

    @staticmethod
    def set_encoder_counter(handle, new_encoder_counter):
        encoder_val = c_int32(new_encoder_counter)
        ret = TLMC_SDK.xa_lib.TLMC_SetEncoderCounter(handle, encoder_val)
        return ret

    @staticmethod
    def set_end_of_message_mode(handle, new_mode):
        ret = TLMC_SDK.xa_lib.TLMC_SetEndOfMessageMode(handle, new_mode)
        return ret

    @staticmethod
    def set_general_move_params(handle, backlash_distance):
        params = TLMC_GeneralMoveParams(backlash_distance)
        ret = TLMC_SDK.xa_lib.TLMC_SetGeneralMoveParams(handle, byref(params))
        return ret

    @staticmethod
    def set_home_params(handle, direction, limit_switch, velocity, offset_distance):
        params = TLMC_HomeParams()
        params.direction = direction
        params.limitSwitch = limit_switch
        params.velocity = c_uint32(velocity)
        params.offsetDistance = c_int32(offset_distance)
        ret = TLMC_SDK.xa_lib.TLMC_SetHomeParams(handle, byref(params))
        return ret

    @staticmethod
    def set_io_configuration_params(handle, port_number, mode, trigger_out_source):
        port_val = port_number
        params = TLMC_IoConfigurationParams()
        params.mode = mode
        params.triggerOutSource = trigger_out_source
        ret = TLMC_SDK.xa_lib.TLMC_SetIoConfigurationParams(
            handle, port_val, byref(params))
        return ret

    @staticmethod
    def set_io_position_trigger_enable_state(handle, new_enable_state, max_wait_in_milliseconds):
        enable_state_val = new_enable_state
        max_wait_in_milliseconds_val = c_int64(max_wait_in_milliseconds)
        ret = TLMC_SDK.xa_lib.TLMC_SetIoPositionTriggerEnableState(
            handle, enable_state_val, max_wait_in_milliseconds_val)
        return ret

    @staticmethod
    def set_io_trigger_params(handle, trigger_in_mode, trigger_in_polarity,
                              trigger_in_source, trigger_out_mode, trigger_out_polarity,
                              trigger_out_forward_start_position, trigger_out_forward_interval,
                              trigger_out_forward_number_of_pulses, trigger_out_reverse_start_position,
                              trigger_out_reverse_interval, trigger_out_reverse_number_of_pulses,
                              trigger_out_pulse_width, trigger_out_number_of_cycles):
        params = TLMC_IoTriggerParams()
        params.triggerInMode = trigger_in_mode
        params.triggerInPolarity = trigger_in_polarity
        params.triggerInSource = trigger_in_source
        params.triggerOutMode = trigger_out_mode
        params.triggerOutPolarity = trigger_out_polarity
        params.triggerOutForwardStartPosition = c_int32(
            trigger_out_forward_start_position)
        params.triggerOutForwardInterval = c_int32(
            trigger_out_forward_interval)
        params.triggerOutForwardNumberOfPulses = c_int32(
            trigger_out_forward_number_of_pulses)
        params.triggerOutReverseStartPosition = c_int32(
            trigger_out_reverse_start_position)
        params.triggerOutReverseInterval = c_int32(
            trigger_out_reverse_interval)
        params.triggerOutReverseNumberOPulses = c_int32(
            trigger_out_reverse_number_of_pulses)
        params.triggerOutPulseWidth = c_uint32(trigger_out_pulse_width)
        params.triggerOutNumberOfCycles = c_uint32(
            trigger_out_number_of_cycles)
        ret = TLMC_SDK.xa_lib.TLMC_SetIoTriggerParams(handle, byref(params))
        return ret

    @staticmethod
    def set_joystick_params(handle, low_gear_velocity, high_gear_velocity, low_gear_acceleration, high_gear_acceleration, direction_sense):
        params = TLMC_JoystickParams()
        params.lowGearMaxVelocity = c_uint32(low_gear_velocity)
        params.highGearMaxVelocity = c_uint32(high_gear_velocity)
        params.lowGearAcceleration = c_uint32(low_gear_acceleration)
        params.highGearAcceleration = c_uint32(high_gear_acceleration)
        params.directionSense = direction_sense
        ret = TLMC_SDK.xa_lib.TLMC_SetJoystickParams(handle, byref(params))
        return ret

    @staticmethod
    def set_kcube_io_trigger_params(handle, trigger_one_mode, trigger_one_polarity,
                                    trigger_two_mode, trigger_two_polarity):
        params = TLMC_KcubeIoTriggerParams
        params.trigger1Mode = trigger_one_mode
        params.trigger1Polarity = trigger_one_polarity
        params.trigger2Mode = trigger_two_mode
        params.trigger2Polarity = trigger_two_polarity
        ret = TLMC_SDK.xa_lib.TLMC_SetKcubeIoTriggerParams(
            handle, byref(params))
        return ret

    @staticmethod
    def set_kcube_mmi_lock_state(handle, lock_state):
        ret = TLMC_SDK.xa_lib.TLMC_SetKcubeMmiLockState(handle, lock_state)
        return ret

    @staticmethod
    def set_kcube_mmi_params(handle, joystick_mode, joystick_velocity, joystick_acceleration,
                             joystick_direction_sense, position_one, position_two,
                             display_brightness, display_timeout, display_dim_level,
                             position_three, joystick_sensitivity):
        params = TLMC_KcubeMmiParams()
        params.joystickMode = joystick_mode
        params.joystickMaxVelocity = c_uint32(joystick_velocity)
        params.joystickAcceleration = c_uint32(joystick_acceleration)
        params.joystickDirectionSense = joystick_direction_sense
        params.presetPosition1 = c_int32(position_one)
        params.presetPosition2 = c_int32(position_two)
        params.displayBrightness = c_uint16(display_brightness)
        params.displayTimeout = c_uint16(display_timeout)
        params.displayDimLevel = c_uint16(display_dim_level)
        params.presetPosition3 = c_int32(position_three)
        params.joystickSensitivity = c_uint16(joystick_sensitivity)
        ret = TLMC_SDK.xa_lib.TLMC_SetKcubeMmiParams(handle, byref(params))
        return ret

    @staticmethod
    def set_kcube_position_trigger_params(handle, fwrd_start_position, fwrd_interval,
                                          fwrd_number_of_pulses, rev_start_position,
                                          rev_interval, rev_number_of_pulses, pulse_width,
                                          number_of_cycles):
        params = TLMC_KcubePositionTriggerParams()
        params.forwardStartPosition = c_int32(fwrd_start_position)
        params.forwardInterval = c_uint32(fwrd_interval)
        params.forwardNumberOfPulses = c_uint32(fwrd_number_of_pulses)
        params.reverseStartPosition = c_int32(rev_start_position)
        params.reverseInterval = c_uint32(rev_interval)
        params.reverseNumberOfPulses = c_uint32(rev_number_of_pulses)
        params.pulseWidth = c_uint32(pulse_width)
        params.numberOfCycles = c_uint32(number_of_cycles)
        ret = TLMC_SDK.xa_lib.TLMC_SetKcubePositionTriggerParams(
            handle, byref(params))
        return ret

    @staticmethod
    def set_lcd_display_params(handle, knob_sensitivity, display_brightness, display_timeout,
                               display_dim_level):
        params = TLMC_LcdDisplayParams()
        params.knobSensitivity = c_int16(knob_sensitivity)
        params.displayBrightness = c_uint16(display_brightness)
        params.displayTimeout = c_uint16(display_timeout)
        params.displayDimLevel = c_uint16(display_dim_level)
        ret = TLMC_SDK.xa_lib.TLMC_SetLcdDisplayParams(handle, byref(params))
        return ret

    @staticmethod
    def set_lcd_move_params(handle, knob_mode, jog_step_size, acceleration,
                            max_velocity, jog_stop_mode, preset_position):
        params = TLMC_LcdMoveParams()
        params.knobMode = knob_mode 
        params.jogStepSize = c_int32(jog_step_size)
        params.acceleration = c_int32(acceleration)
        params.maxVelocity = c_int32(max_velocity)
        params.jogStopMode = jog_stop_mode
        params.presetPosition = c_int32(preset_position)
        ret = TLMC_SDK.xa_lib.TLMC_SetLcdMoveParams(handle, byref(params))
        return ret

    @staticmethod
    def set_limit_switch_params(handle, clockwise_mode, counter_clockwise_mode, clockwise_soft_limit,
                                counter_clockwise_soft_limit, soft_limit_operating_mode):
        params = TLMC_LimitSwitchParams()
        params.clockwiseHardLimitOperatingMode = clockwise_mode
        params.counterclockwiseHardLimitOperatingMode = counter_clockwise_mode
        params.clockwiseSoftLimit = clockwise_soft_limit 
        params.counterclockwiseSoftLimit = counter_clockwise_soft_limit 
        params.softLimitOperatingMode = soft_limit_operating_mode
        ret = TLMC_SDK.xa_lib.TLMC_SetLimitSwitchParams(handle, byref(params))
        return ret

    @staticmethod
    def set_motor_output_params(handle, current_limit, energy_limit, motor_limit, motor_bias):
        params = TLMC_MotorOutputParams()
        params.continuousCurrentLimit = c_uint16(current_limit)
        params.energyLimit = c_uint16(energy_limit)
        params.motorLimit = c_uint16(motor_limit)
        params.motorBias = c_uint16(motor_bias)
        ret = TLMC_SDK.xa_lib.TLMC_SetMotorOutputParams(handle, byref(params))
        return ret

    @staticmethod
    def set_move_absolute_params(handle, absolute_position):
        params = TLMC_MoveAbsoluteParams(c_int32(absolute_position))
        ret = TLMC_SDK.xa_lib.TLMC_SetMoveAbsoluteParams(handle, byref(params))
        return ret

    @staticmethod
    def set_move_jog_params(handle, jog_mode, step_size, min_velocity, max_velocity, acceleration, stop_mode):
        params = TLMC_JogParams()
        params.mode = jog_mode
        params.stepSize = c_int32(step_size)
        params.minVelocity = c_uint32(min_velocity)
        params.acceleration = c_uint32(acceleration)
        params.maxVelocity = c_uint32(max_velocity)
        params.stopMode = stop_mode
        ret = TLMC_SDK.xa_lib.TLMC_SetJogParams(handle, byref(params))
        return ret

    @staticmethod
    def set_move_relative_params(handle, relative_distance):
        params = TLMC_MoveRelativeParams(relative_distance)
        ret = TLMC_SDK.xa_lib.TLMC_SetMoveRelativeParams(handle, byref(params))
        return ret

    @staticmethod
    def set_position_counter(handle, new_position_counter):
        position_val = c_int32(new_position_counter)
        ret = TLMC_SDK.xa_lib.TLMC_SetPositionCounter(handle, position_val)
        return ret

    @staticmethod
    def set_position_loop_params(handle, position_loop_scenario, proportional, integral, integral_limit,
                                 derivative, servo_cycles, scale, velocity_feed_fwrd,
                                 acceleration_feed_fwrd, error_limit):
        scenario_val = position_loop_scenario
        params = TLMC_PositionLoopParams
        params.proportional = c_uint16(proportional)
        params.integral = c_uint16(integral)
        params.integralLimit = c_uint32(integral_limit)
        params.derivative = c_uint16(derivative)
        params.servoCycles = c_uint16(servo_cycles)
        params.scale = c_uint16(scale)
        params.velocityFeedForward = c_uint16(velocity_feed_fwrd)
        params.accelerationFeedForward = c_uint16(acceleration_feed_fwrd)
        params.errorLimit = c_uint32(error_limit)
        ret = TLMC_SDK.xa_lib.TLMC_SetPositionLoopParams(
            handle, scenario_val, byref(params))
        return ret

    @staticmethod
    def set_power_params(handle, rest_factor, move_factor):
        params = TLMC_PowerParams()
        params.restFactor = c_uint16(rest_factor)
        params.moveFactor = c_uint16(move_factor)
        ret = TLMC_SDK.xa_lib.TLMC_SetPowerParams(handle, byref(params))
        return ret

    @staticmethod
    def set_profiled_mode_params(handle, mode, jerk):
        params = TLMC_ProfiledModeParams()
        params.mode = mode
        params.jerk = c_uint32(jerk)
        ret = TLMC_SDK.xa_lib.TLMC_SetProfiledModeParams(handle, byref(params))
        return ret

    @staticmethod
    def set_setting(handle, pSettings_name):
        TLMC_val = TLMC_Value()
        pSettings_name_val = c_char(pSettings_name)
        ret = TLMC_SDK.xa_lib.TLMC_SetSetting(
            handle, pSettings_name_val, TLMC_val)
        return ret

    @staticmethod
    def set_settings_from_string(handle, pSettings_name):
        pSettings_name_val = create_string_buffer(
            pSettings_name.encode("utf-8"))
        ret = TLMC_SDK.xa_lib.TLMC_SetSettingsFromString(
            handle, pSettings_name_val)
        return ret

    @staticmethod
    def set_stage_axis_params(handle, type_id, axis_id, part_number, serial_number,
                              counts_per_unit, min_position, max_position,
                              max_acceleration, max_decceleration, max_velcoity,
                              gear_box_ratio):
        params = TLMC_StageAxisParams()
        params.typeId = type_id 
        params.axisId = axis_id 
        params.partNumber = c_char(part_number)
        params.serialNumber = c_uint32(serial_number)
        params.countsPerUnit = c_uint32(counts_per_unit)
        params.minPosition = c_int32(min_position)
        params.maxPosition = c_int32(max_position)
        params.maxAcceleration = c_uint32(max_acceleration)
        params.maxDecceleration = c_uint32(max_decceleration)
        params.maxVelocity = c_uint32(max_velcoity)
        params.gearBoxRatio = c_uint16(gear_box_ratio)
        ret = TLMC_SDK.xa_lib.TLMC_SetStageAxisParams(handle, byref(params))
        return ret

    @staticmethod
    def set_status_mode(handle, operating_mode):
        ret = TLMC_SDK.xa_lib.TLMC_SetStatusMode(handle, operating_mode)
        return ret

    @staticmethod
    def set_stepper_loop_params(handle, loop_mode, proportional, integral,
                                differential, output_clip, output_tolerance,
                                microsteps_per_ecount):
        params = TLMC_StepperLoopParams()
        params.mode = loop_mode
        params.proportional = c_int32(proportional)
        params.integral = c_int32(integral)
        params.differential = c_int32(differential)
        params.outputClip = c_int32(output_clip)
        params.outputTolerance = c_int32(output_tolerance)
        params.microstepsPerEncoderCount = c_uint32(microsteps_per_ecount)
        ret = TLMC_SDK.xa_lib.TLMC_SetStepperLoopParams(handle, byref(params))
        return ret

    @staticmethod
    def set_track_settle_params(handle, settle_time, settle_window, track_window):
        params = TLMC_TrackSettleParams()
        params.settleTime = c_uint16(settle_time)
        params.settleWindow = c_uint16(settle_window)
        params.trackWindow = c_uint16(track_window)
        ret = TLMC_SDK.xa_lib.TLMC_SetTrackSettleParams(handle, byref(params))
        return ret

    @staticmethod
    def set_trigger_params_for_dc_brushless(handle, mode):
        params = TLMC_TriggerParamsForDcBrushless()
        params.mode = mode
        ret = TLMC_SDK.xa_lib.TLMC_SetTriggerParamsForDcBrushless(
            handle, byref(params))
        return ret

    @staticmethod
    def set_trigger_params_for_stepper(handle, trigger_mode):
        params = TLMC_TriggerParamsForStepper()
        params.mode = trigger_mode
        ret = TLMC_SDK.xa_lib.TLMC_SetTriggerParamsForStepper(
            handle, byref(params))
        return ret

    @staticmethod
    def set_velocity_params(handle, min_velocity, acceleration, max_velocity):
        params = TLMC_VelocityParams()
        params.minVelocity = c_uint32(min_velocity)
        params.acceleration = c_uint32(acceleration)
        params.maxVelocity = c_uint32(max_velocity)
        ret = TLMC_SDK.xa_lib.TLMC_SetVelocityParams(handle, byref(params))
        return ret

    @staticmethod
    def shutdown():
        ret = TLMC_SDK.xa_lib.TLMC_Shutdown()
        return ret

    @staticmethod
    def startup(pSettings_file_name):
        ret = 0
        ret = TLMC_SDK.xa_lib.TLMC_Startup(pSettings_file_name)
        return ret

    @staticmethod
    def stop(handle, stop_mode, max_wait_in_milliseconds):
        max_wait_in_milliseconds_val = c_int64(max_wait_in_milliseconds)
        ret = TLMC_SDK.xa_lib.TLMC_Stop(
            handle, stop_mode, max_wait_in_milliseconds_val)
        return ret
