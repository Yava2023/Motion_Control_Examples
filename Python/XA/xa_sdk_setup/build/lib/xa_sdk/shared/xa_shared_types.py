import ctypes
import inspect

from ctypes import *
from abc import ABCMeta, abstractmethod
from xa_sdk.shared.tlmc_type_structures import *
from xa_sdk.native_sdks.xa_sdk import XASDK
# Base class for all products. Contains everything needed for calling the native SDK interface methods


class XADevice(metaclass=ABCMeta):
    def __init__(self):
        self.device_id = -1
        self.transport = "DEFAULT"
        self.sdk = None
        self.handle = ctypes.c_ulong(-1)
        self.native_api = XASDK()

    @property
    @abstractmethod
    def device_id(self):
        return self.device_id

    @device_id.setter
    @abstractmethod
    def device_id(self, val):
        self.device_id = val

    @property
    def native_api(self):
        return self.sdk

    @native_api.setter
    def native_api(self, val):
        self.sdk = val

    @property
    @abstractmethod
    def transport(self):
        return self.transport

    @transport.setter
    @abstractmethod
    def transport(self, val):
        self.transport = val

    @property
    def device_handle(self):
        return self.handle

    @device_handle.setter
    def device_handle(self, val):
        self.handle = val

    @abstractmethod
    def add_user_message_to_log(self, user_message):
        ret = self.native_api.add_user_message_to_log(user_message)
        return ret

    @abstractmethod
    def close(self):
        """
        Ends the current device session. Should be called before disconnect() and shutdown().
        """
        ret = self.native_api.close(self.handle)
        return ret

    @abstractmethod
    def disconnect(self):
        """
        Disconnects from the stated device. Should be called before close() and shutdown. 
        """
        ret = self.native_api.disconnect(self.handle)
        return ret

    @abstractmethod
    def get_device_info(self, max_wait_in_milliseconds: int):
        """
        Returns the device info. This includes the deviceFamily, deviceType, partNumber, device, transport type,
        and parentDevice. 
        """
        ret = self.native_api.get_device_info(
            self.handle, max_wait_in_milliseconds)
        return DeviceInfo(ret)

    @abstractmethod
    def get_hardware_info(self, max_wait_in_milliseconds: int):
        """
        Returns the hardware info for the device. This includes the serialNumber, partNumber, deviceType,
        firmwareVersion, notes, deviceDependentData, hardwareVersion, modificationState,
        and numberOfChannels.
        """
        ret = self.native_api.get_hardware_info(
            self.handle, max_wait_in_milliseconds)
        return HardwareInfo(ret)

    @abstractmethod
    def get_method_list(self, cls):
        """
        Returns a list of methods accessible to the device class. 
        """
        methods = inspect.getmembers(cls, predicate=inspect.isfunction)
        for name, method in methods:
            if name == '__init__' or name == 'device_id' or name == 'transport':
                pass
            else:
                print(name)
        

    @abstractmethod
    def get_setting(self, settings_name: str, max_wait_in_milliseconds: int):
        """
        Returns a single specified setting parameter.
        """
        ret = self.native_api.get_setting(
            self.handle, settings_name, max_wait_in_milliseconds)
        return ret

    @abstractmethod
    def get_setting_as_string(self, buffer: list, buffer_length: int, result_length: int,
                            TLMC_setting_string_format: TLMC_SettingStringFormat, include_read_only_items: bool):
        """
        Returns settings as a string. 
        """
        ret = self.native_api.get_setting_as_string(self.device_handle, buffer, buffer_length,
                                                    result_length, TLMC_setting_string_format, include_read_only_items)
        return ret

    @abstractmethod
    def get_setting_count(self):
        """
        Returns the amount of available settings objects. Used with get_settings(). 
        """
        ret = self.native_api.get_setting_count(self.handle)
        return ret

    @abstractmethod
    def get_setting_discrete_values(self, settings_name: str, buffer: list, buffer_length: int, result_length: int):
        """
        Returns only the settings specified.
        """
        ret = self.native_api.get_setting_discrete_values(
            self.handle, settings_name, buffer, buffer_length, result_length)
        return ret

    @abstractmethod
    def get_settings(self, source_start_index: int, number_of_items: int, number_of_items_copied: int):
        """
        Returns all of the available settings objects. Use get_setting_count() to get the number_of_items. 
        """
        ret = self.native_api.get_settings(
            self.handle, source_start_index, number_of_items, number_of_items_copied)
        return TLMCSetting(ret)

    @abstractmethod
    def identify(self):
        """
        Initiates an identify command. This causes the controller LEDs to flash to prove an established connection. 
        """
        ret = self.native_api.identify(self.handle)
        return ret

    @abstractmethod
    def set_end_of_message_mode(self, mode: TLMC_EndOfMessagesMode):
        """
        Changes the end of message mode
        """
        ret = self.native_api.set_end_of_message_mode(self.handle, mode)
        return ret

    @abstractmethod
    def set_setting(self, settings_name: str):
        """
        Changes the specified setting parameter. 
        """
        ret = self.native_api.set_setting(self.handle, settings_name)
        return ret

    @abstractmethod
    def set_settings_from_string(self, settings_name: str):
        """
        Changes settings based on input string.
        """
        ret = self.native_api.set_settings_from_string(
            self.device_handle, settings_name)
        return ret

    
    
class AnalogMonitorConfigurationParams():

    def __init__(self, tlmc_monitor_configuration_params):
        self._motor_channel = 0
        self._system_variable = 0
        self._scale = 0
        self._offset = 0

        if type(tlmc_monitor_configuration_params) == TLMC_AnalogMonitorConfigurationParams:
            self._motor_channel = TLMC_AnalogMonitorMotorChannel(
                c_uint16(tlmc_monitor_configuration_params.motorChannel).value)
            self._system_variable = TLMC_AnalogMonitorSystemVariable(
                c_uint16(tlmc_monitor_configuration_params.systemVariable).value)
            self._scale = c_int32(
                tlmc_monitor_configuration_params.scale).value
            self._offset = c_int32(
                tlmc_monitor_configuration_params.offset).value

    @property
    def motor_channel(self):
        return self._motor_channel

    @motor_channel.setter
    def motor_channel(self, val):
        self._motor_channel = val

    @property
    def system_variable(self, val):
        return self._system_variable

    @system_variable.setter
    def system_variable(self, val):
        self._system_variable = val

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, val):
        self._scale = val

    @property
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, val):
        self._offset = val


class ConnectedProductInfo():

    def __init__(self, tlmc_connected_product_info):
        self._product_name = 0
        self._part_number = 0
        self._axis_type = 0
        self._movement_type = 0
        self._unit_type = 0
        self._distance_scale_factor = 0
        self._velocity_scale_factor = 0
        self._acceleration_scale_factor = 0
        self._min_position = 0
        self._max_position = 0
        self._max_velocity = 0
        self._max_acceleration = 0

        if type(tlmc_connected_product_info) == TLMC_ConnectedProductInfo():
            self._product_name = c_char_p(
                tlmc_connected_product_info.productName)
            self._part_number = c_char_p(
                tlmc_connected_product_info.partNumber)
            self._axis_type = TLMC_ConnectedProductAxisType(
                c_uint16(tlmc_connected_product_info.axisType).value)
            self._movement_type = TLMC_ConnectedProductMovementType(
                c_uint16(tlmc_connected_product_info.movementType).value)
            self._unit_type = TLMC_Unit(
                c_uint16(tlmc_connected_product_info.unitType).value)
            self._distance_scale_factor = c_double(
                tlmc_connected_product_info.distanceScaleFactor).value
            self._velocity_scale_factor = c_double(
                tlmc_connected_product_info.velocityScaleFactor).value
            self._acceleration_scale_factor = c_double(
                tlmc_connected_product_info.accelerationScaleFactor).value
            self._min_position = c_double(
                tlmc_connected_product_info.minPosition).value
            self._max_position = c_double(
                tlmc_connected_product_info.maxPosition).value
            self._max_velocity = c_double(
                tlmc_connected_product_info.maxVelocity).value
            self._max_acceleration = c_double(
                tlmc_connected_product_info.maxAcceleration).value

    @property
    def product_name(self):
        return self._product_name

    @product_name.setter
    def product_name(self, val):
        self._product_name = val

    @property
    def part_number(self):
        return self._part_number
    
    @part_number.setter
    def part_number(self, val):
        self._part_number = val

    @property
    def axis_type(self):
        return self._axis_type

    @axis_type.setter
    def axis_type(self, val):
        self._axis_type = val

    @property
    def movement_type(self):
        return self._movement_type

    @movement_type.setter
    def movement_type(self, val):
        self._movement_type = val

    @property
    def unit_type(self):
        return self._unit_type

    @unit_type.setter
    def unit_type(self, val):
        self._unit_type = val

    @property
    def distance_scale_factor(self):
        return self._distance_scale_factor

    @distance_scale_factor.setter
    def distance_scale_factor(self, val):
        self._distance_scale_factor = val

    @property
    def velocity_scale_factor(self):
        return self._velocity_scale_factor

    @velocity_scale_factor.setter
    def velocity_scale_factor(self, val):
        self._velocity_scale_factor = val

    @property
    def acceleration_scale_factor(self):
        return self._acceleration_scale_factor

    @acceleration_scale_factor.setter
    def acceleration_scale_factor(self, val):
        self._acceleration_scale_factor = val

    @property
    def min_position(self):
        return self._min_position

    @min_position.setter
    def min_position(self, val):
        self._min_position = val

    @property
    def max_position(self):
        return self._max_position

    @max_position.setter
    def max_position(self, val):
        self._max_position = val

    @property
    def max_velocity(self):
        return self._max_velocity

    @max_velocity.setter
    def max_velocity(self, val):
        self._max_velocity = val

    @property
    def max_acceleration(self):
        return self._max_acceleration

    @max_acceleration.setter
    def max_acceleration(self, val):
        self._max_acceleration = val


class DCBrushlessTriggerParams():

    def __init__(self, tlmc_trigger_params_for_dc_brushless):
        self._modes = 0

        if type(tlmc_trigger_params_for_dc_brushless) == TLMC_TriggerParamsForDcBrushless:
            self._modes = TLMC_TriggerModesForDcBrushless(
                c_uint8(tlmc_trigger_params_for_dc_brushless.modes).value)

    @property
    def modes(self):
        return self._modes

    @modes.setter
    def modes(self, val):
        self._modes = val


class DeviceInfo():

    def __init__(self, tlmc_device_info):
        self._device_family = 0
        self._device_type = 0
        self._part_number = 0
        self._device = 0
        self._transport = 0
        self._parent_device = 0
        self._device_type_descriptions = 0

        if type(tlmc_device_info) == TLMC_DeviceInfo:
            self._device_family = TLMC_DeviceFamily(
                c_uint8(tlmc_device_info.deviceFamily).value)
            self._device_type = (
                c_uint32(tlmc_device_info.deviceType).value)
            self._part_number = c_char_p(tlmc_device_info.partNumber)
            self._device = c_char_p(tlmc_device_info.device)
            self._transport = c_char_p(tlmc_device_info.transport)
            self._parent_device = c_char_p(tlmc_device_info.parentDevice)
            self._device_type_descriptions = c_char_p(tlmc_device_info.deviceTypeDescription)

    @property
    def device_family(self):
        return self._device_family

    @device_family.setter
    def device_family(self, val):
        self._device_family = val

    @property
    def device_type(self):
        return self._device_type

    @device_type.setter
    def device_type(self, val):
        self._device_type = val

    @property
    def part_number(self):
        return self._part_number

    @part_number.setter
    def part_number(self, val):
        self._part_number = val

    @property
    def device(self):
        return self._device

    @device.setter
    def device(self, val):
        self._device = val

    @property
    def transport(self):
        return self._transport

    @transport.setter
    def transport(self, val):
        self._transport = val

    @property
    def parent_device(self):
        return self._parent_device

    @parent_device.setter
    def parent_device(self, val):
        self._parent_device = val

    @property
    def device_type_description(self):
        return self._device_type_description
    
    @device_type_description.setter
    def device_type_description(self, val):
        self._device_type_descriptions = val

class DCPidParams():
    def __init__(self, tlmc_dc_pid_params):
        self._proportional = 0
        self._integral = 0
        self._derivative = 0
        self._integralLimit = 0
        self._filterControl = 0

        if type(tlmc_dc_pid_params) == TLMC_DcPidParams:
            self._proportional = c_uint32(
                tlmc_dc_pid_params.proportional).value
            self._integral = c_uint32(
                tlmc_dc_pid_params.integral).value
            self._derivative = c_uint32(
                tlmc_dc_pid_params.derivative).value
            self._integralLimit = c_uint32(
                tlmc_dc_pid_params.integralLimit).value
            self._filterControl = c_uint16(
                tlmc_dc_pid_params.filterControl).value
            
    @property
    def proportional(self):
        return self._proportional
    
    @proportional.setter
    def proportional(self,value):
        self._proportional = value

    @property
    def integral(self):
        return self._integral
    
    @integral.setter
    def integral(self, value):
        self._integral = value

    @property
    def derivative(self):
        return self._derivative

    @derivative.setter
    def derivative(self, value):
        self._derivative = value

    @property
    def integral_limit(self):
        return self._integralLimit

    @integral_limit.setter
    def integral_limit(self, value):
        self._integralLimit = value

    @property
    def filter_control(self):
        return self._filterControl
      
    @filter_control.setter
    def filter_control(self, value):
        self._filterControl = value
        
            
class GeneralMoveParams():

    def __init__(self, tlmc_general_move_params):
        self._backlash_distance = 0
        if type(tlmc_general_move_params) == TLMC_GeneralMoveParams:
            self._backlash_distance = c_int16(
                tlmc_general_move_params.backlashDistance).value

    @property
    def backlash_distance(self):
        return self._backlash_distance

    @backlash_distance.setter
    def backlash_distance(self, val):
        self._backlash_distance = val


class HardwareInfo():

    def __init__(self, tlmc_hardware_info):
        self._serial_number = 0
        self._part_number = 0
        self._type = 0
        self._firmware_version = c_ubyte(0)
        self._notes = 0
        self._device_dependent_data = 0
        self._hardware_version = 0
        self._modification_state = 0
        self._number_of_channels = 0

        if type(tlmc_hardware_info) == TLMC_HardwareInfo:
            self._serial_number = c_uint32(
                tlmc_hardware_info.serialNumber).value
            self._part_number = c_char_p(
                tlmc_hardware_info.partNumber).value  
            self._type = c_uint16(tlmc_hardware_info.type).value
            self._firmware_version = TLMC_FirmwareVersion(
                c_uint8(tlmc_hardware_info.firmwareVersion).value)
            self._notes = c_char_p(tlmc_hardware_info.notes).value
            self._device_dependent_data = c_char_p(
                tlmc_hardware_info.deviceDependantData).value
            self._hardware_version = c_uint16(
                tlmc_hardware_info.hardwareVersion).value
            self._modification_state = c_uint16(
                tlmc_hardware_info.modificationState).value
            self._number_of_channels = c_uint16(
                tlmc_hardware_info.numChannels).value

    @property
    def serial_number(self):
        return self._serial_number

    @serial_number.setter
    def serial_number(self, val):
        self._serial_number = val

    @property
    def part_number(self):
        return self._part_number

    @part_number.setter
    def part_number(self, val):
        self._part_number = val

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, val):
        self._type = val

    @property
    def firmware_version(self):
        return self._firmware_version

    @firmware_version.setter
    def firmware_version(self, val):
        self._firmware_version = val

    @property
    def notes(self):
        return self._notes

    @notes.setter
    def notes(self, val):
        self._notes = val

    @property
    def device_dependent_data(self):
        return self._device_dependent_data

    @device_dependent_data.setter
    def device_dependent_data(self, val):
        self._device_dependent_data = val

    @property
    def hardware_version(self):
        return self._hardware_version

    @hardware_version.setter
    def hardware_version(self, val):
        self._hardware_version = val

    @property
    def modification_state(self):
        return self._modification_state

    @modification_state.setter
    def modification_state(self, val):
        self._modification_state = val

    @property
    def number_of_channels(self):
        return self._number_of_channels

    @number_of_channels.setter
    def number_of_channels(self, val):
        self._number_of_channels = val


class HomeParams():

    def __init__(self, tlmc_home_params):
        self._offset = 0
        self._velocity = 0
        self._direction = 0
        self._limitSwitch = 0
        if type(tlmc_home_params) == TLMC_HomeParams:
            self._offset = c_int32(tlmc_home_params.offsetDistance).value
            self._velocity = c_uint32(tlmc_home_params.velocity).value
            self._direction = c_uint16(tlmc_home_params.direction).value
            self._limitSwitch = c_uint16(tlmc_home_params.limitSwitch).value

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, val):
        self._direction = val

    @property
    def limitSwitch(self):
        return self._limitSwitch

    @direction.setter
    def limitSwitch(self, val):
        self._limitSwitch = val

    @property
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, val):
        self._offset = val

    @property
    def velocity(self):
        return self._velocity

    @offset.setter
    def velocity(self, val):
        self._velocity = val


class IoConfigurationParams():

    def __init__(self, tlmc_io_configuration_params):
        self._mode = 0
        self._trigger_out_source = 0

        if type(tlmc_io_configuration_params) == TLMC_IoConfigurationParams:
            self._mode = TLMC_IoPortMode(
                c_uint16(tlmc_io_configuration_params.mode).value)
            self._trigger_out_source = TLMC_IoPortSource(
                c_uint16(tlmc_io_configuration_params.triggerOutSource).value)

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, val):
        self._mode = val

    @property
    def trigger_out_source(self):
        return self._trigger_out_source

    @trigger_out_source.setter
    def trigger_out_source(self, val):
        self.trigger_out_source = val


class IoTriggerParams():

    def __init__(self, tlmc_io_trigger_params):
        self._trigger_in_mode = 0
        self._trigger_in_polarity = 0
        self._trigger_in_source = 0
        self._trigger_out_mode = 0
        self._trigger_out_polarity = 0
        self._trigger_out_forward_start_position = 0
        self._trigger_out_forward_interval = 0
        self._trigger_out_forward_number_of_pulses = 0
        self._trigger_out_reverse_start_position = 0
        self._trigger_out_reverse_interval = 0
        self._trigger_out_reverse_number_of_pulses = 0
        self._trigger_out_pulse_width = 0
        self._trigger_out_number_of_cycles = 0

        if type(tlmc_io_trigger_params) == TLMC_IoTriggerParams:
            self._trigger_in_mode = TLMC_IoTriggerInMode(
                c_uint16(tlmc_io_trigger_params.triggerInMode)).value
            self._trigger_in_polarity = TLMC_IoTriggerPolarity(
                c_uint16(tlmc_io_trigger_params.triggerInPolarity)).value
            self._trigger_in_source = TLMC_IoTriggerInSource(
                c_uint16(tlmc_io_trigger_params.triggerInSource)).value
            self._trigger_out_mode = TLMC_IoTriggerOutMode(
                c_uint16(tlmc_io_trigger_params.triggerOutMode)).value
            self._trigger_out_polarity = TLMC_IoTriggerPolarity(
                c_uint16(tlmc_io_trigger_params.triggerOutPolarity)).value
            self._trigger_out_forward_start_position = c_int32(
                tlmc_io_trigger_params.triggerOutForwardStartPosition).value
            self._trigger_out_forward_interval = c_int32(
                tlmc_io_trigger_params.triggerOutForwardInterval).value
            self._trigger_out_forward_number_of_pulses = c_int32(
                tlmc_io_trigger_params.triggerOutForwardnumberOfPulses).value
            self._trigger_out_reverse_start_position = c_int32(
                tlmc_io_trigger_params.triggerOutReverseStartPosition).value
            self._trigger_out_reverse_interval = c_int32(
                tlmc_io_trigger_params.triggerOutReverseInterval).value
            self._trigger_out_reverse_number_of_pulses = c_int32(
                tlmc_io_trigger_params.triggerOutReverseNumberOfPulses).value
            self._trigger_out_pulse_width = c_uint32(
                tlmc_io_trigger_params.triggerOutPulseWidth).value
            self._trigger_out_number_of_cycles = c_uint32(
                tlmc_io_trigger_params.triggerOutNumberOfCycles).value
            

    @property
    def trigger_in_mode(self):
        return self._trigger_in_mode

    @trigger_in_mode.setter
    def trigger_in_mode(self, val):
        self._trigger_in_mode = val

    @property
    def trigger_in_polarity(self):
        return self._trigger_in_polarity

    @trigger_in_polarity.setter
    def trigger_in_polarity(self, val):
        self._trigger_in_polarity = val

    @property
    def trigger_in_source(self):
        return self._trigger_in_source

    @trigger_in_source.setter
    def trigger_in_source(self, val):
        self._trigger_in_source = val

    @property
    def trigger_out_mode(self):
        return self._trigger_out_mode

    @trigger_out_mode.setter
    def trigger_out_mode(self, val):
        self._trigger_out_mode = val

    @property
    def trigger_out_polarity(self):
        return self._trigger_out_polarity

    @trigger_out_polarity.setter
    def trigger_out_polarity(self, val):
        self._trigger_out_polarity

    @property
    def trigger_out_forward_start_position(self):
        return self._trigger_out_forward_start_position

    @trigger_out_forward_start_position.setter
    def trigger_out_forward_start_position(self, val):
        self._trigger_out_forward_start_position = val

    @property
    def trigger_out_forward_interval(self):
        return self._trigger_out_forward_interval

    @trigger_out_forward_interval.setter
    def trigger_out_forward_interval(self, val):
        self._trigger_out_forward_interval = val

    @property
    def trigger_out_forward_number_of_pulses(self):
        return self._trigger_out_forward_number_of_pulses

    @trigger_out_forward_number_of_pulses.setter
    def trigger_out_forward_number_of_pulses(self, val):
        self._trigger_out_forward_number_of_pulses = val

    @property
    def trigger_out_reverse_start_position(self):
        return self._trigger_out_reverse_start_position

    @trigger_out_reverse_start_position.setter
    def trigger_out_reverse_start_position(self, val):
        self._trigger_out_reverse_start_position

    @property
    def trigger_out_reverse_interval(self):
        return self._trigger_out_reverse_interval

    @trigger_out_reverse_interval.setter
    def trigger_out_reverse_interval(self, val):
        self._trigger_out_reverse_interval = val

    @property
    def trigger_out_reverse_number_of_pulses(self):
        return self._trigger_out_reverse_number_of_pulses

    @trigger_out_reverse_number_of_pulses.setter
    def trigger_out_reverse_number_of_pulses(self, val):
        self._trigger_out_reverse_number_of_pulses = val

    @property
    def trigger_out_pulse_width(self):
        return self._trigger_out_pulse_width

    @trigger_out_pulse_width.setter
    def trigger_out_pulse_width(self, val):
        self._trigger_out_pulse_width = val

    @property
    def trigger_out_number_of_cycles(self):
        return self._trigger_out_number_of_cycles

    @trigger_out_number_of_cycles.setter
    def trigger_out_number_of_cycles(self, val):
        self._trigger_out_number_of_cycles = val



class JogParams():

    def __init__(self, tlmc_move_jog_params):
        self._mode = 0
        self._step_size = 0
        self._min_velocity = 0
        self._acceleration = 0
        self._max_velocity = 0
        self._stop_mode = 0
        if type(tlmc_move_jog_params) == TLMC_JogParams:
            self._mode = (c_uint16(tlmc_move_jog_params.mode)).value
            self._step_size = c_int32(tlmc_move_jog_params.stepSize).value
            self._min_velocity = c_uint32(
                tlmc_move_jog_params.minVelocity).value
            self._acceleration = c_uint32(
                tlmc_move_jog_params.acceleration).value
            self._max_velocity = c_uint32(
                tlmc_move_jog_params.maxVelocity).value
            self._stop_mode = (
                c_uint16(tlmc_move_jog_params.stopMode)).value

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, val):
        self._mode = val

    @property
    def step_size(self):
        return self._step_size

    @step_size.setter
    def step_size(self, val):
        self._step_size = val

    @property
    def min_velocity(self):
        return self._min_velocity

    @min_velocity.setter
    def min_velocity(self, val):
        self._min_velocity = val

    @property
    def acceleration(self):
        return self._acceleration

    @acceleration.setter
    def acceleration(self, val):
        self._acceleration = val

    @property
    def max_velocity(self):
        return self._max_velocity

    @max_velocity.setter
    def max_velocity(self, val):
        self._max_velocity = val

    @property
    def stop_mode(self):
        return self._stop_mode

    @stop_mode.setter
    def stop_mode(self, val):
        self._stop_mode = val


class JoystickParams():
    def __init__(self, tlmc_joystick_params):
        self._low_gear_max_velocity = 0
        self._high_gear_max_velocity = 0
        self._low_gear_acceleration = 0
        self._high_gear_acceleration = 0
        self._direction_sense = 0

        if type(tlmc_joystick_params) == TLMC_JoystickParams:
            self._low_gear_max_velocity = c_uint32(
                tlmc_joystick_params.lowGearMaxVelocity).value
            self._high_gear_max_velocity = c_uint32(
                tlmc_joystick_params.highGearMaxVelocity).value
            self._low_gear_acceleration = c_uint32(
                tlmc_joystick_params.lowGearAcceleration).value
            self._high_gear_acceleration = c_uint32(
                tlmc_joystick_params.highGearAcceleration).value
            self._direction_sense = TLMC_JoystickDirectionSense(
                c_uint16(tlmc_joystick_params.directionSense).value)

    @property
    def low_gear_max_veloctiy(self):
        return self._low_gear_max_velocity

    @low_gear_max_veloctiy.setter
    def low_gear_max_velocity(self, val):
        self._low_gear_max_velocity = val

    @property
    def high_gear_max_velocity(self):
        return self._high_gear_max_velocity

    @high_gear_max_velocity.setter
    def high_gear_max_velocity(self, val):
        self._high_gear_max_velocity = val

    @property
    def low_gear_acceleration(self):
        return self._low_gear_acceleration

    @low_gear_acceleration.setter
    def low_gear_acceleration(self, val):
        self._low_gear_acceleration = val

    @property
    def high_gear_acceleration(self):
        return self._high_gear_acceleration

    @high_gear_acceleration.setter
    def high_gear_acceleration(self, val):
        self._high_gear_acceleration = val

    @property
    def direction_sense(self):
        return self._direction_sense

    @direction_sense.setter
    def direction_sense(self, val):
        self._direction_sense = val


class KcubeIoTriggerParams():

    def __init__(self, tlmc_kcube_io_trigger_params):
        self._trigger_1_mode = 0
        self._trigger_1_polarity = 0
        self._trigger_2_mode = 0
        self._trigger_2_polarity = 0

        if type(tlmc_kcube_io_trigger_params) == TLMC_KcubeIoTriggerParams:
            self._trigger_1_mode = TLMC_KcubeIoTriggerMode(
                (tlmc_kcube_io_trigger_params.trigger1Mode)).value
            self._trigger_1_polarity = TLMC_KcubeIoTriggerPolarity(
                (tlmc_kcube_io_trigger_params.trigger1Polarity)).value
            self._trigger_2_mode = TLMC_KcubeIoTriggerMode(
                (tlmc_kcube_io_trigger_params.trigger2Mode)).value
            self._trigger_2_polarity = TLMC_KcubeIoTriggerPolarity(
                (tlmc_kcube_io_trigger_params.trigger2Polarity)).value

    @property
    def trigger_1_mode(self):
        return self._trigger_1_mode

    @trigger_1_mode.setter
    def trigger_1_mode(self, val):
        self._trigger_1_mode = val

    @property
    def trigger_1_polarity(self):
        return self._trigger_1_polarity

    @trigger_1_polarity.setter
    def trigger_1_polarity(self, val):
        self._trigger_1_polarity = val

    @property
    def trigger_2_mode(self):
        return self._trigger_2_mode

    @trigger_2_mode.setter
    def trigget_2_mode(self, val):
        self._trigger_2_mode = val

    @property
    def trigger_2_polarity(self):
        return self._trigger_2_polarity

    @trigger_2_polarity.setter
    def trigger_2_mode(self, val):
        self._trigger_2_polarity = val


class KcubeMmiParams():

    def __init__(self, tlmc_kcube_mmi_params):
        self._joystick_mode = 0
        self._joystick_max_velocity = 0
        self._joystick_acceleration = 0
        self._joystick_direction_sense = 0
        self._preset_position_1 = 0
        self._preset_position_2 = 0
        self._display_brightness = 0
        self._display_timeout = 0
        self._display_dim_level = 0
        self._preset_position_3 = 0
        self._joystick_sensativity = 0

        if type(tlmc_kcube_mmi_params) == TLMC_KcubeMmiParams:
            self._joystick_mode = TLMC_KcubeMmi_JoystickMode(
                tlmc_kcube_mmi_params.joystickMode).value
            self._joystick_max_velocity = c_uint32(
                tlmc_kcube_mmi_params.joystickMaxVelocity).value
            self._joystick_acceleration = c_uint32(
                tlmc_kcube_mmi_params.joystickAcceleration).value
            self._joystick_direction_sense = TLMC_KcubeMmi_JoystickDirectionSense(
                (tlmc_kcube_mmi_params.joystickDirectionSense)).value
            self._preset_position_1 = c_int32(
                tlmc_kcube_mmi_params.presetPosition1).value
            self._preset_position_2 = c_int32(
                tlmc_kcube_mmi_params.presetPosition2).value
            self._display_brightness = c_uint16(
                tlmc_kcube_mmi_params.displayBrightness).value
            self._display_timeout = c_uint16(
                tlmc_kcube_mmi_params.displayTimeout).value
            self._display_dim_level = c_uint16(
                tlmc_kcube_mmi_params.displayDimLevel).value
            self._preset_position_3 = c_int32(
                tlmc_kcube_mmi_params.presetPosition3).value
            self._joystick_sensativity = c_uint16(
                tlmc_kcube_mmi_params.joystickSensativity).value

    @property
    def joystick_mode(self):
        return self._joystick_mode

    @joystick_mode.setter
    def joystick_mode(self, val):
        self._joystick_mode = val

    @property
    def joystick_max_velcoity(self):
        return self._joystick_max_velocity

    @joystick_max_velcoity.setter
    def joystick_max_velocity(self, val):
        self._joystick_max_velocity = val

    @property
    def joystick_acceleration(self):
        return self._joystick_acceleration

    @joystick_acceleration.setter
    def joystick_acceleration(self, val):
        self._joystick_acceleration = val

    @property
    def joystick_direction_sense(self):
        return self._joystick_direction_sense

    @joystick_direction_sense.setter
    def joystick_direction_sense(self, val):
        self._joystick_direction_sense = val

    @property
    def preset_position_1(self):
        return self._preset_position_1

    @preset_position_1.setter
    def preset_position_1(self, val):
        self._preset_position_1 = val

    @property
    def preset_position_2(self):
        return self._preset_position_2

    @preset_position_2.setter
    def preset_position_2(self, val):
        self._preset_position_2 = val

    @property
    def display_brightness(self):
        return self._display_brightness

    @display_brightness.setter
    def display_brightness(self, val):
        self._display_brightness = val

    @property
    def display_timeout(self):
        return self._display_timeout

    @display_timeout.setter
    def display_timeout(self, val):
        self._display_timeout = val

    @property
    def display_dim_level(self):
        return self._display_dim_level

    @display_dim_level.setter
    def display_dim_level(self, val):
        self._display_dim_level = val

    @property
    def preset_position_3(self):
        return self._preset_position_3

    @preset_position_3.setter
    def preset_psotion_3(self, val):
        self._preset_position_3 = val

    @property
    def joystick_sensativity(self):
        return self._joystick_sensativity

    @joystick_sensativity.setter
    def joystick_sensativity(self, val):
        self._joystick_sensativity = val


class KcubePositionTriggerParams():

    def __init__(self, tlmc_kcube_position_trigger_params):
        self._forward_start_position = 0
        self._forward_interval = 0
        self._forward_number_of_pulses = 0
        self._reverse_start_position = 0
        self._reverse_interval = 0
        self._reverse_number_of_pulses = 0
        self._pulse_width = 0
        self._number_of_cycles = 0

        if type(tlmc_kcube_position_trigger_params) == TLMC_KcubePositionTriggerParams:
            self._forward_start_position = c_int32(
                tlmc_kcube_position_trigger_params.forwardStartPosition).value
            self._forward_interval = c_uint32(
                tlmc_kcube_position_trigger_params.forwardInterval).value
            self._forward_number_of_pulses = c_uint32(
                tlmc_kcube_position_trigger_params.forwardNumberOfPulses).value
            self._reverse_start_position = c_int32(
                tlmc_kcube_position_trigger_params.reverseStartPosition).value
            self._reverse_interval = c_uint32(
                tlmc_kcube_position_trigger_params.reverseInterval).value
            self._reverse_number_of_pulses = c_uint32(
                tlmc_kcube_position_trigger_params.reverseNumberOfPulses).value
            self._pulse_width = c_uint32(
                tlmc_kcube_position_trigger_params.pulseWidth).value
            self._number_of_cycles = c_uint32(
                tlmc_kcube_position_trigger_params.numberOfCycles).value

    @property
    def forward_start_position(self):
        return self._forward_start_position

    @forward_start_position.setter
    def forward_start_position(self, val):
        self._forward_start_position = val

    @property
    def forward_interval(self):
        return self._forward_interval

    @forward_interval.setter
    def forward_interval(self, val):
        self._forward_interval = val

    @property
    def forward_number_of_pulses(self):
        return self._forward_number_of_pulses

    @forward_number_of_pulses.setter
    def forward_number_of_pulses(self, val):
        self._forward_number_of_pulses = val

    @property
    def reverse_start_position(self):
        return self._reverse_start_position

    @reverse_start_position.setter
    def reverse_start_position(self, val):
        self._reverse_start_position = val

    @property
    def reverse_interval(self):
        return self._reverse_interval

    @reverse_interval.setter
    def reverse_interval(self, val):
        self._reverse_interval = val

    @property
    def reverse_number_of_pulses(self):
        return self._reverse_number_of_pulses

    @reverse_number_of_pulses.setter
    def reverse_number_of_pulses(self, val):
        self._reverse_number_of_pulses = val

    @property
    def pulse_width(self):
        return self._pulse_width

    @pulse_width.setter
    def pulse_width(self, val):
        self._pulse_width = val

    @property
    def number_of_cycles(self):
        return self._number_of_cycles

    @number_of_cycles.setter
    def number_of_cycles(self, val):
        self._number_of_cycles = val


class LcdDisplayParams():

    def __init__(self, tlmc_lcd_display_params):
        self._knob_sensativity = 0
        self._display_brightness = 0
        self._display_timeout = 0
        self._display_dim_level = 0

        if type(tlmc_lcd_display_params) == TLMC_LcdDisplayParams:
            self._knob_snesativity = c_int16(
                tlmc_lcd_display_params.knobSensativity).value
            self._display_brightness = c_uint16(
                tlmc_lcd_display_params.displayBrightness).value
            self._display_timeout = c_uint16(
                tlmc_lcd_display_params.displayTimeout).value
            self._display_dim_level = c_uint16(
                tlmc_lcd_display_params.displayDimLevel).value

    @property
    def knob_sensativity(self):
        return self._knob_sensativity

    @knob_sensativity.setter
    def knob_sensativity(self, val):
        self._knob_sensativity = val

    @property
    def display_brightness(self):
        return self._display_brightness

    @display_brightness.setter
    def display_brightness(self, val):
        self._display_brightness = val

    @property
    def display_timeout(self):
        return self._display_timeout

    @display_timeout.setter
    def display_timeout(self, val):
        self._display_timeout = val

    @property
    def display_dim_level(self):
        return self._display_dim_level

    @display_dim_level.setter
    def display_dim_level(self, val):
        self._display_dim_level = val


class LcdMoveParams():

    def __init__(self, tlmc_lcd_move_params):
        self._knob_mode = 0
        self._jog_step_size = 0
        self._acceleration = 0
        self._max_velocity = 0
        self._jog_stop_mode = 0
        self._preset_position = 0

        if type(tlmc_lcd_move_params) == TLMC_LcdMoveParams:
            self._knob_mode = TLMC_LcdKnobMode(
                c_uint16(tlmc_lcd_move_params.knobMode)).value
            self._jog_step_size = c_int32(
                tlmc_lcd_move_params.jogStepSize).value
            self._acceleration = c_int32(
                tlmc_lcd_move_params.acceleration).value
            self._max_velocity = c_int32(
                tlmc_lcd_move_params.maxVelocity).value
            self._jog_stop_mode = TLMC_JogStopModes(
                c_uint16(tlmc_lcd_move_params.jogStopMode)).value
            self._preset_position = c_int32(
                tlmc_lcd_move_params.presetPosition).value

    @property
    def knob_mode(self):
        return self._knob_mode

    @knob_mode.setter
    def knob_mode(self, val):
        self._knob_mode = val

    @property
    def jog_step_size(self):
        return self._jog_step_size

    @jog_step_size.setter
    def jog_step_size(self, val):
        self._jog_step_size = val

    @property
    def acceleration(self):
        return self._acceleration

    @acceleration.setter
    def acceleration(self, val):
        self._acceleration = val

    @property
    def max_velocity(self):
        return self._max_velocity

    @max_velocity.setter
    def max_velcoity(self, val):
        self._max_velocity = val

    @property
    def jog_stop_mode(self):
        return self._jog_stop_mode

    @jog_stop_mode.setter
    def jog_stop_mode(self, val):
        self._jog_stop_mode = val

    @property
    def preset_position(self):
        return self._preset_position

    @preset_position.setter
    def preset_position(self, val):
        self._preset_position = val


class LimitSwitchParams():

    def __init__(self, tlmc_limit_switch_params):
        self._clockwise_limit_mode = 0
        self._counterclockwise_limit_mode = 0
        self._clockwise_soft_limit = 0
        self._counterclockwise_soft_limit = 0
        self._soft_limit_operating_mode = 0

        if type(tlmc_limit_switch_params) == TLMC_LimitSwitchParams:
            self._clockwise_limit_mode = TLMC_HardLimitOperatingModes(
                c_uint16(tlmc_limit_switch_params.clockwiseHardLimitOperatingMode)).value
            self._counterclockwise_limit_mode = TLMC_HardLimitOperatingModes(c_uint16(
                tlmc_limit_switch_params.counterclockwiseHardLimitOperatingMode)).value
            self._clockwise_soft_limit = c_int32(
                tlmc_limit_switch_params.clockwiseSoftLimit).value
            self._counterclockwise_soft_limit = c_int32(
                tlmc_limit_switch_params.counterclockwiseSoftLimit).value
            self._soft_limit_operating_mode = TLMC_SoftLimitOperatingModes(
                c_uint16(tlmc_limit_switch_params.softLimitOperatingMode)).value

    @property
    def clockwise_limit_mode(self):
        return self._clockwise_limit_mode

    @clockwise_limit_mode.setter
    def clockwise_limit_mode(self, val):
        self._clockwise_limit_mode = val

    @property
    def counterclockwise_limit_mode(self):
        return self._counterclockwise_limit_mode

    @counterclockwise_limit_mode.setter
    def counterclockwise_limit_mode(self, val):
        self._counterclockwise_limit_mode = val

    @property
    def clockwise_soft_limit(self):
        return self._clockwise_soft_limit

    @clockwise_soft_limit.setter
    def clockwise_soft_limit(self, val):
        self._clockwise_soft_limit = val

    @property
    def counterclockwise_soft_limit(self):
        return self._counterclockwise_soft_limit

    @counterclockwise_soft_limit.setter
    def counterclockwise_soft_limit(self, val):
        self._counterclockwise_soft_limit = val

    @property
    def soft_limit_operating_mode(self):
        return self._soft_limit_operating_mode

    @soft_limit_operating_mode.setter
    def soft_limit_operating_mode(self, val):
        self._soft_limit_operating_mode = val


class MotorOutputParams():

    def __init__(self, tlmc_motor_output_params):
        self._continuous_current_limit = 0
        self._energy_limit = 0
        self._motor_limit = 0
        self._motor_bias = 0

        if type(tlmc_motor_output_params) == TLMC_MotorOutputParams:
            self._continuous_current_limit = c_uint16(
                tlmc_motor_output_params.continuousCurrentLimit).value
            self._energy_limit = c_uint16(
                tlmc_motor_output_params.energyLimit).value
            self._motor_limit = c_uint16(
                tlmc_motor_output_params.motorLimit).value
            self._motor_bias = c_uint16(
                tlmc_motor_output_params.motor_bias).value

    @property
    def continuous_current_limit(self):
        return self._continuous_current_limit

    @continuous_current_limit.setter
    def continuous_current_limit(self, val):
        self._continuous_current_limit = val

    @property
    def energy_limit(self):
        return self._energy_limit

    @energy_limit.setter
    def energy_limit(self, val):
        self._energy_limit = val

    @property
    def motor_limit(self):
        return self._motor_limit

    @motor_limit.setter
    def motor_limit(self, val):
        self._motor_limit = val

    @property
    def motor_bias(self):
        return self.motor_bias

    @motor_bias.setter
    def motor_bias(self, val):
        self._motor_bias = val


class MoveAbsoluteParams():

    def __init__(self, tlmc_move_absolute_params):
        self._absolute_position = 0
        if type(tlmc_move_absolute_params) == TLMC_MoveAbsoluteParams:
            self._absolute_position = c_int32(
                tlmc_move_absolute_params.absolutePosition).value

    @property
    def absolute_position(self):
        return self._absolute_position

    @absolute_position.setter
    def absolute_position(self, val):
        self._absolute_position = val


class MoveRelativeParams():

    def __init__(self, tlmc_move_relative_params):
        self._relative_distance = 0
        if type(tlmc_move_relative_params) == TLMC_MoveRelativeParams:
            self._relative_distance = c_int32(
                tlmc_move_relative_params.relativeDistance).value

    @property
    def relative_distance(self):
        return self._relative_distance

    @relative_distance.setter
    def realtive_distance(self, val):
        self._relative_distance = val

class PhysicalUnit():

    def __init__(self):
        self._physical_value = 0
        self._unit_return = 0
        

    @property
    def physical_value(self):
        return self._physical_value
    
    @physical_value.setter
    def physical_value(self, val):
        self._physical_value = val

    @property
    def unit_return(self):
        return self._unit_return
    
    @unit_return.setter
    def unit_return(self, val):
        self._unit_return = val

class PositionLoopParams():

    def __init__(self, tlmc_position_loop_params):
        self._proportional = 0
        self._integral = 0
        self._integral_limit = 0
        self._derivative = 0
        self._servo_cycles = 0
        self._scale = 0
        self._velocity_feed_forward = 0
        self._acceleration_feed_forward = 0
        self._error_limit = 0

        if type(tlmc_position_loop_params) == TLMC_PositionLoopParams:
            self._proportional = c_uint16(
                tlmc_position_loop_params.proportional).value
            self._integral = c_uint16(tlmc_position_loop_params.integral).value
            self._integral_limit = c_uint32(
                tlmc_position_loop_params.integralLimit).value
            self._derivative = c_uint16(
                tlmc_position_loop_params.derivative).value
            self._servoCycles = c_uint16(
                tlmc_position_loop_params.servoCycles).value
            self._scale = c_uint16(tlmc_position_loop_params.scale).value
            self._velocity_feed_forward = c_uint16(
                tlmc_position_loop_params.velocityFeedForward).value
            self._acceleration_feed_forward = c_uint16(
                tlmc_position_loop_params.accelerationFeedForward).value
            self._error_limit = c_uint32(
                tlmc_position_loop_params.errorLimit).value

    @property
    def proportional(self):
        return self._proportional

    @proportional.setter
    def proportional(self, val):
        self._proportional = val

    @property
    def integral(self):
        return self._integral

    @integral.setter
    def integral(self, val):
        self._integral = val

    @property
    def integral_limit(self):
        return self._integral_limit

    @integral_limit.setter
    def integral_limit(self, val):
        self._integral_limit = val

    @property
    def derivative(self):
        return self._derivative

    @derivative.setter
    def derivative(self, val):
        self._derivative = val

    @property
    def servo_cycles(self):
        return self._servo_cycles

    @servo_cycles.setter
    def servo_cycles(self, val):
        self._servo_cycles = val

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, val):
        self._scale = val

    @property
    def velocity_feed_forward(self):
        return self._velocity_feed_forward

    @velocity_feed_forward.setter
    def velocity_feed_forward(self, val):
        self._velocity_feed_forward = val

    @property
    def acceleration_feed_forward(self):
        return self._acceleration_feed_forward

    @acceleration_feed_forward.setter
    def acceleration_feed_forward(self, val):
        self._acceleration_feed_forward = val

    @property
    def error_limit(self):
        return self._error_limit

    @error_limit.setter
    def error_limit(self, val):
        self._error_limit = val


class PZ_MaxOutputVoltageParams():

    def __init__(self, tlmc_pz_max_output_voltage_params):
        self._max_output_voltage = 0
        self._voltage_limit = 0

        if type(tlmc_pz_max_output_voltage_params) == TLMC_PZ_MaxOutputVoltageParams:
            self._max_output_voltage = c_uint16(
                tlmc_pz_max_output_voltage_params.maxOutputVoltage).value
            self._voltage_limit = TLMC_PZ_VoltageLimit(
                tlmc_pz_max_output_voltage_params.voltageLimit).value

    @property
    def max_output_voltage(self):
        return self._max_output_voltage

    @max_output_voltage.setter
    def max_output_voltage(self, val):
        self._max_output_voltage = val

    @property
    def voltage_limit(self):
        return self._voltage_limit

    @voltage_limit.setter
    def voltage_limit(self, val):
        self._voltage_limit = val


class PZ_OutputVoltageControlSourceParams():

    def __init__(self, tlmc_pz_output_voltage_source_params):
        self._source = 0

        if type(tlmc_pz_output_voltage_source_params) == TLMC_PZ_OutputVoltageControlSourceParams:
            self._source = TLMC_PZ_OutputVoltageControlSource(
                tlmc_pz_output_voltage_source_params.source).value

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, val):
        self._source = val


class PZ_OutPutWaveformLoopTableSample():

    def __init__(self, tlmc_pz_output_waveform_loop_table_sample):
        self._index = 0
        self._voltage = 0

        if type(tlmc_pz_output_waveform_loop_table_sample) == TLMC_PZ_OutputWaveformLoopTableSample:
            self._index = c_uint16(
                tlmc_pz_output_waveform_loop_table_sample.index).value
            self._voltage = c_int16(
                tlmc_pz_output_waveform_loop_table_sample.voltage).value

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, val):
        self._index = val

    @property
    def voltage(self):
        return self._voltage

    @voltage.setter
    def voltage(self, val):
        self._voltage = val


class PZ_OutputWaveformParams():

    def __init__(self, pz_output_waveform_params):
        self._mode = 0
        self._number_of_samples_per_cycle = 0
        self._number_of_cycles = 0
        self._inter_sample_delay = 0
        self._per_cycle_delay = 0
        self._post_cycle_delay = 0
        self._output_trigger_start_index = 0
        self._output_trigger_width = 0
        self._number_of_samples_between_trigger_repetition = 0

        if type(pz_output_waveform_params) == TLMC_PZ_OutputWaveformParams:
            self._mode = TLMC_PZ_OutputWaveformOperartingMode(
                c_uint16(pz_output_waveform_params.mode).value)
            self._number_of_samples_per_cycle = c_uint16(
                pz_output_waveform_params.numberOfSamplesPerCycle).value
            self._number_of_cycles = c_uint16(
                pz_output_waveform_params.numberOfCycles).value
            self._inter_sample_delay = c_int32(
                pz_output_waveform_params.interSampleDelay).value
            self._pre_cycle_delay = c_int32(
                pz_output_waveform_params.preCycleDelay).value
            self._post_cycle_delay = c_int32(
                pz_output_waveform_params.postCycleDelay).value
            self._output_trigger_start_index = c_uint16(
                pz_output_waveform_params.outputTriggerStartIndex).value
            self._output_trigger_width = c_int32(
                pz_output_waveform_params.outputTriggerWidth).value
            self._number_of_samples_between_trigger_repetition = c_uint16(
                pz_output_waveform_params.numberOfSamplesBetweenTriggerRepetition).value

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, val):
        self._mode = val

    @property
    def number_of_samples_per_cycle(self):
        return self._number_of_samples_per_cycle

    @number_of_samples_per_cycle.setter
    def number_of_samples_per_cycle(self, val):
        self._number_of_samples_per_cycle = val

    @property
    def number_of_cycles(self):
        return self._number_of_cycles

    @number_of_cycles.setter
    def number_of_cycles(self, val):
        self._number_of_cycles = val

    @property
    def inter_sample_delay(self):
        return self._inter_sample_delay

    @inter_sample_delay.setter
    def inter_sample_delay(self, val):
        self._inter_sample_delay = val

    @property
    def pre_cycle_delay(self):
        return self._pre_cycle_delay

    @pre_cycle_delay.setter
    def pre_cycle_delay(self, val):
        self._pre_cycle_delay = val

    @property
    def post_cycle_delay(self):
        return self._post_cycle_delay

    @post_cycle_delay.setter
    def post_cycle_delay(self, val):
        self._post_cycle_delay = val

    @property
    def output_trigger_start_index(self):
        return self._output_trigger_start_index

    @output_trigger_start_index.setter
    def output_trigger_start_index(self, val):
        self._output_trigger_start_index = val

    @property
    def output_trigger_width(self):
        return self._output_trigger_width

    @output_trigger_width.setter
    def output_trigger_width(self, val):
        self._output_trigger_width = val

    @property
    def number_of_samples_between_trigger_repetition(self):
        return self._number_of_samples_between_trigger_repetition

    @number_of_samples_between_trigger_repetition.setter
    def number_of_samples_between_trigger_repetition(self, val):
        self._number_of_samples_between_trigger_repetition = val


class PZ_PositionLoopParams():

    def __init__(self, tlmc_position_loop_params):
        self._proportional = 0
        self._integral = 0

        if type(tlmc_position_loop_params) == TLMC_PZ_PositionLoopParams:
            self._proportional = c_uint16(
                tlmc_position_loop_params.proportional).value
            self._integral = c_uint16(tlmc_position_loop_params.integral).value

    @property
    def proportional(self):
        return self._proportional

    @proportional.setter
    def proportional(self, val):
        self._proportional = val

    @property
    def integral(self):
        return self._integral

    @integral.setter
    def integral(self, val):
        self._integral = val


class PZ_SlewRateParams():

    def __init__(self, pz_slew_rate_params):
        self._open_slew_rate = 0
        self._closed_loop_slew_rate = 0

        if type(pz_slew_rate_params) == TLMC_PZ_SlewRateParams:
            self._open_slew_rate = c_uint16(
                pz_slew_rate_params.openSlewRate).value
            self._closed_loop_slew_rate = c_uint16(
                pz_slew_rate_params.closedLoopSlewRate).value

    @property
    def open_slew_rate(self):
        return self._open_slew_rate

    @open_slew_rate.setter
    def open_slew_rate(self, val):
        self._open_slew_rate = val

    @property
    def closed_loop_slew_rate(self):
        return self._closed_loop_slew_rate

    @closed_loop_slew_rate.setter
    def closed_loop_slew_rate(self, val):
        self._closed_loop_slew_rate = val


class PZ_Status():

    def __init__(self, pz_status):
        self._output_voltage = 0
        self._position = 0
        self._status_bits = 0

        if type(pz_status) == TLMC_PZ_Status:
            self._output_voltage = c_int16(pz_status.outputVoltage).value
            self._position = c_int16(pz_status.position).value
            self._status_bits = TLMC_PZ_StatusBits(pz_status.statusBits).value

    @property
    def output_voltage(self):
        return self._output_voltage

    @output_voltage.setter
    def output_voltage(self, val):
        self._output_voltage = val

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, val):
        self._position = val

    @property
    def status_bits(self):
        return self._status_bits

    @status_bits.setter
    def status_bits(self, val):
        self._status_bits = val


class StageAxisParams():

    def __init__(self, tlmc_stage_axis_params):
        self._type_id = 0
        self._axis_id = 0
        self._part_number = 0
        self._serial_number = 0
        self._counter_per_unit = 0
        self._min_position = 0
        self._max_position = 0
        self._max_acceleration = 0
        self._max_deceleration = 0
        self._max_velocity = 0
        self._gear_box_ratio = 0

        if type(tlmc_stage_axis_params) == TLMC_StageAxisParams:
            self._type_id = TLMC_StageAxis_TypeId(
                c_uint16(tlmc_stage_axis_params.typeId).value)
            self._axis_id = TLMC_StageAxis_AxisId(
                c_uint16(tlmc_stage_axis_params.axisID).value)
            self._part_number = c_char(tlmc_stage_axis_params.partNumber).value
            self._serial_number = c_uint32(
                tlmc_stage_axis_params.serialNumber).value
            self._counts_per_unit = c_uint32(
                tlmc_stage_axis_params.countesPerUnit).value
            self._min_position = c_uint32(
                tlmc_stage_axis_params.minPosition).value
            self._max_position = c_int32(
                tlmc_stage_axis_params.maxPosition).value
            self._max_acceleration = c_uint32(
                tlmc_stage_axis_params.maxAcceleration).value
            self._max_deceleration = c_uint32(
                tlmc_stage_axis_params.maxDeceleration).value
            self._maxVelocity = c_uint32(
                tlmc_stage_axis_params.maxVelocity).value
            self._gear_box_ratio = c_uint16(
                tlmc_stage_axis_params.gearBoxRatio).value

    @property
    def type_id(self):
        return self._type_id

    @type_id.setter
    def type_id(self, val):
        self._type_id = val

    @property
    def axis_id(self):
        return self._axis_id

    @axis_id.setter
    def axis_id(self, val):
        self._axis_id = val

    @property
    def part_number(self):
        return self._part_number

    @part_number.setter
    def part_number(self, val):
        self._part_number = val

    @property
    def serial_number(self):
        return self._serial_number

    @serial_number.setter
    def serial_number(self, val):
        self._serial_number = val

    @property
    def counts_per_unit(self):
        return self._counter_per_unit

    @counts_per_unit.setter
    def counts_per_unit(self, val):
        self._counter_per_unit = val

    @property
    def min_position(self):
        return self._min_position

    @min_position.setter
    def min_position(self, val):
        self._min_position = val

    @property
    def max_position(self):
        return self._max_position

    @max_position.setter
    def max_position(self, val):
        self._max_position = val

    @property
    def max_acceleration(self):
        return self._max_acceleration

    @max_acceleration.setter
    def max_acceleration(self, val):
        self._max_acceleration = val

    @property
    def max_deceleration(self):
        return self._max_deceleration

    @max_deceleration.setter
    def max_deceleration(self, val):
        self._max_deceleration = val

    @property
    def max_velocity(self):
        return self._max_velocity

    @max_velocity.setter
    def max_velocity(self, val):
        self._max_velocity = val

    @property
    def gear_box_ratio(self):
        return self._gear_box_ratio

    @gear_box_ratio.setter
    def gear_box_ratio(self, val):
        self._gear_box_ratio = val


class StepperTriggerParams():

    def __init__(self, tlmc_trigger_params_for_stepper):
        self._modes = 0

        if type(tlmc_trigger_params_for_stepper) == TLMC_TriggerParamsForStepper:
            self._modes = TLMC_TriggerModesForStepper(
                c_uint8(tlmc_trigger_params_for_stepper.modes).value)

    @property
    def modes(self):
        return self._modes

    @modes.setter
    def modes(self, val):
        self._modes = val


class StepperLoopParams():

    def __init__(self, tlmc_stepper_loop_params):
        self._loop_mode = 0
        self._proportional = 0
        self._integral = 0
        self._differential = 0
        self._output_clip = 0
        self._ouput_tolerance = 0
        self._microsteps_per_encoder_count = 0

        if type(tlmc_stepper_loop_params) == TLMC_StepperLoopParams:
            self._loop_mode = TLMC_StepperLoopParams_LoopMode(
                c_uint16(tlmc_stepper_loop_params.loopMode).value)
            self._proportional = c_int32(
                tlmc_stepper_loop_params.proportional).value
            self._integral = c_int32(tlmc_stepper_loop_params.intgral).value
            self._differential = c_int32(
                tlmc_stepper_loop_params.differential).value
            self._output_clip = c_int32(tlmc_stepper_loop_params.outputClip)
            self._ouput_tolerance = c_int32(
                tlmc_stepper_loop_params.outputTolerance).value
            self._microsteps_per_encoder_count = c_uint32(
                tlmc_stepper_loop_params.microtepsPerEncoderCount).value

    @property
    def loop_mode(self):
        return self._loop_mode

    @loop_mode.setter
    def loop_mode(self, val):
        self._loop_mode = val

    @property
    def proportional(self):
        return self._proportional

    @proportional.setter
    def proportional(self, val):
        self._proportional = val

    @property
    def integral(self):
        return self._integral

    @integral.setter
    def integral(self, val):
        self._integral = val

    @property
    def differential(self):
        return self._differential

    @differential.setter
    def differential(self, val):
        self._differential = val

    @property
    def output_clip(self):
        return self._output_clip

    @output_clip.setter
    def output_clip(self, val):
        self._output_clip = val

    @property
    def output_tolerance(self):
        return self._ouput_tolerance

    @output_tolerance.setter
    def ouput_tolerance(self, val):
        self._ouput_tolerance = val


class TLMCAdcInputs():

    def __init__(self, tlmc_adc_inputs):
        self._adc_input_1 = 0
        self._adc_input_2 = 0

        if type(tlmc_adc_inputs) == TLMC_AdcInputs():
            self._adc_input_1 = c_uint16(tlmc_adc_inputs.adcInput1).value
            self._adc_input_2 = c_uint16(tlmc_adc_inputs.adcInput2).value

    @property
    def adc_input_1(self):
        return self._adc_input_1

    @adc_input_1.setter
    def adc_input(self, val):
        self._adc_input_1 = val

    @property
    def adc_input_2(self):
        return self._adc_input_2

    @adc_input_2.setter
    def adc_input_2(self, val):
        self._adc_input_2 = val


class TLMCCurrentLoopParams():

    def __init__(self, tlmc_current_loop_params):
        self._phase = 0
        self._proportional = 0
        self._integral = 0
        self._integral_limit = 0
        self._integral_dead_band = 0
        self._feed_forward = 0

        if type(tlmc_current_loop_params) == TLMC_CurrentLoopParams():
            self._phase = TLMC_CurrentLoopPhase(
                c_uint16(tlmc_current_loop_params.phase).value)
            self._proportional = c_uint16(
                tlmc_current_loop_params.proportional).value
            self._integral = c_uint16(tlmc_current_loop_params.integral).value
            self._integral_limit = c_uint16(
                tlmc_current_loop_params.integralLimit).value
            self._integral_dead_band = c_uint16(
                tlmc_current_loop_params.integralDeadBand).value
            self._feed_forward = c_uint16(
                tlmc_current_loop_params.feedForward).value

    @property
    def phase(self):
        return self._phase

    @phase.setter
    def phase(self, val):
        self._phase = val

    @property
    def proportional(self):
        return self._proportional

    @proportional.setter
    def proportional(self, val):
        self._proportional = val

    @property
    def integral(self):
        return self._integral

    @integral.setter
    def integral(self, val):
        self._integral = val

    @property
    def integral_limit(self):
        return self._integral_limit

    @integral_limit.setter
    def integral_limit(self, val):
        self._integral_limit = val

    @property
    def feed_forward(self):
        return self._feed_forward

    @feed_forward.setter
    def feed_forward(self, val):
        self._feed_forward = val


class TLMCPowerParams():

    def __int__(self, tlmc_power_params):
        self._rest_factor = 0
        self._move_factor = 0

        if type(tlmc_power_params) == TLMC_PowerParams():
            self._rest_factor = c_uint16(tlmc_power_params.restFactor).value
            self._move_factor = c_uint16(tlmc_power_params.moveFactor).value

    @property
    def rest_factor(self):
        return self._rest_factor

    @rest_factor.setter
    def rest_factor(self, val):
        self._rest_factor = val

    @property
    def move_factor(self):
        return self._move_factor

    @move_factor.setter
    def move_factor(self, val):
        self._move_factor = val


class TLMCRichResponse():

    def __init__(self, tlmc_rich_response):
        self._message_id = 0
        self._code = 0
        self._notes = 0

        if type(tlmc_rich_response) == TLMC_RichResponse():
            self._message_id = c_uint16(tlmc_rich_response.messageId).value
            self._code = c_uint16(tlmc_rich_response.code).value
            self._notes = str(tlmc_rich_response.notes)

    @property
    def message_id(self):
        return self._message_id

    @message_id.setter
    def message_id(self, val):
        self._message_id = val

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, val):
        self._code = val

    @property
    def notes(self):
        return self._notes

    @notes.setter
    def notes(self, val):
        self._notes = val


class TLMCSetting():

    def __init__(self, tlmc_setting):
        self._value_type = 0  
        self._is_value_set = False
        self._value = 0
        self._scale_type = 0
        self._unit_type = 0
        self._name = 0
        self._display_name = 0
        self._is_read_only = False
        self._has_discrete_values = False
        self._has_min = False
        self._has_max = False
        self._min_value = 0
        self._max_value = 0

        if type(tlmc_setting) == TLMC_Setting:
            self._value_type = TLMC_ValueType(
                c_uint8(tlmc_setting.valueType).value)
            self._is_value_set = c_bool(tlmc_setting.isValueSet).value
            match self._value_type:
                case TLMC_ValueType.TLMC_ValueType_int64:
                    self._value = c_uint64(tlmc_setting.value).value
                    if self._has_min == True:
                        self._min_value = c_uint64(tlmc_setting.minValue).value
                    if self._has_max == True:
                        self._max_value = c_uint64(tlmc_setting.maxValue).value
                case TLMC_ValueType.TLMC_ValueType_bool:
                    self._value = c_bool(tlmc_setting.value).value
                    if self._has_min == True:
                        self._min_value = c_bool(tlmc_setting.minValue).value
                    if self._has_max == True:
                        self._max_value = c_bool(tlmc_setting.maxValue).value
                case TLMC_ValueType.TLMC_ValueType_string:
                    self._value = str(tlmc_setting.value)
                    if self._has_min == True:
                        self._min_value = str(tlmc_setting)
                    if self._has_max == True:
                        self.max_value = str(tlmc_setting.maxValue)
            self._scale_type = TLMC_ScaleType(
                c_uint16(tlmc_setting.scaleType).value)
            self._unit_type = TLMC_Unit(c_uint16(tlmc_setting.unitType)).value
            self._name = str(tlmc_setting.name)
            self._display_name = str(tlmc_setting.displayName)
            self._is_read_only = c_bool(tlmc_setting.isReadOnly).value
            self._has_discrete_values = c_bool(tlmc_setting.hasDiscreteValue)
            self._has_min = c_bool(tlmc_setting.hasMin).value
            self._has_max = c_bool(tlmc_setting.hasMax).value

    @property
    def value_type(self):
        return self._value_type

    @value_type.setter
    def value_type(self, val):
        self._value_type = val

    @property
    def is_value_set(self):
        return self._is_value_set

    @is_value_set.setter
    def is_value_set(self, val):
        self._is_value_set = val

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._value = val

    @property
    def scale_type(self):
        return self._scale_type

    @scale_type.setter
    def scale_type(self, val):
        self._scale_type = val

    @property
    def unit_type(self):
        return self._unit_type

    @unit_type.setter
    def unit_type(self, val):
        self._unit_type = val

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        self._name = val

    @property
    def display_name(self):
        return self._display_name

    @display_name.setter
    def display_name(self, val):
        self._display_name = val

    @property
    def is_read_only(self):
        return self._is_read_only

    @is_read_only.setter
    def is_read_only(self, val):
        self._is_read_only = val

    @property
    def has_discrete_values(self):
        return self._has_discrete_values

    @has_discrete_values.setter
    def has_discrete_value(self, val):
        self._has_discrete_values = val

    @property
    def has_min(self):
        return self._has_min

    @has_min.setter
    def has_min(self, val):
        self._has_min = val

    @property
    def has_max(self):
        return self._has_max

    @has_max.setter
    def has_max(self, val):
        self._has_max = val


class TLMCTrackSettleParams():

    def __init__(self, tlmc_track_settle_params):
        self._settle_time = 0
        self._settle_window = 0
        self._track_window = 0

        if type(tlmc_track_settle_params) == TLMC_TrackSettleParams():
            self._settle_time = c_uint16(
                tlmc_track_settle_params.settleTime).value
            self._settle_window = c_uint16(
                tlmc_track_settle_params.settleWindow).value
            self._track_window = c_uint16(
                tlmc_track_settle_params.trackWindow).value

    @property
    def settle_time(self):
        return self._settle_time

    @settle_time.setter
    def settle_time(self, val):
        self._settle_time = val

    @property
    def settle_window(self):
        return self._settle_window

    @settle_window.setter
    def settle_window(self, val):
        self._settle_window = val

    @property
    def track_window(self):
        return self._track_window

    @track_window.setter
    def track_window(self, val):
        self._track_winodw = val


class TLMCUniversalStatus():

    def __init__(self, tlmc_universal_status):
        self._position = 0
        self._velocity = 0
        self._motor_current = 0
        self.status_bits = 0

        if type(tlmc_universal_status) == TLMC_UniversalStatus():
            self._position = c_int32(tlmc_universal_status.position).value
            self._velocity = c_int16(tlmc_universal_status.velocity).value
            self._motor_current = c_int16(
                tlmc_universal_status.motorCurrent).value
            self._status_bits = TLMC_UniversalStatusBits(
                c_uint32(tlmc_universal_status.statusBits).value)

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, val):
        self._position = val

    @property
    def velocity(self):
        return self._velocity

    @velocity.setter
    def velocity(self, val):
        self._velocity = val

    @property
    def motor_curret(self):
        return self._motor_current

    @motor_curret.setter
    def motor_current(self, val):
        self._motor_current = val

    @property
    def status_bits(self):
        return self._status_bits

    @status_bits.setter
    def status_bits(self, val):
        self._status_bits = val

class UnitConversionResult():

    def __init__(self, value_list):
        self._value = int(value_list[0])
        self._unit = int(value_list[1])

    @property
    def converted_value(self):
        return(self._value)
    
    @property
    def unit(self):
        return(self._unit)
    

class VelocityParams():

    def __init__(self, tlmc_velocity_params):
        self._min_velocity = 0
        self._acceleration = 0
        self._max_velocity = 0
        if type(tlmc_velocity_params) == TLMC_VelocityParams:
            self._min_velocity = c_uint32(
                tlmc_velocity_params.minVelocity).value
            self._acceleration = c_uint32(
                tlmc_velocity_params.acceleration).value
            self._max_velocity = c_uint32(
                tlmc_velocity_params.maxVelocity).value

    @property
    def min_velocity(self):
        return self._min_velocity

    @min_velocity.setter
    def min_velocity(self, val):
        self._min_velocity = val

    @property
    def acceleration(self):
        return self._acceleration

    @acceleration.setter
    def acceleration(self, val):
        self._acceleration = val

    @property
    def max_velocity(self):
        return self._max_velocity

    @max_velocity.setter
    def max_velocity(self, val):
        self._max_velocity = val
