# tlmc_core.py  — Patched for Windows x64 (__stdcall) against tlmc_xa_native_api.h
# - Corrects symbol names, buffer handling, pointer usage, and sizes.
# - Uses UTF-8 for all strings passed to the DLL.
# - Fixes out-params: always allocate ctypes object/struct -> byref -> write back to list[0].
# - Keeps function names used by higher-level XASDK but routes to correct TLMC_* exports.
#
# Requires: xa_sdk/shared/tlmc_type_structures.py to define all TLMC_* ctypes Structures/enums.

from ctypes import (
    WinDLL, c_uint32, c_uint16, c_uint8, c_int16, c_int32, c_int64, c_double, c_bool,
    c_char_p, POINTER, byref, create_string_buffer
)
import os
from pathlib import Path
import json

# Import native structs/enums defined to match the header
from xa_sdk.shared.tlmc_type_structures import *  # noqa: F401,F403


class TLMC_SDK:
    is_load = False
    xa_lib = None

    @staticmethod
    def try_load_library(current_path: str):
        """
        Load tlmc_xa_native.dll from the given directory (Windows 64-bit).
        """
        dll_dir = Path(current_path).resolve()
        dll_path = dll_dir / "tlmc_xa_native.dll"

        if not dll_path.exists():
            raise FileNotFoundError(f"DLL not found at {dll_path}")

        # Limit DLL search to the given dir (Python 3.8+)
        if hasattr(os, "add_dll_directory"):
            os.add_dll_directory(str(dll_dir))
        else:
            os.environ["PATH"] = str(dll_dir) + os.pathsep + os.environ.get("PATH", "")

        TLMC_SDK.xa_lib = WinDLL(str(dll_path))
        TLMC_SDK.is_load = True

        # You can set argtypes/restype here for the functions you call most often.
        # Return type for all TLMC_* APIs is ResultCode (uint16).
        lib = TLMC_SDK.xa_lib
        lib.TLMC_Startup.argtypes = [c_char_p]
        lib.TLMC_Startup.restype = c_uint16
        lib.TLMC_Shutdown.argtypes = []
        lib.TLMC_Shutdown.restype = c_uint16

        lib.TLMC_AddUserMessageToLog.argtypes = [c_char_p]
        lib.TLMC_AddUserMessageToLog.restype = c_uint16

        lib.TLMC_Open.argtypes = [c_char_p, c_char_p, c_uint32, POINTER(c_uint32)]
        lib.TLMC_Open.restype = c_uint16
        lib.TLMC_Close.argtypes = [c_uint32]
        lib.TLMC_Close.restype = c_uint16

        lib.TLMC_GetDeviceListItemCount.argtypes = [POINTER(c_uint16)]
        lib.TLMC_GetDeviceListItemCount.restype = c_uint16

        lib.TLMC_GetDigitalInputStates.argtypes = [c_uint32, POINTER(c_uint32), c_int64]
        lib.TLMC_GetDigitalInputStates.restype = c_uint16
        lib.TLMC_GetDigitalOutputStates.argtypes = [c_uint32, POINTER(c_uint8), c_int64]
        lib.TLMC_GetDigitalOutputStates.restype = c_uint16
        lib.TLMC_SetDigitalOutputStates.argtypes = [c_uint32, c_uint8]
        lib.TLMC_SetDigitalOutputStates.restype = c_uint16

        lib.TLMC_ConvertFromDeviceToPhysical.argtypes = [c_uint32, c_uint16, c_int64, POINTER(c_double), POINTER(c_uint16)]
        lib.TLMC_ConvertFromDeviceToPhysical.restype = c_uint16
        lib.TLMC_ConvertFromPhysicalToDevice.argtypes = [c_uint32, c_uint16, c_uint16, c_double, POINTER(c_int64)]
        lib.TLMC_ConvertFromPhysicalToDevice.restype = c_uint16

        lib.TLMC_GetConnectedProduct.argtypes = [c_uint32, c_char_p, c_uint32]
        lib.TLMC_GetConnectedProduct.restype = c_uint16

        lib.TLMC_SetConnectedProduct.argtypes = [c_uint32, c_char_p]
        lib.TLMC_SetConnectedProduct.restype = c_uint16

        lib.TLMC_SetConnectedProductInfo.argtypes = [
            c_uint32,  # handle
            c_char_p,  # productName
            c_uint16, c_uint16, c_uint16,  # axisType, movementType, unitType
            c_double, c_double, c_double,  # distanceSF, velocitySF, accelerationSF
            c_double, c_double,  # minPos, maxPos
            c_double, c_double,  # maxVel, maxAcc
        ]
        lib.TLMC_SetConnectedProductInfo.restype = c_uint16

        lib.TLMC_PZ_SetOutputVoltage.argtypes = [c_uint32, c_int16]
        lib.TLMC_PZ_SetOutputVoltage.restype = c_uint16
        lib.TLMC_PZ_GetStatusBits.argtypes = [c_uint32, POINTER(c_uint32), c_int64]
        lib.TLMC_PZ_GetStatusBits.restype = c_uint16

        # (Extend with more argtypes/restype as needed; the rest of the wrapper
        # passes correctly-typed ctypes objects already.)

    # ----- System / lifecycle -----

    @staticmethod
    def startup(pSettings_file_name: str):
        p = None if pSettings_file_name is None else pSettings_file_name.encode('utf-8')
        return TLMC_SDK.xa_lib.TLMC_Startup(p)

    @staticmethod
    def shutdown():
        return TLMC_SDK.xa_lib.TLMC_Shutdown()

    @staticmethod
    def add_user_message_to_log(user_message: str):
        return TLMC_SDK.xa_lib.TLMC_AddUserMessageToLog(user_message.encode('utf-8'))

    # ----- Open/Close/Disconnect -----

    @staticmethod
    def open(device: str, transport: str, operating_mode: int, device_handle):
        dev = device.encode('utf-8') if device else None
        trn = transport.encode('utf-8') if transport else None
        return TLMC_SDK.xa_lib.TLMC_Open(dev, trn, c_uint32(operating_mode), byref(device_handle))

    @staticmethod
    def close(handle):
        return TLMC_SDK.xa_lib.TLMC_Close(handle)

    @staticmethod
    def disconnect(handle):
        return TLMC_SDK.xa_lib.TLMC_Disconnect(handle)

    # ----- Conversion -----

    @staticmethod
    def convert_from_device_units_to_physical(handle, tlmc_scale_type, device_value, physical_value_out):
        """Return physical value; unit is retrieved but not exposed (to keep high-level API stable)."""
        pv = c_double(0.0)
        unit = c_uint16(0)
        rc = TLMC_SDK.xa_lib.TLMC_ConvertFromDeviceToPhysical(
            handle, c_uint16(tlmc_scale_type), c_int64(device_value), byref(pv), byref(unit)
        )
        if rc == 0:
            physical_value_out[0] = pv.value
        return rc

    @staticmethod
    def convert_from_physical_to_device(handle, tlmc_scale_type, tlmc_unit_type, physical_value, device_value_out):
        dv = c_int64(0)
        rc = TLMC_SDK.xa_lib.TLMC_ConvertFromPhysicalToDevice(
            handle, c_uint16(tlmc_scale_type), c_uint16(tlmc_unit_type), c_double(physical_value), byref(dv)
        )
        if rc == 0:
            device_value_out[0] = dv.value
        return rc

    # ----- Simulation -----

    @staticmethod
    def create_simulation(description: dict):
        contents = json.dumps(description).encode('utf-8')
        return TLMC_SDK.xa_lib.TLMC_CreateSimulation(contents)

    @staticmethod
    def remove_simulation(description: dict):
        contents = json.dumps(description).encode('utf-8')
        return TLMC_SDK.xa_lib.TLMC_RemoveSimulation(contents)

    # ----- Device list / device info -----

    @staticmethod
    def get_device_list_item_count(count):
        cv = c_uint16(0)
        rc = TLMC_SDK.xa_lib.TLMC_GetDeviceListItemCount(byref(cv))
        if rc == 0:
            count[0] = cv.value
        return rc

    @staticmethod
    def get_device_list_items(source_start_index, number_of_items, tlmc_device_info_list, number_of_items_copied):
        ArrayType = TLMC_DeviceInfo * number_of_items
        dest = ArrayType()
        copied = c_uint16(0)
        rc = TLMC_SDK.xa_lib.TLMC_GetDeviceListItems(
            c_uint16(source_start_index), c_uint16(number_of_items), dest, byref(copied)
        )
        if rc == 0:
            tlmc_device_info_list[:] = [dest[i] for i in range(copied.value)]
            number_of_items_copied[0] = copied.value
        return rc

    @staticmethod
    def get_device_info(handle, device_info):
        info = TLMC_DeviceInfo()
        rc = TLMC_SDK.xa_lib.TLMC_GetDeviceInfo(handle, byref(info))
        if rc == 0:
            device_info[0] = info
        return rc

    # ----- Strings / Settings -----

    @staticmethod
    def get_connected_product(handle, connected_product_out, buffer_len=TLMC_ConnectedProductNameBufferLength if 'TLMC_ConnectedProductNameBufferLength' in globals() else 64):
        buf = create_string_buffer(buffer_len)
        rc = TLMC_SDK.xa_lib.TLMC_GetConnectedProduct(handle, buf, c_uint32(buffer_len))
        if rc == 0:
            connected_product_out[0] = buf.value.decode('utf-8', errors='ignore')
        return rc

    @staticmethod
    def get_connected_product_info(handle, product_info):
        info = TLMC_ConnectedProductInfo()
        rc = TLMC_SDK.xa_lib.TLMC_GetConnectedProductInfo(handle, byref(info))
        if rc == 0:
            product_info[0] = info
        return rc

    @staticmethod
    def get_connected_products_supported(handle, connected_products_out, buffer_len=256):
        buf = create_string_buffer(buffer_len)
        result_len = c_uint32(0)
        rc = TLMC_SDK.xa_lib.TLMC_GetConnectedProductsSupported(handle, buf, c_uint32(buffer_len), byref(result_len))
        if rc == 0:
            connected_products_out[0] = buf.value.decode('utf-8', errors='ignore')
        return rc

    @staticmethod
    def get_setting(handle, settings_name: str, tlmc_setting_out, max_wait_in_milliseconds):
        st = TLMC_Setting()
        name = settings_name.encode("utf-8")
        rc = TLMC_SDK.xa_lib.TLMC_GetSetting(handle, name, byref(st), c_int64(max_wait_in_milliseconds))
        if rc == 0:
            tlmc_setting_out[0] = st
        return rc

    @staticmethod
    def get_setting_count(handle, count_out):
        cv = c_uint16(0)
        rc = TLMC_SDK.xa_lib.TLMC_GetSettingCount(handle, byref(cv))
        if rc == 0:
            count_out[0] = cv.value
        return rc

    @staticmethod
    def get_setting_discrete_values(handle, settings_name: str, buffer, buffer_length, result_length_out):
        name = settings_name.encode("utf-8")
        res_len = c_uint32(0)
        # 'buffer' must be created by caller with create_string_buffer(buffer_length)
        rc = TLMC_SDK.xa_lib.TLMC_GetSettingDiscreteValues(handle, name, buffer, c_uint32(buffer_length), byref(res_len))
        if rc == 0 and result_length_out is not None:
            result_length_out[0] = res_len.value
        return rc

    @staticmethod
    def get_settings(handle, source_start_index, number_of_items, tlmc_settings_out, number_of_items_copied_out):
        ArrayType = TLMC_Setting * number_of_items
        dest = ArrayType()
        copied = c_uint16(0)
        rc = TLMC_SDK.xa_lib.TLMC_GetSettings(
            handle, c_uint16(source_start_index), c_uint16(number_of_items), dest, byref(copied)
        )
        if rc == 0:
            tlmc_settings_out[:] = [dest[i] for i in range(copied.value)]
            number_of_items_copied_out[0] = copied.value
        return rc

    @staticmethod
    def get_settings_as_string(handle, buffer, buffer_length, result_length_out, tlmc_setting_string_format, include_read_only_items):
        res_len = c_uint32(0)
        rc = TLMC_SDK.xa_lib.TLMC_GetSettingsAsString(
            handle, buffer, c_uint32(buffer_length), byref(res_len), c_uint8(tlmc_setting_string_format), c_bool(include_read_only_items)
        )
        if rc == 0 and result_length_out is not None:
            result_length_out[0] = res_len.value
        return rc

    @staticmethod
    def set_setting(handle, settings_name: str, value: TLMC_Value):
        # Header: TLMC_SetSetting(hDevice, const char* name, const union TLMC_Value* pNewValue)
        name = settings_name.encode('utf-8')
        return TLMC_SDK.xa_lib.TLMC_SetSetting(handle, name, byref(value))

    @staticmethod
    def set_settings_from_string(handle, settings_json: str):
        return TLMC_SDK.xa_lib.TLMC_SetSettingsFromString(handle, settings_json.encode("utf-8"))

    @staticmethod
    def set_connected_product(handle, product_name: str):
        pn = product_name.encode('utf-8')
        return TLMC_SDK.xa_lib.TLMC_SetConnectedProduct(handle, pn)

    @staticmethod
    def set_connected_product_info(
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
    ):
        pn = product_name.encode('utf-8')
        return TLMC_SDK.xa_lib.TLMC_SetConnectedProductInfo(
            handle,
            pn,
            c_uint16(axis_type),
            c_uint16(movement_type),
            c_uint16(unit_type),
            c_double(distance_scale_factor),
            c_double(velocity_scale_factor),
            c_double(acceleration_scale_factor),
            c_double(min_position),
            c_double(max_position),
            c_double(max_velocity),
            c_double(max_acceleration),
        )

    # ----- Status items -----

    @staticmethod
    def get_status_item(handle, status_item_id, status_item_out):
        si = TLMC_StatusItem()
        rc = TLMC_SDK.xa_lib.TLMC_GetStatusItem(handle, c_int32(status_item_id), byref(si))
        if rc == 0:
            status_item_out[0] = si
        return rc

    @staticmethod
    def get_status_item_count(handle, count_out):
        cv = c_uint16(0)
        rc = TLMC_SDK.xa_lib.TLMC_GetStatusItemCount(handle, byref(cv))
        if rc == 0:
            count_out[0] = cv.value
        return rc

    @staticmethod
    def get_status_items(handle, start_index, number_of_items, status_items_out, number_of_items_copied_out):
        ArrayType = TLMC_StatusItem * number_of_items
        dest = ArrayType()
        copied = c_uint16(0)
        rc = TLMC_SDK.xa_lib.TLMC_GetStatusItems(
            handle, c_uint16(start_index), c_uint16(number_of_items), dest, byref(copied)
        )
        if rc == 0:
            status_items_out[:] = [dest[i] for i in range(copied.value)]
            number_of_items_copied_out[0] = copied.value
        return rc

    # ----- Motion, general params -----

    @staticmethod
    def get_adc_inputs(handle, adc_inputs_out, max_wait_in_milliseconds):
        vals = TLMC_AdcInputs()
        rc = TLMC_SDK.xa_lib.TLMC_GetAdcInputs(handle, byref(vals), c_int64(max_wait_in_milliseconds))
        if rc == 0:
            adc_inputs_out[0] = vals
        return rc

    @staticmethod
    def get_aux_io_port_mode(handle, port_number, port_mode_out, max_wait_in_milliseconds):
        mode = c_uint16(0)
        rc = TLMC_SDK.xa_lib.TLMC_GetAuxIoPortMode(handle, c_uint16(port_number), byref(mode), c_int64(max_wait_in_milliseconds))
        if rc == 0:
            port_mode_out[0] = mode.value
        return rc

    @staticmethod
    def set_aux_io_port_mode(handle, port_numbers_mask, new_mode):
        # Header param is 'portNumbers' (bitmask). Allow caller to pass one or more bits.
        return TLMC_SDK.xa_lib.TLMC_SetAuxIoPortMode(handle, c_uint16(port_numbers_mask), c_uint16(new_mode))

    @staticmethod
    def get_aux_io_software_states(handle, software_states_out, max_wait_in_milliseconds):
        states = c_uint16(0)
        rc = TLMC_SDK.xa_lib.TLMC_GetAuxIoSoftwareStates(handle, byref(states), c_int64(max_wait_in_milliseconds))
        if rc == 0:
            software_states_out[0] = states.value
        return rc

    @staticmethod
    def set_aux_io_software_states(handle, new_states):
        return TLMC_SDK.xa_lib.TLMC_SetAuxIoSoftwareStates(handle, c_uint16(new_states))

    @staticmethod
    def get_bow_index(handle, bow_index_out, max_wait_in_milliseconds):
        idx = c_uint16(0)
        rc = TLMC_SDK.xa_lib.TLMC_GetBowIndex(handle, byref(idx), c_int64(max_wait_in_milliseconds))
        if rc == 0:
            bow_index_out[0] = idx.value
        return rc

    @staticmethod
    def set_bow_index(handle, new_bow_index):
        return TLMC_SDK.xa_lib.TLMC_SetBowIndex(handle, c_uint16(new_bow_index))

    @staticmethod
    def get_current_loop_params(handle, loop_scenario, params_out, max_wait_in_milliseconds):
        params = TLMC_CurrentLoopParams()
        rc = TLMC_SDK.xa_lib.TLMC_GetCurrentLoopParams(handle, c_uint16(loop_scenario), byref(params), c_int64(max_wait_in_milliseconds))
        if rc == 0:
            params_out[0] = params
        return rc

    @staticmethod
    def set_current_loop_params(handle, loop_scenario, phase, proportional, integral, integral_limit, integral_dead_band, feed_fwrd):
        params = TLMC_CurrentLoopParams()
        params.phase = c_uint16(phase)
        params.proportional = c_uint16(proportional)
        params.integral = c_uint16(integral)
        params.integralLimit = c_uint16(integral_limit)
        params.integralDeadBand = c_uint16(integral_dead_band)
        params.feedForward = c_uint16(feed_fwrd)
        return TLMC_SDK.xa_lib.TLMC_SetCurrentLoopParams(handle, c_uint16(loop_scenario), byref(params))

    @staticmethod
    def get_dc_pid_params(handle, pid_params_out, max_wait_in_milliseconds):
        params = TLMC_DcPidParams()
        rc = TLMC_SDK.xa_lib.TLMC_GetDcPidParams(handle, byref(params), c_int64(max_wait_in_milliseconds))
        if rc == 0:
            pid_params_out[0] = params
        return rc

    @staticmethod
    def set_dc_pid_params(handle, proportional, integral, derivative, integral_limit, filter_control):
        params = TLMC_DcPidParams()
        params.proportional = c_uint32(proportional)
        params.integral = c_uint32(integral)
        params.derivative = c_uint32(derivative)
        params.integralLimit = c_uint32(integral_limit)
        params.filterControl = c_uint16(filter_control)
        return TLMC_SDK.xa_lib.TLMC_SetDcPidParams(handle, byref(params))

    @staticmethod
    def get_digital_input_states(handle, input_state_out, max_wait_in_milliseconds):
        st = c_uint32(0)  # 32-bit bitfield
        rc = TLMC_SDK.xa_lib.TLMC_GetDigitalInputStates(handle, byref(st), c_int64(max_wait_in_milliseconds))
        if rc == 0:
            input_state_out[0] = st.value
        return rc

    @staticmethod
    def get_digital_output_states(handle, output_state_out, max_wait_in_milliseconds):
        st = c_uint8(0)
        rc = TLMC_SDK.xa_lib.TLMC_GetDigitalOutputStates(handle, byref(st), c_int64(max_wait_in_milliseconds))
        if rc == 0:
            output_state_out[0] = st.value
        return rc

    @staticmethod
    def set_digital_output_states(handle, new_output_state):
        return TLMC_SDK.xa_lib.TLMC_SetDigitalOutputStates(handle, c_uint8(new_output_state))

    @staticmethod
    def get_enable_state(handle, enable_state_out, max_wait_in_milliseconds):
        st = c_uint8(0)
        rc = TLMC_SDK.xa_lib.TLMC_GetEnableState(handle, byref(st), c_int64(max_wait_in_milliseconds))
        if rc == 0:
            enable_state_out[0] = st.value
        return rc

    @staticmethod
    def set_enable_state(handle, new_enable_state, verification_max_wait_ms=-1):
        return TLMC_SDK.xa_lib.TLMC_SetEnableState(handle, c_uint8(new_enable_state), c_int64(verification_max_wait_ms))

    @staticmethod
    def get_encoder_counter(handle, encoder_counter_out, max_wait_in_milliseconds):
        val = c_int32(0)
        rc = TLMC_SDK.xa_lib.TLMC_GetEncoderCounter(handle, byref(val), c_int64(max_wait_in_milliseconds))
        if rc == 0:
            encoder_counter_out[0] = val.value
        return rc

    @staticmethod
    def set_encoder_counter(handle, new_encoder_counter):
        return TLMC_SDK.xa_lib.TLMC_SetEncoderCounter(handle, c_int32(new_encoder_counter))

    @staticmethod
    def get_general_move_params(handle, params_out, max_wait_in_milliseconds):
        params = TLMC_GeneralMoveParams()
        rc = TLMC_SDK.xa_lib.TLMC_GetGeneralMoveParams(handle, byref(params), c_int64(max_wait_in_milliseconds))
        if rc == 0:
            params_out[0] = params
        return rc

    @staticmethod
    def set_general_move_params(handle, backlash_distance):
        params = TLMC_GeneralMoveParams()
        params.backlashDistance = c_int32(backlash_distance)
        return TLMC_SDK.xa_lib.TLMC_SetGeneralMoveParams(handle, byref(params))

    @staticmethod
    def get_hardware_info(handle, hardware_info_out, max_wait_in_milliseconds):
        info = TLMC_HardwareInfo()
        rc = TLMC_SDK.xa_lib.TLMC_GetHardwareInfo(handle, byref(info), c_int64(max_wait_in_milliseconds))
        if rc == 0:
            hardware_info_out[0] = info
        return rc

    @staticmethod
    def get_home_params(handle, home_params_out, max_wait_in_milliseconds):
        params = TLMC_HomeParams()
        rc = TLMC_SDK.xa_lib.TLMC_GetHomeParams(handle, byref(params), c_int64(max_wait_in_milliseconds))
        if rc == 0:
            home_params_out[0] = params
        return rc

    @staticmethod
    def set_home_params(handle, direction, limit_switch, velocity, offset_distance):
        params = TLMC_HomeParams()
        params.direction = c_uint16(direction)
        params.limitSwitch = c_uint16(limit_switch)
        params.velocity = c_uint32(velocity)
        params.offsetDistance = c_int32(offset_distance)
        return TLMC_SDK.xa_lib.TLMC_SetHomeParams(handle, byref(params))

    @staticmethod
    def get_io_configuration_number_of_ports_supported(handle, number_of_ports_out):
        n = c_uint8(0)
        rc = TLMC_SDK.xa_lib.TLMC_GetIoConfigurationNumberOfPortsSupported(handle, byref(n))
        if rc == 0:
            number_of_ports_out[0] = n.value
        return rc

    @staticmethod
    def get_io_configuration_params(handle, port_number, params_out, max_wait_in_milliseconds):
        params = TLMC_IoConfigurationParams()
        rc = TLMC_SDK.xa_lib.TLMC_GetIoConfigurationParams(handle, c_uint16(port_number), byref(params), c_int64(max_wait_in_milliseconds))
        if rc == 0:
            params_out[0] = params
        return rc

    @staticmethod
    def set_io_configuration_params(handle, port_number, mode, trigger_out_source):
        params = TLMC_IoConfigurationParams()
        params.mode = c_uint16(mode)
        params.triggerOutSource = c_uint16(trigger_out_source)
        return TLMC_SDK.xa_lib.TLMC_SetIoConfigurationParams(handle, c_uint16(port_number), byref(params))

    @staticmethod
    def get_io_position_trigger_enable_state(handle, enable_state_out, max_wait_in_milliseconds):
        st = c_uint8(0)
        rc = TLMC_SDK.xa_lib.TLMC_GetIoPositionTriggerEnableState(handle, byref(st), c_int64(max_wait_in_milliseconds))
        if rc == 0:
            enable_state_out[0] = st.value
        return rc

    @staticmethod
    def set_io_position_trigger_enable_state(handle, new_enable_state, verification_max_wait_ms):
        return TLMC_SDK.xa_lib.TLMC_SetIoPositionTriggerEnableState(handle, c_uint8(new_enable_state), c_int64(verification_max_wait_ms))

    @staticmethod
    def get_io_trigger_params(handle, io_trigger_params_out, max_wait_in_milliseconds):
        params = TLMC_IoTriggerParams()
        rc = TLMC_SDK.xa_lib.TLMC_GetIoTriggerParams(handle, byref(params), c_int64(max_wait_in_milliseconds))
        if rc == 0:
            io_trigger_params_out[0] = params
        return rc

    @staticmethod
    def set_io_trigger_params(handle, *args):
        (trigger_in_mode, trigger_in_polarity, trigger_in_source,
         trigger_out_mode, trigger_out_polarity,
         trig_fwd_start_pos, trig_fwd_interval, trig_fwd_num_pulses,
         trig_rev_start_pos, trig_rev_interval, trig_rev_num_pulses,
         trig_out_pulse_width, trig_out_num_cycles) = args

        params = TLMC_IoTriggerParams()
        params.triggerInMode = c_uint16(trigger_in_mode)
        params.triggerInPolarity = c_uint16(trigger_in_polarity)
        params.triggerInSource = c_uint16(trigger_in_source)
        params.triggerOutMode = c_uint16(trigger_out_mode)
        params.triggerOutPolarity = c_uint16(trigger_out_polarity)
        params.triggerOutForwardStartPosition = c_int32(trig_fwd_start_pos)
        params.triggerOutForwardInterval = c_int32(trig_fwd_interval)
        params.triggerOutForwardNumberOfPulses = c_int32(trig_fwd_num_pulses)
        params.triggerOutReverseStartPosition = c_int32(trig_rev_start_pos)
        params.triggerOutReverseInterval = c_int32(trig_rev_interval)
        params.triggerOutReverseNumberOfPulses = c_int32(trig_rev_num_pulses)
        params.triggerOutPulseWidth = c_uint32(trig_out_pulse_width)
        params.triggerOutNumberOfCycles = c_uint32(trig_out_num_cycles)
        return TLMC_SDK.xa_lib.TLMC_SetIoTriggerParams(handle, byref(params))

    @staticmethod
    def get_jog_params(handle, jog_params_out, max_wait_in_milliseconds):
        params = TLMC_JogParams()
        rc = TLMC_SDK.xa_lib.TLMC_GetJogParams(handle, byref(params), c_int64(max_wait_in_milliseconds))
        if rc == 0:
            jog_params_out[0] = params
        return rc

    @staticmethod
    def set_jog_params(handle, jog_mode, step_size, min_velocity, max_velocity, acceleration, stop_mode):
        params = TLMC_JogParams()
        params.mode = c_uint16(jog_mode)
        params.stepSize = c_int32(step_size)
        params.minVelocity = c_uint32(min_velocity)
        params.acceleration = c_uint32(acceleration)
        params.maxVelocity = c_uint32(max_velocity)
        params.stopMode = c_uint16(stop_mode)
        return TLMC_SDK.xa_lib.TLMC_SetJogParams(handle, byref(params))

    @staticmethod
    def get_joystick_params(handle, joystick_params_out, max_wait_in_milliseconds):
        params = TLMC_JoystickParams()
        rc = TLMC_SDK.xa_lib.TLMC_GetJoystickParams(handle, byref(params), c_int64(max_wait_in_milliseconds))
        if rc == 0:
            joystick_params_out[0] = params
        return rc

    @staticmethod
    def set_joystick_params(handle, low_gear_velocity, high_gear_velocity, low_gear_acceleration, high_gear_acceleration, direction_sense):
        params = TLMC_JoystickParams()
        params.lowGearMaxVelocity = c_uint32(low_gear_velocity)
        params.highGearMaxVelocity = c_uint32(high_gear_velocity)
        params.lowGearAcceleration = c_uint32(low_gear_acceleration)
        params.highGearAcceleration = c_uint32(high_gear_acceleration)
        params.directionSense = c_uint16(direction_sense)
        return TLMC_SDK.xa_lib.TLMC_SetJoystickParams(handle, byref(params))

    @staticmethod
    def get_kcube_io_trigger_params(handle, kcube_io_params_out, max_wait_in_milliseconds):
        params = TLMC_KcubeIoTriggerParams()
        rc = TLMC_SDK.xa_lib.TLMC_GetKcubeIoTriggerParams(handle, byref(params), c_int64(max_wait_in_milliseconds))
        if rc == 0:
            kcube_io_params_out[0] = params
        return rc

    @staticmethod
    def set_kcube_io_trigger_params(handle, trigger_one_mode, trigger_one_polarity, trigger_two_mode, trigger_two_polarity):
        params = TLMC_KcubeIoTriggerParams()
        params.trigger1Mode = c_uint16(trigger_one_mode)
        params.trigger1Polarity = c_uint16(trigger_one_polarity)
        params.trigger2Mode = c_uint16(trigger_two_mode)
        params.trigger2Polarity = c_uint16(trigger_two_polarity)
        return TLMC_SDK.xa_lib.TLMC_SetKcubeIoTriggerParams(handle, byref(params))

    @staticmethod
    def get_kcube_mmi_lock_state(handle, lock_state_out, max_wait_in_milliseconds):
        val = c_uint8(0)
        rc = TLMC_SDK.xa_lib.TLMC_GetKcubeMmiLockState(handle, byref(val), c_int64(max_wait_in_milliseconds))
        if rc == 0:
            lock_state_out[0] = val.value
        return rc

    @staticmethod
    def set_kcube_mmi_lock_state(handle, lock_state):
        return TLMC_SDK.xa_lib.TLMC_SetKcubeMmiLockState(handle, c_uint8(lock_state))

    @staticmethod
    def get_kcube_mmi_params(handle, mmi_params_out, max_wait_in_milliseconds):
        params = TLMC_KcubeMmiParams()
        rc = TLMC_SDK.xa_lib.TLMC_GetKcubeMmiParams(handle, byref(params), c_int64(max_wait_in_milliseconds))
        if rc == 0:
            mmi_params_out[0] = params
        return rc

    @staticmethod
    def set_kcube_mmi_params(handle, joystick_mode, joystick_velocity, joystick_acceleration,
                             joystick_direction_sense, position_one, position_two,
                             display_brightness, display_timeout, display_dim_level,
                             position_three, joystick_sensitivity):
        params = TLMC_KcubeMmiParams()
        params.joystickMode = c_uint16(joystick_mode)
        params.joystickMaxVelocity = c_uint32(joystick_velocity)
        params.joystickAcceleration = c_uint32(joystick_acceleration)
        params.joystickDirectionSense = c_uint16(joystick_direction_sense)
        params.presetPosition1 = c_int32(position_one)
        params.presetPosition2 = c_int32(position_two)
        params.displayBrightness = c_uint16(display_brightness)
        params.displayTimeout = c_uint16(display_timeout)
        params.displayDimLevel = c_uint16(display_dim_level)
        params.presetPosition3 = c_int32(position_three)
        params.joystickSensitivity = c_uint16(joystick_sensitivity)
        return TLMC_SDK.xa_lib.TLMC_SetKcubeMmiParams(handle, byref(params))

    @staticmethod
    def get_kcube_position_trigger_params(handle, kcube_trigger_params_out, max_wait_in_milliseconds):
        params = TLMC_KcubePositionTriggerParams()
        rc = TLMC_SDK.xa_lib.TLMC_GetKcubePositionTriggerParams(handle, byref(params), c_int64(max_wait_in_milliseconds))
        if rc == 0:
            kcube_trigger_params_out[0] = params
        return rc

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
        return TLMC_SDK.xa_lib.TLMC_SetKcubePositionTriggerParams(handle, byref(params))

    @staticmethod
    def get_lcd_display_params(handle, lcd_display_params_out, max_wait_in_milliseconds):
        params = TLMC_LcdDisplayParams()
        rc = TLMC_SDK.xa_lib.TLMC_GetLcdDisplayParams(handle, byref(params), c_int64(max_wait_in_milliseconds))
        if rc == 0:
            lcd_display_params_out[0] = params
        return rc

    @staticmethod
    def set_lcd_display_params(handle, knob_sensitivity, display_brightness, display_timeout, display_dim_level):
        params = TLMC_LcdDisplayParams()
        params.knobSensitivity = c_int16(knob_sensitivity)
        params.displayBrightness = c_uint16(display_brightness)
        params.displayTimeout = c_uint16(display_timeout)
        params.displayDimLevel = c_uint16(display_dim_level)
        return TLMC_SDK.xa_lib.TLMC_SetLcdDisplayParams(handle, byref(params))

    @staticmethod
    def get_lcd_move_params(handle, lcd_move_params_out, max_wait_in_milliseconds):
        params = TLMC_LcdMoveParams()
        rc = TLMC_SDK.xa_lib.TLMC_GetLcdMoveParams(handle, byref(params), c_int64(max_wait_in_milliseconds))
        if rc == 0:
            lcd_move_params_out[0] = params
        return rc

    @staticmethod
    def set_lcd_move_params(handle, knob_mode, jog_step_size, acceleration, max_velocity, jog_stop_mode, preset_position):
        params = TLMC_LcdMoveParams()
        params.knobMode = c_uint16(knob_mode)
        params.jogStepSize = c_int32(jog_step_size)
        params.acceleration = c_int32(acceleration)
        params.maxVelocity = c_int32(max_velocity)
        params.jogStopMode = c_uint16(jog_stop_mode)
        # Only set first preset index for compatibility with previous API
        params.presetPosition[0] = c_int32(preset_position)
        return TLMC_SDK.xa_lib.TLMC_SetLcdMoveParams(handle, byref(params))

    @staticmethod
    def get_limit_switch_params(handle, limit_switch_params_out, max_wait_in_milliseconds):
        params = TLMC_LimitSwitchParams()
        rc = TLMC_SDK.xa_lib.TLMC_GetLimitSwitchParams(handle, byref(params), c_int64(max_wait_in_milliseconds))
        if rc == 0:
            limit_switch_params_out[0] = params
        return rc

    @staticmethod
    def set_limit_switch_params(handle, clockwise_mode, counter_clockwise_mode, clockwise_soft_limit, counter_clockwise_soft_limit, soft_limit_operating_mode):
        params = TLMC_LimitSwitchParams()
        params.clockwiseHardLimitOperatingMode = c_uint16(clockwise_mode)
        params.counterclockwiseHardLimitOperatingMode = c_uint16(counter_clockwise_mode)
        params.clockwiseSoftLimit = c_int32(clockwise_soft_limit)
        params.counterclockwiseSoftLimit = c_int32(counter_clockwise_soft_limit)
        params.softLimitOperatingMode = c_uint16(soft_limit_operating_mode)
        return TLMC_SDK.xa_lib.TLMC_SetLimitSwitchParams(handle, byref(params))

    @staticmethod
    def get_motor_output_params(handle, motor_output_params_out, max_wait_in_milliseconds):
        params = TLMC_MotorOutputParams()
        rc = TLMC_SDK.xa_lib.TLMC_GetMotorOutputParams(handle, byref(params), c_int64(max_wait_in_milliseconds))
        if rc == 0:
            motor_output_params_out[0] = params
        return rc

    @staticmethod
    def set_motor_output_params(handle, current_limit, energy_limit, motor_limit, motor_bias):
        params = TLMC_MotorOutputParams()
        params.continuousCurrentLimit = c_uint16(current_limit)
        params.energyLimit = c_uint16(energy_limit)
        params.motorLimit = c_uint16(motor_limit)
        params.motorBias = c_uint16(motor_bias)
        return TLMC_SDK.xa_lib.TLMC_SetMotorOutputParams(handle, byref(params))

    @staticmethod
    def get_move_absolute_params(handle, move_absolute_params_out, max_wait_in_milliseconds):
        params = TLMC_MoveAbsoluteParams()
        rc = TLMC_SDK.xa_lib.TLMC_GetMoveAbsoluteParams(handle, byref(params), c_int64(max_wait_in_milliseconds))
        if rc == 0:
            move_absolute_params_out[0] = params
        return rc

    @staticmethod
    def set_move_absolute_params(handle, absolute_position):
        params = TLMC_MoveAbsoluteParams()
        params.absolutePosition = c_int32(absolute_position)
        return TLMC_SDK.xa_lib.TLMC_SetMoveAbsoluteParams(handle, byref(params))

    @staticmethod
    def get_move_relative_params(handle, move_relative_params_out, max_wait_in_milliseconds):
        params = TLMC_MoveRelativeParams()
        rc = TLMC_SDK.xa_lib.TLMC_GetMoveRelativeParams(handle, byref(params), c_int64(max_wait_in_milliseconds))
        if rc == 0:
            move_relative_params_out[0] = params
        return rc

    @staticmethod
    def set_move_relative_params(handle, relative_distance):
        params = TLMC_MoveRelativeParams()
        params.relativeDistance = c_int32(relative_distance)
        return TLMC_SDK.xa_lib.TLMC_SetMoveRelativeParams(handle, byref(params))

    @staticmethod
    def get_position_counter(handle, position_counter_out, max_wait_in_milliseconds):
        val = c_int32(0)
        rc = TLMC_SDK.xa_lib.TLMC_GetPositionCounter(handle, byref(val), c_int64(max_wait_in_milliseconds))
        if rc == 0:
            position_counter_out[0] = val.value
        return rc

    @staticmethod
    def set_position_counter(handle, new_position_counter):
        return TLMC_SDK.xa_lib.TLMC_SetPositionCounter(handle, c_int32(new_position_counter))

    @staticmethod
    def get_position_loop_params(handle, position_loop_scenario, position_loop_params_out, max_wait_in_milliseconds):
        params = TLMC_PositionLoopParams()
        rc = TLMC_SDK.xa_lib.TLMC_GetPositionLoopParams(handle, c_uint16(position_loop_scenario), byref(params), c_int64(max_wait_in_milliseconds))
        if rc == 0:
            position_loop_params_out[0] = params
        return rc

    @staticmethod
    def set_position_loop_params(handle, position_loop_scenario, proportional, integral, integral_limit, derivative, servo_cycles, scale, velocity_feed_fwrd, acceleration_feed_fwrd, error_limit):
        params = TLMC_PositionLoopParams()
        params.proportional = c_uint16(proportional)
        params.integral = c_uint16(integral)
        params.integralLimit = c_uint32(integral_limit)
        params.derivative = c_uint16(derivative)
        params.servoCycles = c_uint16(servo_cycles)
        params.scale = c_uint16(scale)
        params.velocityFeedForward = c_uint16(velocity_feed_fwrd)
        params.accelerationFeedForward = c_uint16(acceleration_feed_fwrd)
        params.errorLimit = c_uint32(error_limit)
        return TLMC_SDK.xa_lib.TLMC_SetPositionLoopParams(handle, c_uint16(position_loop_scenario), byref(params))

    @staticmethod
    def get_power_params(handle, power_params_out, max_wait_in_milliseconds):
        params = TLMC_PowerParams()
        rc = TLMC_SDK.xa_lib.TLMC_GetPowerParams(handle, byref(params), c_int64(max_wait_in_milliseconds))
        if rc == 0:
            power_params_out[0] = params
        return rc

    @staticmethod
    def set_power_params(handle, rest_factor, move_factor):
        params = TLMC_PowerParams()
        params.restFactor = c_uint16(rest_factor)
        params.moveFactor = c_uint16(move_factor)
        return TLMC_SDK.xa_lib.TLMC_SetPowerParams(handle, byref(params))

    @staticmethod
    def get_profiled_mode_params(handle, profiled_params_out, max_wait_in_milliseconds):
        params = TLMC_ProfileModeParams()
        rc = TLMC_SDK.xa_lib.TLMC_GetProfileModeParams(handle, byref(params), c_int64(max_wait_in_milliseconds))
        if rc == 0:
            profiled_params_out[0] = params
        return rc

    @staticmethod
    def set_profiled_mode_params(handle, mode, jerk):
        params = TLMC_ProfileModeParams()
        params.mode = c_uint16(mode)
        params.jerk = c_uint32(jerk)
        return TLMC_SDK.xa_lib.TLMC_SetProfileModeParams(handle, byref(params))

    # ----- Piezo (PZ) -----

    @staticmethod
    def pz_get_max_output_voltage_params(handle, max_output_voltage_params_out, max_wait_in_milliseconds):
        params = TLMC_PZ_MaxOutputVoltageParams()
        rc = TLMC_SDK.xa_lib.TLMC_PZ_GetMaxOutputVoltageParams(handle, byref(params), c_int64(max_wait_in_milliseconds))
        if rc == 0:
            max_output_voltage_params_out[0] = params
        return rc

    @staticmethod
    def pz_set_max_output_voltage(handle, max_output_voltage):
        return TLMC_SDK.xa_lib.TLMC_PZ_SetMaxOutputVoltage(handle, c_uint16(max_output_voltage))

    @staticmethod
    def pz_get_max_travel(handle, max_travel_out, max_wait_in_milliseconds):
        val = c_uint16(0)
        rc = TLMC_SDK.xa_lib.TLMC_PZ_GetMaxTravel(handle, byref(val), c_int64(max_wait_in_milliseconds))
        if rc == 0:
            max_travel_out[0] = val.value
        return rc

    @staticmethod
    def pz_get_output_voltage(handle, output_voltage_out, max_wait_in_milliseconds):
        val = c_int16(0)
        rc = TLMC_SDK.xa_lib.TLMC_PZ_GetOutputVoltage(handle, byref(val), c_int64(max_wait_in_milliseconds))
        if rc == 0:
            output_voltage_out[0] = val.value
        return rc

    @staticmethod
    def pz_set_output_voltage(handle, new_output_voltage):
        return TLMC_SDK.xa_lib.TLMC_PZ_SetOutputVoltage(handle, c_int16(new_output_voltage))

    @staticmethod
    def pz_get_output_voltage_control_source_params(handle, voltage_source_params_out, max_wait_in_milliseconds):
        params = TLMC_PZ_OutputVoltageControlSourceParams()
        rc = TLMC_SDK.xa_lib.TLMC_PZ_GetOutputVoltageControlSourceParams(handle, byref(params), c_int64(max_wait_in_milliseconds))
        if rc == 0:
            voltage_source_params_out[0] = params
        return rc

    @staticmethod
    def pz_set_output_voltage_control_source_params(handle, source):
        params = TLMC_PZ_OutputVoltageControlSourceParams()
        params.source = c_uint16(source)
        return TLMC_SDK.xa_lib.TLMC_PZ_SetOutputVoltageControlSourceParams(handle, byref(params))

    @staticmethod
    def pz_set_output_waveform_lookup_table_sample(handle, index, voltage):
        sample = TLMC_PZ_OutputWaveformLookupTableSample()
        sample.index = c_uint16(index)
        sample.voltage = c_int16(voltage)
        return TLMC_SDK.xa_lib.TLMC_PZ_SetOutputWaveformLookupTableSample(handle, byref(sample))

    @staticmethod
    def pz_get_output_waveform_params(handle, waveform_params_out, max_wait_in_milliseconds):
        params = TLMC_PZ_OutputWaveformParams()
        rc = TLMC_SDK.xa_lib.TLMC_PZ_GetOutputWaveformParams(handle, byref(params), c_int64(max_wait_in_milliseconds))
        if rc == 0:
            waveform_params_out[0] = params
        return rc

    @staticmethod
    def pz_set_output_waveform_params(handle, mode, n_per_cycle, n_cycles, inter_delay, pre_delay, post_delay, trig_start_index, trig_width, n_between_triggers):
        params = TLMC_PZ_OutputWaveformParams()
        params.mode = c_uint16(mode)
        params.numberOfSamplesPerCycle = c_uint16(n_per_cycle)
        params.numberOfCycles = c_int32(n_cycles)
        params.interSampleDelay = c_int32(inter_delay)
        params.preCycleDelay = c_int32(pre_delay)
        params.postCycleDelay = c_int32(post_delay)
        params.outputTriggerStartIndex = c_uint16(trig_start_index)
        params.outputTriggerWidth = c_int32(trig_width)
        params.numberOfSamplesBetweenTriggerRepetition = c_uint16(n_between_triggers)
        return TLMC_SDK.xa_lib.TLMC_PZ_SetOutputWaveformParams(handle, byref(params))

    @staticmethod
    def pz_start_output_waveform(handle):
        return TLMC_SDK.xa_lib.TLMC_PZ_StartOutputWaveform(handle)

    @staticmethod
    def pz_stop_output_waveform(handle):
        return TLMC_SDK.xa_lib.TLMC_PZ_StopOutputWaveform(handle)

    @staticmethod
    def pz_get_position(handle, position_out, max_wait_in_milliseconds):
        pos = c_int16(0)
        rc = TLMC_SDK.xa_lib.TLMC_PZ_GetPosition(handle, byref(pos), c_int64(max_wait_in_milliseconds))
        if rc == 0:
            position_out[0] = pos.value
        return rc

    @staticmethod
    def pz_set_position(handle, new_position):
        return TLMC_SDK.xa_lib.TLMC_PZ_SetPosition(handle, c_int16(new_position))

    @staticmethod
    def pz_get_position_control_mode(handle, control_mode_out, max_wait_in_milliseconds):
        cm = c_uint16(0)
        rc = TLMC_SDK.xa_lib.TLMC_PZ_GetPositionControlMode(handle, byref(cm), c_int64(max_wait_in_milliseconds))
        if rc == 0:
            control_mode_out[0] = cm.value
        return rc

    @staticmethod
    def pz_set_position_control_mode(handle, new_control_mode, verification_max_wait_ms=-1):
        return TLMC_SDK.xa_lib.TLMC_PZ_SetPositionControlMode(handle, c_uint16(new_control_mode), c_int64(verification_max_wait_ms))

    @staticmethod
    def pz_get_position_loop_params(handle, position_loop_params_out, max_wait_in_milliseconds):
        params = TLMC_PZ_PositionLoopParams()
        rc = TLMC_SDK.xa_lib.TLMC_PZ_GetPositionLoopParams(handle, byref(params), c_int64(max_wait_in_milliseconds))
        if rc == 0:
            position_loop_params_out[0] = params
        return rc

    @staticmethod
    def pz_set_position_loop_params(handle, proportional, integral):
        params = TLMC_PZ_PositionLoopParams()
        params.proportional = c_uint16(proportional)
        params.integral = c_uint16(integral)
        return TLMC_SDK.xa_lib.TLMC_PZ_SetPositionLoopParams(handle, byref(params))

    @staticmethod
    def pz_get_slew_rate_params(handle, slew_rate_params_out, max_wait_in_milliseconds):
        params = TLMC_PZ_SlewRateParams()
        rc = TLMC_SDK.xa_lib.TLMC_PZ_GetSlewRateParams(handle, byref(params), c_int64(max_wait_in_milliseconds))
        if rc == 0:
            slew_rate_params_out[0] = params
        return rc

    @staticmethod
    def pz_set_slew_rate_params(handle, open_slew_rate, closed_slew_rate):
        params = TLMC_PZ_SlewRateParams()
        params.openLoopSlewRate = c_uint16(open_slew_rate)
        params.closedLoopSlewRate = c_uint16(closed_slew_rate)
        return TLMC_SDK.xa_lib.TLMC_PZ_SetSlewRateParams(handle, byref(params))

    @staticmethod
    def pz_get_status(handle, status_out, max_wait_in_milliseconds):
        st = TLMC_PZ_Status()
        rc = TLMC_SDK.xa_lib.TLMC_PZ_GetStatus(handle, byref(st), c_int64(max_wait_in_milliseconds))
        if rc == 0:
            status_out[0] = st
        return rc

    @staticmethod
    def pz_get_status_bits(handle, status_bits_out, max_wait_in_milliseconds):
        bits = c_uint32(0)
        rc = TLMC_SDK.xa_lib.TLMC_PZ_GetStatusBits(handle, byref(bits), c_int64(max_wait_in_milliseconds))
        if rc == 0:
            status_bits_out[0] = bits.value
        return rc

    @staticmethod
    def pz_set_zero(handle, max_wait_in_milliseconds):
        return TLMC_SDK.xa_lib.TLMC_PZ_SetZero(handle, c_int64(max_wait_in_milliseconds))

    # ----- Rack / Stage / Stepper / Universal -----

    @staticmethod
    def rack_identify(handle, channel):
        return TLMC_SDK.xa_lib.TLMC_RackIdentify(handle, c_uint8(channel))

    @staticmethod
    def get_rack_bay_occupied_state(handle, bay_number, occupied_state_out, max_wait_in_milliseconds):
        st = c_uint16(0)
        rc = TLMC_SDK.xa_lib.TLMC_GetRackBayOccupiedState(handle, c_uint16(bay_number), byref(st), c_int64(max_wait_in_milliseconds))
        if rc == 0:
            occupied_state_out[0] = st.value
        return rc

    @staticmethod
    def get_stage_axis_params(handle, stage_axis_params_out, max_wait_in_milliseconds):
        params = TLMC_StageAxisParams()
        rc = TLMC_SDK.xa_lib.TLMC_GetStageAxisParams(handle, byref(params), c_int64(max_wait_in_milliseconds))
        if rc == 0:
            stage_axis_params_out[0] = params
        return rc

    @staticmethod
    def set_stage_axis_params(handle, type_id, axis_id, part_number, serial_number,
                              counts_per_unit, min_position, max_position,
                              max_acceleration, max_deceleration, max_velocity, gear_box_ratio):
        params = TLMC_StageAxisParams()
        params.productId = c_uint16(type_id)
        params.axisId = c_uint16(axis_id)
        pn = part_number.encode('utf-8')
        if len(pn) >= 16:
            pn = pn[:15]
        params.partNumber = pn  # ctypes char[16] accepts bytes (zero-padded)
        params.serialNumber = c_uint32(serial_number)
        params.countsPerUnit = c_uint32(counts_per_unit)
        params.minPosition = c_int32(min_position)
        params.maxPosition = c_int32(max_position)
        params.maxAcceleration = c_uint32(max_acceleration)
        params.maxDeceleration = c_uint32(max_deceleration)
        params.maxVelocity = c_uint32(max_velocity)
        params.gearboxRatio = c_uint16(gear_box_ratio)
        return TLMC_SDK.xa_lib.TLMC_SetStageAxisParams(handle, byref(params))

    @staticmethod
    def get_stepper_loop_params(handle, stepper_loop_params_out, max_wait_in_milliseconds):
        params = TLMC_StepperLoopParams()
        rc = TLMC_SDK.xa_lib.TLMC_GetStepperLoopParams(handle, byref(params), c_int64(max_wait_in_milliseconds))
        if rc == 0:
            stepper_loop_params_out[0] = params
        return rc

    @staticmethod
    def set_stepper_loop_params(handle, loop_mode, proportional, integral, differential, output_clip, output_tolerance, microsteps_per_ecount):
        params = TLMC_StepperLoopParams()
        params.loopMode = c_uint16(loop_mode)
        params.proportional = c_int32(proportional)
        params.integral = c_int32(integral)
        params.differential = c_int32(differential)
        params.outputClip = c_int32(output_clip)
        params.outputTolerance = c_int32(output_tolerance)
        params.microstepsPerEncoderCount = c_uint32(microsteps_per_ecount)
        return TLMC_SDK.xa_lib.TLMC_SetStepperLoopParams(handle, byref(params))

    @staticmethod
    def get_stepper_status(handle, stepper_status_out, max_wait_in_milliseconds):
        st = TLMC_StepperStatus()
        rc = TLMC_SDK.xa_lib.TLMC_GetStepperStatus(handle, byref(st), c_int64(max_wait_in_milliseconds))
        if rc == 0:
            stepper_status_out[0] = st
        return rc

    @staticmethod
    def get_track_settle_params(handle, track_params_out, max_wait_in_milliseconds):
        params = TLMC_TrackSettleParams()
        rc = TLMC_SDK.xa_lib.TLMC_GetTrackSettleParams(handle, byref(params), c_int64(max_wait_in_milliseconds))
        if rc == 0:
            track_params_out[0] = params
        return rc

    @staticmethod
    def set_track_settle_params(handle, settle_time, settle_window, track_window):
        params = TLMC_TrackSettleParams()
        params.settleTime = c_uint16(settle_time)
        params.settleWindow = c_uint16(settle_window)
        params.trackWindow = c_uint16(track_window)
        return TLMC_SDK.xa_lib.TLMC_SetTrackSettleParams(handle, byref(params))

    @staticmethod
    def get_trigger_params_for_dc_brushless(handle, trigger_params_out, max_wait_in_milliseconds):
        params = TLMC_TriggerParamsForDcBrushless()
        rc = TLMC_SDK.xa_lib.TLMC_GetTriggerParamsForDcBrushless(handle, byref(params), c_int64(max_wait_in_milliseconds))
        if rc == 0:
            trigger_params_out[0] = params
        return rc

    @staticmethod
    def set_trigger_params_for_dc_brushless(handle, modes):
        params = TLMC_TriggerParamsForDcBrushless()
        params.modes = c_uint8(modes)
        return TLMC_SDK.xa_lib.TLMC_SetTriggerParamsForDcBrushless(handle, byref(params))

    @staticmethod
    def get_trigger_params_for_stepper(handle, trigger_params_out, max_wait_in_milliseconds):
        params = TLMC_TriggerParamsForStepper()
        rc = TLMC_SDK.xa_lib.TLMC_GetTriggerParamsForStepper(handle, byref(params), c_int64(max_wait_in_milliseconds))
        if rc == 0:
            trigger_params_out[0] = params
        return rc

    @staticmethod
    def set_trigger_params_for_stepper(handle, modes):
        params = TLMC_TriggerParamsForStepper()
        params.modes = c_uint8(modes)
        return TLMC_SDK.xa_lib.TLMC_SetTriggerParamsForStepper(handle, byref(params))

    @staticmethod
    def get_universal_status(handle, universal_status_out, max_wait_in_milliseconds):
        st = TLMC_UniversalStatus()
        rc = TLMC_SDK.xa_lib.TLMC_GetUniversalStatus(handle, byref(st), c_int64(max_wait_in_milliseconds))
        if rc == 0:
            universal_status_out[0] = st
        return rc

    @staticmethod
    def get_universal_status_bits(handle, status_bits_out, max_wait_in_milliseconds):
        bits = c_uint32(0)
        rc = TLMC_SDK.xa_lib.TLMC_GetUniversalStatusBits(handle, byref(bits), c_int64(max_wait_in_milliseconds))
        if rc == 0:
            status_bits_out[0] = bits.value
        return rc

    @staticmethod
    def get_velocity_params(handle, velocity_params_out, max_wait_in_milliseconds):
        params = TLMC_VelocityParams()
        rc = TLMC_SDK.xa_lib.TLMC_GetVelocityParams(handle, byref(params), c_int64(max_wait_in_milliseconds))
        if rc == 0:
            velocity_params_out[0] = params
        return rc

    @staticmethod
    def set_velocity_params(handle, min_velocity, acceleration, max_velocity):
        params = TLMC_VelocityParams()
        params.minVelocity = c_uint32(min_velocity)
        params.acceleration = c_uint32(acceleration)
        params.maxVelocity = c_uint32(max_velocity)
        return TLMC_SDK.xa_lib.TLMC_SetVelocityParams(handle, byref(params))

    # ----- Motion (home/move/stop/identify etc.) -----

    @staticmethod
    def home(handle, max_wait_in_milliseconds):
        return TLMC_SDK.xa_lib.TLMC_Home(handle, c_int64(max_wait_in_milliseconds))

    @staticmethod
    def identify(handle):
        return TLMC_SDK.xa_lib.TLMC_Identify(handle)

    @staticmethod
    def move(handle, mode, param, max_wait_in_milliseconds):
        return TLMC_SDK.xa_lib.TLMC_Move(handle, c_uint8(mode), c_int32(param), c_int64(max_wait_in_milliseconds))

    @staticmethod
    def move_absolute(handle, move_mode, position, max_wait_in_milliseconds):
        position_val = position
        if move_mode == TLMC_MoveModes.MoveMode_AbsoluteToProgrammedPosition:
            position_val = 0  # TLMC_Unused
        else:
            move_mode = TLMC_MoveModes.MoveMode_Absolute
        return TLMC_SDK.move(handle, move_mode, position_val, max_wait_in_milliseconds)

    @staticmethod
    def move_continuous(handle, direction, max_wait_in_milliseconds):
        if direction == TLMC_MoveDirection.Move_Direction_Reverse:
            move_mode = TLMC_MoveModes.MoveMode_ContinuousReverse
        else:
            move_mode = TLMC_MoveModes.MoveMode_ContinuousForward
        return TLMC_SDK.move(handle, move_mode, 0, max_wait_in_milliseconds)

    @staticmethod
    def move_jog(handle, direction, max_wait_in_milliseconds):
        if direction == TLMC_MoveDirection.Move_Direction_Reverse:
            move_mode = TLMC_MoveModes.MoveMode_JogReverse
        else:
            move_mode = TLMC_MoveModes.MoveMode_JogForward
        return TLMC_SDK.move(handle, move_mode, 0, max_wait_in_milliseconds)

    @staticmethod
    def move_relative(handle, move_mode, step_size, max_wait_in_milliseconds):
        if move_mode == TLMC_MoveModes.MoveMode_RelativeByProgrammedDistance:
            param = 0  # TLMC_Unused
        else:
            move_mode = TLMC_MoveModes.MoveMode_Relative  # set (not compare)
            param = step_size
        return TLMC_SDK.move(handle, move_mode, param, max_wait_in_milliseconds)

    @staticmethod
    def stop(handle, stop_mode, max_wait_in_milliseconds):
        return TLMC_SDK.xa_lib.TLMC_Stop(handle, c_uint8(stop_mode), c_int64(max_wait_in_milliseconds))

    # ----- Misc -----

    @staticmethod
    def restore_factory_defaults(handle):
        return TLMC_SDK.xa_lib.TLMC_RestoreFactoryDefaults(handle)

    @staticmethod
    def set_status_mode(handle, operating_mode):
        return TLMC_SDK.xa_lib.TLMC_SetStatusMode(handle, c_uint32(operating_mode))

    @staticmethod
    def set_end_of_move_messages_mode(handle, new_mode):
        return TLMC_SDK.xa_lib.TLMC_SetEndOfMoveMessagesMode(handle, c_uint8(new_mode))

    @staticmethod
    def get_rich_response(handle, rich_response_out):
        rr = TLMC_RichResponse()
        rc = TLMC_SDK.xa_lib.TLMC_GetRichResponse(handle, byref(rr))
        if rc == 0:
            rich_response_out[0] = rr
        return rc

    @staticmethod
    def persist_params(handle, parameter_group_id):
        return TLMC_SDK.xa_lib.TLMC_PersistParams(handle, c_uint16(parameter_group_id))