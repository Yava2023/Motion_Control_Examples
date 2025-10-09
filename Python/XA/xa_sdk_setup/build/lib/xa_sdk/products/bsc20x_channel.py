from xa_sdk.shared.xa_shared_types import XADevice
from xa_sdk.shared.xa_shared_types import *
from xa_sdk.native_sdks.xa_sdk import XASDK

class BSC20XCHANNEL(XADevice):
    """
    Thorlabs benchtop stepper motor channel. 
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
        cls = BSC20XCHANNEL
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

    def set_end_of_message_mode(self, mode):
        super().set_end_of_message_mode(mode)

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
        Converts device unit input into physical units. Arguments used are the scaleType, user deviceValue,
        and the unitType 
        """
        ret = self.native_api.convert_from_device_units_to_physical(
            self.device_handle, TLMC_scale_type, device_value)
        return UnitConversionResult(ret)
    
    def convert_from_physical_to_device(self, TLMC_scale_type: TLMC_ScaleType, TLMC_unit_type: TLMC_Unit, physical_value: int):
        """
        Converts physical unit input into device units. Arguments used are the scaleType, the unitType,
        and the user physicalValue.
        and the unitType 
        """
        ret = self.native_api.convert_from_physical_to_device(
            self.device_handle, TLMC_scale_type, TLMC_unit_type, physical_value)
        return ret
    
    def get_adc_inputs(self, max_wait_in_milliseconds: int):
        """
        Returns the adc inputs. 
        """
        ret = self.native_api.get_adc_inputs(
            self.device_handle, max_wait_in_milliseconds)
        return TLMCAdcInputs(ret)

    def get_bow_index(self,index_value: TLMC_BowIndex, max_wait_in_milliseconds: int):
        """
        Returns the default or previously set bow index. 
        """
        self.native_api.get_bow_index(
            self.device_handle, index_value, max_wait_in_milliseconds)

    def get_connected_product(self):
        """
        Returns product info for actuator/motor connected to device or channel. 
        """
        ret = self.native_api.get_connected_product(self.device_handle)
        return ret

    def get_connected_product_info(self):
        """
        Returns info based on actuator or motor connected to the device and or channel object.
        """
        ret = self.native_api.get_connected_product_info(self.device_handle)
        return ConnectedProductInfo(ret)

    def get_connected_products_supported(self):
        """
        Returns list of compatible Thorlabs motors and actuators.
        """
        ret = self.native_api.get_connected_products_supported(
            self.device_handle)
        return ret

    def get_digital_output_params(self, max_wait_in_milliseconds: int):
        """
        Returns the output state of the digital output pins. 
        """
        self.native_api.get_digital_output_params(
            self.device_handle, max_wait_in_milliseconds)

    def get_enable_state(self, max_wait_in_milliseconds: int):
        """
        Returns the enable state of the cntroller channel. 
        """
        self.native_api.get_enable_state(
            self.device_handle, max_wait_in_milliseconds)

    def get_encoder_counter(self, max_wait_in_milliseconds: int):
        """
        Returns the current encoder count. 
        """
        ret = self.native_api.get_encoder_counter(
            self.device_handle, max_wait_in_milliseconds)
        return ret

    def get_general_move_params(self, max_wait_in_milliseconds: int):
        """
        Returns the amount of backlash being currently used. 
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

    def get_limit_switch_params(self, max_wait_in_milliseconds: int):
        """
        Returns the limit swith settings. Inlcuding the clockwise limit mode, 
        counter-clockwise limit mode, counter clockwise mode, clockwise soft limit,
        counter-clockwise soft limit, and soft limit operating mode. 
        """
        ret = self.native_api.get_limit_switch_params(
            self.device_handle, max_wait_in_milliseconds)
        return LimitSwitchParams(ret)

    def get_move_absolute_params(self, max_wait_in_milliseconds: int):
        """
        Returns the current target position for move_absolute().
        """
        ret = self.native_api.get_move_absolute_params(
            self.device_handle, max_wait_in_milliseconds)
        return MoveAbsoluteParams(ret)

    def get_move_jog_params(self, max_wait_in_milliseconds: int):
        """
        Returns the current jog settings. Including the min velcity, max velocity, and acceleration. 
        """
        ret = self.native_api.get_move_jog_params(
            self.device_handle, max_wait_in_milliseconds)
        return JogParams(ret)

    def get_move_relative_params(self, max_wait_in_milliseconds: int):
        """
        Returns the current step size for move_relative().
        """
        ret = self.native_api.get_move_relative_params(
            self.device_handle, max_wait_in_milliseconds)
        return MoveRelativeParams(ret)

    def get_position_counter(self, max_wait_in_milliseconds: int):
        """
        Returns the current position of the device. 
        """
        ret = self.native_api.get_position_counter(
            self.device_handle, max_wait_in_milliseconds)
        return ret

    def get_power_params(self, max_wait_in_milliseconds: int):
        """
        Returns the move and rest factor for a device.
        """
        ret = self.native_api.get_power_params(
            self.device_handle, max_wait_in_milliseconds)
        return TLMCPowerParams(ret)

    def get_rich_response(self):
        """
        Returns the device rish response.
        """
        ret = self.native_api.get_rich_response(self.device_handle)
        return TLMCRichResponse(ret)

    def get_status(self):
        """
        Returns the device status.
        """
        ret = self.native_api.get_status(self.device_handle)
        return ret

    def get_status_item(self, status_item_id: TLMC_StatusItemIds, status_item: TLMC_StatusItem):
        """
        Returns a specified status item value. 
        """
        ret = self.native_api.get_status_items(self.device_handle, status_item_id, status_item)
        return ret
    
    def get_status_item_count(self):
        """
        Returns the number of avialable status items 
        """
        ret = self.native_api.get_status_item_count(self.device_handle)
        return ret

    def get_status_items(self, start_index: int, number_of_items: int, number_of_items_copied: int):
        """
        Returns all avialable status items. 
        """
        ret = self.native_api.get_status_items(self.device_handle, start_index, number_of_items, number_of_items_copied)
        return ret
    
    def get_stepper_loop_params(self, max_wait_in_milliseconds: int):
        """
        Returns the position loop settings being used. 
        """
        ret = self.native_api.get_stepper_loop_params(
            self.device_handle, max_wait_in_milliseconds)
        return StepperLoopParams(ret)

    def get_stepper_status(self, max_wait_in_milliseconds: int):
        """
        Returns the current status bits from the motor. 
        """
        ret = self.native_api.get_stepper_status(
            self.device_handle, max_wait_in_milliseconds)
        return ret

    def get_trigger_params_for_stepper(self, max_wai_in_milliseconds: int):
        """
        Returns the trigger settings being used by the channel.
        """
        ret = self.native_api.get_trigger_params_for_stepper(
            self.device_handle, max_wai_in_milliseconds)
        return StepperTriggerParams(ret)

    def get_universal_status(self, max_wait_in_milliseconds: int):
        """
        Returns the universal status parameters of the motor. Including the current position, 
        velocity, motor current, and status bits.
        """
        ret = self.native_api.get_universal_status(
            self.device_handle, max_wait_in_milliseconds)
        return TLMCUniversalStatus(ret)

    def get_universal_status_bits(self, max_wait_in_milliseconds: int):
        """
        Returns the status bits generic to all devices.
        """
        self.native_api.get_universal_status_bits(
            self.device_handle, max_wait_in_milliseconds)

    def get_velocity_params(self, max_wait_in_milliseconds: int):
        """
        Returns the velocity parameters being used by the motor. Includes min_velocity, max_velocity, and acceleration.
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
        self.native_api.move_continous(self.device_handle, max_wait_in_milliseconds)

    def move_jog(self, direction: TLMC_MoveDirection, max_wait_in_milliseconds: int):
        """
        Initiates a jog move. Uses settings changed in set_move_jog_params().
        """
        self.native_api.move_jog(self.device_handle, direction, max_wait_in_milliseconds)

    def move_relative(self,move_mode: TLMC_MoveModes,  step_size: int, max_wait_in_milliseconds: int):
        """
        Initiates a relative move with the specified step size.
        """
        self.native_api.move_relative(self.device_handle, step_size, max_wait_in_milliseconds)

    def rack_identify(self, channel: int):
        """
        Identify command, should cause the LED's on the device to flash.
        """
        self.native_api.rack_identify(self.device_handle, channel)

    def set_bow_index(self, new_bow_index: TLMC_BowIndex):
        """
        Sets the bow index for the motor. 
        """
        self.native_api.set_bow_index(self.device_handle, new_bow_index)

    def set_connected_product(self, product_name: str):
        """
        Sets the designated actutor to a channel or device object. 
        """
        self.native_api.set_connected_product(self.device_handle, product_name)

    def set_connected_product_info(self, product_name: str, axis_type: TLMC_ConnectedProductAxisType, 
                                   movement_type: TLMC_ConnectedProductMovementType,
                                   unit_type: TLMC_Unit, distance_scale_factor: int, 
                                   velocity_scale_factor: int, acceleration_scale_factor: int, 
                                   min_position: int, max_position: int,
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

    def set_general_move_params(self, backlash_distance: int):
        """
        Changes the backlash distance used by the actuator. 
        """
        self.native_api.set_general_move_params(
            self.device_handle, backlash_distance)

    def set_home_params(self,direction: TLMC_MoveDirection, limit_switch: TLMC_HomeLimitSwitches, velocity: int, offset_distance: int):
        """
        Changes the max velocity and home offset used by home().
        """
        self.native_api.set_home_params(
            self.device_handle, direction, limit_switch, velocity, offset_distance)

    def set_limit_switch_params(self, clockwise_limit_mode: TLMC_HardLimitOperatingModes, 
                                counter_clockwise_mode: TLMC_HardLimitOperatingModes,
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

    def set_move_jog_params(self, step_size: int, min_velocity: int, max_velocity: int, acceleration: int):
        """
        Changes the step size, min velocity, max velocity, and acceleration settings used by move_jog().
        """
        self.native_api.set_move_jog_params(
            self.device_handle, step_size, min_velocity, max_velocity, acceleration)

    def set_move_relative_params(self, move_relative_distance: int):
        """
        Changes the step size used by move_relative_by_programmed_position().
        """
        self.native_api.set_move_relative_params(
            self.device_handle, move_relative_distance)

    def set_position_counter(self, new_position_counter: int):
        """
        Sets a new position counter. 
        """
        self.native_api.set_position_counter(
            self.device_handle, new_position_counter)

    def set_power_params(self, rest_factor: int, move_factor: int):
        """
        Sets the move and rest factor for the motor. 
        """
        self.native_api.set_power_params(
            self.device_handle, rest_factor, move_factor)

    def set_stepper_loop_params(self, loop_mode: TLMC_StepperLoopParams_LoopMode, proportional: int,
                                integral: int, differential: int, output_clip: int, output_tolerance: int,
                                microsteps_per_ecount: int):
        """
        Changes the position loop settings. 
        """
        self.native_api(self.device_handle, loop_mode, proportional, integral,
                        differential, output_clip, output_tolerance,
                        microsteps_per_ecount)

    def set_trigger_params_for_stepper(self, trigger_mode: TLMC_TriggerModesForStepper):
        """
        CHanges the trigger settings being used by the channel.
        """
        self.native_api.set_trigger_params_for_stepper(
            self.device_handle, trigger_mode)

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
