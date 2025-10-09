from xa_sdk.native_sdks.xa_sdk import XASDK
from xa_sdk.shared.xa_shared_types import *
from xa_sdk.shared.xa_shared_types import XADevice

class KST201(XADevice):
    """
    Thorlabs Kcube stepper motor controller. 
    """
    # Device properties.

    def device_id(self):
        return super().device_id

    def device_id(self, val):
        super().device_id(self, val)

    def transport(self):
        return super().transport

    def transport(self, val):
        super().transport(self, val)

    # Methods generic to each device.
    def add_user_message_to_log(self, user_message):
        return super().add_user_message_to_log(user_message)

    def close(self):
        super().close()

    def disconnect(self):
        super().disconnect()

    def get_device_info(self, max_wait_in_milliseconds):
        return super().get_device_info(max_wait_in_milliseconds)

    def get_hardware_info(self, wait_in_milliseconds):
        return super().get_hardware_info(wait_in_milliseconds)

    def get_method_list(self):
        cls = KST201
        return super().get_method_list(cls)

    def get_setting(self, pSettings_name, max_wait_in_milliseconds):
        return super().get_setting(pSettings_name, max_wait_in_milliseconds)

    def get_setting_as_string(self, pBuffer, buffer_length, pResult_length, TLMC_setting_string_format, include_read_only_items):
        return super().get_setting_as_string(pBuffer, buffer_length, pResult_length, TLMC_setting_string_format, include_read_only_items)

    def get_setting_count(self):
        return super().get_setting_count()

    def get_setting_discrete_values(self, pSettings_name, pBuffer, buffer_length, result_length):
        return super().get_setting_discrete_values(pSettings_name, pBuffer, buffer_length, result_length)

    def get_settings(self, source_start_index, number_of_items, pNumber_of_items_copied):
        return super().get_settings(source_start_index, number_of_items, pNumber_of_items_copied)

    def identify(self):
        super().identify()

    def set_setting(self, pSettings_name):
        super().set_setting(pSettings_name)

    def set_settings_from_string(self, pSettings_name):
        return super().set_settings_from_string(pSettings_name)

    # Methods unique to motor types (moves and motor parameters)

    def __init__(self, handle, connection_type, operating_mode):
        super().__init__()
        self.native_api = XASDK()
        self.device_handle = handle
        device = self.native_api.open(handle, connection_type, operating_mode)
        if device.value > 0:
            self.device_handle = device

    def convert_from_device_units_to_physical(self, TLMC_scale_type: TLMC_ScaleType, device_value: int):
        """
        Converts a value expressed in device-specific units into an equivalent value expressed in physical units.
        """
        ret = self.native_api.convert_from_device_units_to_physical(
            self.device_handle, TLMC_scale_type, device_value)
        return UnitConversionResult(ret)
    
    def convert_from_physical_to_device(self, TLMC_scale_type: TLMC_ScaleType, TLMC_unit_type: TLMC_Unit, physical_value: int):
        """
        Converts a value expressed in device-specific units into an equivalent value expressed in device units. 
        """
        ret = self.native_api.convert_from_physical_to_device(
            self.device_handle, TLMC_scale_type, TLMC_unit_type, physical_value)
        return ret
    
    def get_bow_index(self, index_val: TLMC_BowIndex, max_wait_in_milliseconds: int):
        """
        This function is used to retrieve the bow index value. 
        """

        ret = self.native_api.get_bow_index(
            self.device_handle, index_val, max_wait_in_milliseconds)
        return ret

    def get_connected_product(self):
        """
        This function is used to retrieve the name of the product connected to a device. 
        """
        ret = self.native_api.get_connected_product(self.device_handle)
        return ret

    def get_connected_product_info(self):
        """
        Retrieve information about the product connected to a device. 
        """
        ret = self.native_api.get_connected_product_info(self.device_handle)
        return ConnectedProductInfo(ret)

    def get_connected_products_supported(self):
        """
        This function is used to retrieve a comma-separated list of the connected products supported by a device.
        """
        ret = self.native_api.get_connected_products_supported(
            self.device_handle)
        return ret

    def get_digital_output_params(self, max_wait_in_milliseconds: int):
        """
        This function is used to retrieve the state of all digital outputs.
        """
        self.native_api.get_digital_output_params(
            self.device_handle, max_wait_in_milliseconds)

    def get_enable_state(self, max_wait_in_milliseconds: int):
        """
        Returns the enable state of the controller or channel. 
        """
        self.native_api.get_enable_state(
            self.device_handle, max_wait_in_milliseconds)

    def get_general_move_params(self, max_wait_in_milliseconds: int):
        """
        This function is used to retrieve the general movement parameters, i.e. backlash distance. 
        """
        ret = self.native_api.get_general_move_params(
            self.device_handle, max_wait_in_milliseconds)
        return GeneralMoveParams(ret)

    def get_home_params(self, max_wait_in_milliseconds: int):
        """
        Returns the home parameters structure containing the homing velocity and home offset distance. 
        """
        ret = self.native_api.get_home_params(
            self.device_handle, max_wait_in_milliseconds)
        return HomeParams(ret)

    def get_kcube_io_trigger_params(self, max_wait_in_milliseconds: int):
        """
        Returns the trigger settings for the controller. 
        This includes the trigger mode and polarity for both ports.
        """
        ret = self.native_api.get_kcube_io_trigger_params(
            self.device_handle, max_wait_in_milliseconds)
        return KcubeIoTriggerParams(ret)

    def get_kcube_mmi_lock_state(self, max_wait_in_milliseconds: int):
        """
        This function is used to retrieve the K-Cube MMI lock state.
        """
        ret = self.native_api.get_kcube_mi_lock_state(
            self.device_handle, max_wait_in_milliseconds)
        return ret

    def get_kcube_mmi_params(self, max_wait_in_milliseconds: int):
        """
        This function is used to retrieve the K-Cube MMI parameters. 
        """
        ret = self.native_api.get_kcube_mmi_params(
            self.device_handle, max_wait_in_milliseconds)
        return KcubeMmiParams(ret)

    def get_kcube_position_trigger_params(self, max_wait_in_milliseconds):
        """
        This function is used to retrieve the kcube position trigger parameters
        """
        ret = self.native_api.get_kcube_position_trigger_params(
            self.device_handle, max_wait_in_milliseconds)
        return KcubePositionTriggerParams(ret)

    def get_limit_switch_params(self, max_wait_in_milliseconds: int):
        """
        This function is used to retrieve the limit switch parameters. 
        """
        ret = self.native_api.get_limit_switch_params(
            self.device_handle, max_wait_in_milliseconds)
        return LimitSwitchParams(ret)

    def get_move_absolute_params(self, max_wait_in_milliseconds: int):
        """
        This function is used to retrieve the target position used for move_absolute().
        """
        ret = self.native_api.get_move_absolute_params(
            self.device_handle, max_wait_in_milliseconds)
        return MoveAbsoluteParams(ret)

    def get_move_jog_params(self, max_wait_in_milliseconds: int):
        """
        This function retrieves the jog settings uploaded to the device. Including the min velcity, max velocity, and acceleration. 
        """
        ret = self.native_api.get_move_jog_params(
            self.device_handle, max_wait_in_milliseconds)
        return JogParams(ret)

    def get_move_relative_params(self, max_wait_in_milliseconds: int):
        """
        This function retrieves the step size used for move_relative().
        """
        ret = self.native_api.get_move_relative_params(
            self.device_handle, max_wait_in_milliseconds)
        return MoveRelativeParams(ret)

    def get_position_counter(self, max_wait_in_milliseconds: int):
        """
        This function retrieves the position of the stage/actuator. 
        """
        ret = self.native_api.get_position_counter(
            self.device_handle, max_wait_in_milliseconds)
        return ret

    def get_position_loop_params(self, position_loop_scenario: TLMC_PositionLoopScenario, max_wait_in_milliseconds: int):
        """
        This function retrieves the position loop parameters. 
        """
        ret = self.native_api.get_position_loop_params(
            self.device_handle, position_loop_scenario, max_wait_in_milliseconds)
        return PositionLoopParams(ret)

    def get_power_params(self, max_wait_in_milliseconds: int):
        """
        This function retrieves the power parameters from teh device. Including, the move and rest factor. 
        """
        ret = self.native_api.get_power_params(
            self.device_handle, max_wait_in_milliseconds)
        return TLMCPowerParams(ret)

    def get_status_item(self, status_item_id: TLMC_StatusItemIds, status_item: TLMC_StatusItem):
        """
        This function is used to retrieve information about a setting.
        """
        ret = self.native_api.get_status_item(self.device_handle, status_item_id, status_item)
        return ret

    def get_status_item_count(self):
        """
        This function retrieves the number of status items available on a device. 
        """
        ret = self.native_api.get_status_item_count(self.device_handle)
        return ret

    def get_status_items(self, start_index: int, number_of_items: int, number_of_items_copied: int):
        """
        This function may be used to retrieve a contiguous block of TLMC_StatusItem information structures from those available.
        You may request as many, or as few, as you would like to process in a single call.This may be useful where you have limited heap space,
        or can only allocate variables on the stack and have a limited stack size.
        """
        ret = self.native_api.get_status_items(self.device_handle, start_index, number_of_items, number_of_items_copied)
        return ret
    
    def get_stepper_status(self, max_wait_in_milliseconds: int):
        """
        This function is used to retrieve the stepper status. 
        """
        ret = self.native_api.get_stepper_status(
            self.handle, max_wait_in_milliseconds)
        return ret

    def get_universal_status(self, max_wait_in_milliseconds: int):
        """
        Returns the universal status parameters of the motor. Including the current position, 
        velocity, motor current, and status bits.
        """
        ret = self.native_api(self.device_handle, max_wait_in_milliseconds)
        return TLMCUniversalStatus(ret)

    def get_universal_status_bits(self, max_wait_in_milliseconds: int):
        """
        This function retrieves the universal status bits.
        """
        ret = self.native_api(self.device_handle, max_wait_in_milliseconds)
        return ret

    def get_velocity_params(self, max_wait_in_milliseconds: int):
        """
        This function Retrieves the velocity parameters being used by the motor. 
        Includes min_velocity, max_velocity, and acceleration.
        """
        ret = self.native_api.get_velocity_params(
            self.device_handle, max_wait_in_milliseconds)
        return VelocityParams(ret)

    def home(self, timeout: int):
        """
        Performs a home command which returns the motor to it's predefined home position.
        Velocity and offset distance changed by set_home_params(). 
        """
        self.native_api.home(self.device_handle, timeout)

    def move_absolute(self, move_mode: TLMC_MoveModes, position: int, max_wait_in_milliseconds: int):
        """
        Initiates an absolute move, to specified position.
        """
        self.native_api.move_absolute(self.device_handle, move_mode, position, max_wait_in_milliseconds)

    def move_continuous(self, direction: TLMC_MoveDirection, max_wait_in_milliseconds: int):
        """
        Initiates a continuous move in the specified direction. 
        """
        self.native_api.move_continous(self.device_handle, direction, max_wait_in_milliseconds)

    def move_jog(self, direction: TLMC_MoveDirection, max_wait_in_milliseconds: int):
        """
        Initiates a jog move. Uses settings changed in set_move_jog_params().
        """
        self.native_api.move_jog(self.device_handle, direction, max_wait_in_milliseconds)

    def move_relative(self, move_mode: TLMC_MoveModes, step_size: int, max_wait_in_milliseconds: int):
        """
        Initiates a relative move. If using TLMC_MoveMode.RelativeByProgrammed
        step_size is set using set_move_relative_params and should be 0 or TLMC_Unused.
        """
        self.native_api.move_relative(self.device_handle, move_mode, step_size, max_wait_in_milliseconds)

    def restore_to_factory_defaults(self):
        """
        Sets the stage back to it's default settings.
        """
        self.native_api.restore_to_factory_defaults(self.device_handle)

    def set_bow_index(self, new_bow_index: TLMC_BowIndex):
        """
        Sets the bow index for the motor. 
        """
        self.native_api.set_bow_index(self.device_handle, new_bow_index)

    def set_connected_product(self, product_name: str):
        self.native_api.set_connected_product(self.device_handle, product_name)
        """
        Sets the designated actutor to a channel or device object. 
        """

    def set_connected_product_info(self, product_name: str, axis_type: TLMC_ConnectedProductAxisType,
                                movement_type: TLMC_ConnectedProductMovementType,
                                unit_type: TLMC_Unit, distance_scale_factor: int, velocity_scale_factor: int,
                                acceleration_scale_factor: int, min_position: int, max_position: int,
                                max_velocity: int, max_acceleration: int):
        """
        Sets property info of designated actuator to device or channel object.
        """
        self.native_api.set_connected_product_info(self.device_handle, product_name, axis_type, movement_type,
                                                   unit_type, distance_scale_factor, velocity_scale_factor,
                                                   acceleration_scale_factor, min_position, max_position,
                                                   max_velocity, max_acceleration)

    def set_digital_ouput_params(self, new_ouput_state: TLMC_DigitalOutput):
        """
        Sets the output state of the digital output pins. 
        Triggering might need to be disabled for this to be used. 
        """
        self.native_api.set_digital_output_params(
            self.device_handle, new_ouput_state)

    def set_enable_state(self, enable_state: TLMC_EnableState):
        """
        Enables the motor channel. 
        """
        self.native_api.set_enable_state(self.device_handle, enable_state)

    def set_encoder_counter(self, new_encoder_counter: int):
        """
        Changes the current encoder count. 
        """
        self.native_api.set_encoder_counter(
            self.device_handle, new_encoder_counter)

    def set_end_of_message_mode(self, mode: TLMC_EndOfMessagesMode):
        """
        Changes the end of message mode. 
        """
        self.native_api.set_end_of_message_mode(mode)

    def set_general_move_params(self, backlash_distance: int):
        """
        Changes the backlash distance used by the actuator. 
        """
        self.native_api.set_general_move_params(
            self.device_handle, backlash_distance)

    def set_home_params(self, direction: TLMC_MoveDirection, limit_switch: TLMC_HomeLimitSwitches, velocity: int, offset_distance: int):
        """
        Changes the max velocity and home offset used by home().
        """
        self.native_api.set_home_params(
            self.device_handle, direction, limit_switch, velocity, offset_distance)

    def set_kcube_io_trigger_params(self, trigger_one_mode: TLMC_KcubeIoTriggerMode, trigger_one_polarity: TLMC_KcubeIoTriggerPolarity,
                                    trigger_two_mode: TLMC_KcubeIoTriggerMode, trigger_two_polarity: TLMC_KcubeIoTriggerPolarity):
        """
        Changes the trigger mode and polarity for both IO ports. 
        """
        self.native_api.set_kcube_io_trigger_params(self.device_handle, trigger_one_mode, trigger_one_polarity,
                                                    trigger_two_mode, trigger_two_polarity)

    def set_kcube_mmi_lock_state(self, lock_state: TLMC_KcubeMmiLockState):
        """
        Changes the Kcube mmi lock state.
        """
        self.native_api.set_kcube_mmi_lock_state(
            self.device_handle, lock_state)

    def set_kcube_mmi_params(self, joystick_mode: TLMC_KcubeMmi_JoystickMode, joystick_velocity: int, joystick_acceleration: int,
                             joystick_direction_sense: TLMC_KcubeMmi_JoystickDirectionSense, position_one: int, position_two: int,
                             display_brightness: int, display_timeout: int, display_dim_level: int,
                             position_three: int, joystick_sensitivity: int):
        """
        Changes the joystick and display settings on the kcube.
        """
        self.native_api.set_kcube_mmi_params(self.device_handle, joystick_mode, joystick_velocity, joystick_acceleration,
                                             joystick_direction_sense, position_one, position_two,
                                             display_brightness, display_timeout, display_dim_level,
                                             position_three, joystick_sensitivity)

    def set_kcube_position_trigger_params(self, fwrd_start_position: int, fwrd_interval: int,
                                          fwrd_number_of_pulses: int, rev_start_position: int,
                                          rev_interval: int, rev_number_of_pulses: int, pulse_width: int,
                                          number_of_cycles: int):
        """
        Changes the kcube position trigger settings.
        """
        self.native_api.set_kcube_position_trigger_params(self.device_handle, fwrd_start_position, fwrd_interval,
                                                          fwrd_number_of_pulses, rev_start_position,
                                                          rev_interval, rev_number_of_pulses, pulse_width,
                                                          number_of_cycles)

    def set_limit_switch_params(self, clockwise_limit_mode: TLMC_HardLimitOperatingModes, counter_clockwise_mode: TLMC_HardLimitOperatingModes,
                                clockwise_soft_limit: int, counter_clockwise_soft_limit: int,
                                soft_limit_operating_mode: TLMC_SoftLimitOperatingModes):
        """
        Changes the limit switch settings. 

        ClockwiseLimitMode: 
        CounterClockWiseLimitMode:
        ClockwiseSoftLimit:
        CountercClockwiseSoftLimit:
        SoftLimitOperatingMode:
        """
        self.native_api.set_limit_switch_params(self.device_handle, clockwise_limit_mode, counter_clockwise_mode,
                                                clockwise_soft_limit, counter_clockwise_soft_limit, soft_limit_operating_mode)

    def set_move_absolute_params(self, absolute_position: int):
        """
        Sets the target position used by move_absolute_to_programmed_position().
        """
        self.native_api.set_move_absolute_params(
            self.device_handle, absolute_position)

    def set_move_relative_params(self, move_relative_distance: int):
        """
        Changes the step size used by move_relative_by_programmed_position.
        """
        self.native_api.set_move_relative_params(
            self.device_handle, move_relative_distance)

    def set_move_jog_params(self, step_size: int, min_velocity: int, max_velocity: int, acceleration: int):
        """
        Changes the step size, min velocity, max velocity, and acceleration settings used by move_jog().
        """
        self.native_api.set_move_jog_params(
            self.device_handle, step_size, min_velocity, max_velocity, acceleration)

    def set_position_counter(self, new_position_counter: int):
        """
        Sets a new position counter. 
        """
        self.native_api.set_position_counter(
            self.device_handle, new_position_counter)

    def set_position_loop_params(self, position_loop_scenario: TLMC_PositionLoopScenario, proportional: int,
                                  integral: int, integral_limit: int,
                                 derivative: int, servo_cycles: int, scale: int, velocity_feed_fwrd: int,
                                 acceleration_feed_fwrd: int, error_limit: int):
        """
        Changes the position loop parameters.
        """
        self.native_api.set_position_loop_params(self.device_handle, position_loop_scenario, proportional, integral, integral_limit,
                                                 derivative, servo_cycles, scale, velocity_feed_fwrd,
                                                 acceleration_feed_fwrd, error_limit)

    def set_power_params(self, rest_factor: int, move_factor: int):
        """
        Sets the move and rest factor for the motor. 
        """
        self.native_api.set_power_params(
            self.device_handle, rest_factor, move_factor)

    def set_velocity_params(self, min_velocity: int, acceleration: int, max_velocity: int):
        """
        Changes the min_velocity, max_velocity, and acelleration used by the motor. Affects all moves besides jogs and home.
        """
        self.native_api.set_velocity_params(
            self.device_handle, min_velocity, acceleration, max_velocity)

    def stop(self, stop_mode: TLMC_StopModes, max_wait_in_milliseconds: int):
        """
        Stops last or current method execution. 
        """
        self.native_api.stop(self.device_handle, stop_mode,
                             max_wait_in_milliseconds)
