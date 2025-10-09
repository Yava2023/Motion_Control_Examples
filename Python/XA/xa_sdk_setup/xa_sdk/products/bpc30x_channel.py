from xa_sdk.native_sdks.xa_sdk import XASDK
from xa_sdk.shared.xa_shared_types import *
from xa_sdk.shared.xa_shared_types import XADevice

class BPC30XCHANNEL(XADevice):
    """
    Thorlabs benchtop piezo controller channel.
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

    # Mehtods generic to each device.
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
        cls = BPC30XCHANNEL
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


    # Methods unique to motor types (moves and settings parameters)
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
    
    def convert_from_physical_to_device(self, TLMC_scale_type: TLMC_ScaleType, TLMC_unit_type: TLMC_Unit, physical_value: float):
        """
        Converts physical unit input into device units. Arguments used are the scaleType, the unitType,
        and the user physicalValue.
        and the unitType 
        """
        ret = self.native_api.convert_from_physical_to_device(
            self.device_handle, TLMC_scale_type, TLMC_unit_type, physical_value)

        return ret
    
    def get_aux_io_port_mode(self, port_number: int, max_wait_in_milliseconds: int):
        """
        Returns the aux IO port mode being used. 
        """
        ret = self.native_api.get_aux_io_port_mode(
            self.device_handle, port_number, max_wait_in_milliseconds)
        return ret

    def get_aux_io_software_states(self, max_wait_in_milliseconds: int):
        """
        Returns the aux IO software state.
        """
        ret = self.native_api.get_aux_io_software_states(
            self.device_handle, max_wait_in_milliseconds)
        return ret

    def get_enable_state(self, max_wait_in_milliseconds: int):
        """
        Returns the enable state of the cntroller channel. 
        """
        self.native_api.get_enable_state(
            self.device_handle, max_wait_in_milliseconds)

    def get_io_configuration_number_of_ports_supported(self):
        """
        Returns the number of IO ports available. 
        """
        ret = self.native_api.get_io_configuration_number_of_ports_supported(
            self.device_handle)
        return ret

    def get_io_configuration_params(self, port_number: int, max_wait_in_milliseconds: int):
        """
        Returns the IO port settings structure.
        """
        ret = self.native_api.get_io_configuration_params(
            self.device_handle, port_number, max_wait_in_milliseconds)
        return IoConfigurationParams(ret)

    def get_io_position_trigger_enable_state(self, max_wait_in_milliseconds: int):
        """
        Returns the positions trigger enable state.
        """
        ret = self.native_api.get_io_position_trigger_enable_state(
            self.device_handle, max_wait_in_milliseconds)
        return ret

    def get_io_trigger_params(self, max_wait_in_milliseconds: int):
        """
        Rturns the IO trigger settings. 
        """
        ret = self.native_api.get_io_trigger_params(
            self.device_handle, max_wait_in_milliseconds)
        return IoTriggerParams(ret)

    def get_max_output_voltage_params(self, max_wait_in_milliseconds: int):
        """
        Returns the max output voltage.
        """
        ret = self.native_api.pz_get_max_output_voltage_params(
            self.handle, max_wait_in_milliseconds)
        return PZ_MaxOutputVoltageParams(ret)

    def get_max_travel(self, max_wait_in_milliseconds: int):
        """
        Returns the max travel range of the motor. 
        """
        ret = self.native_api.pz_get_max_travel(
            self.device_handle, max_wait_in_milliseconds)
        return ret

    def get_output_voltage(self, max_wait_in_milliseconds: int):
        """
        Returns the current output voltage. 
        """
        ret = self.native_api.pz_get_output_voltage(
            self.device_handle, max_wait_in_milliseconds)
        return ret

    def get_output_voltage_control_source_params(self, max_wait_in_milliseconds: int):
        """
        Returns the output voltage source. 
        """
        ret = self.native_api.pz_get_ouput_voltage_control_source_params(
            self.device_handle, max_wait_in_milliseconds)
        return PZ_OutputVoltageControlSourceParams(ret)

    def get_ouput_waveform_params(self, max_wait_in_milliseconds: int):
        """
        Returns the output waveform settings structure. 
        """
        ret = self.native_api.pz_get_ouput_waveform_params(
            self.device_handle, max_wait_in_milliseconds)
        return PZ_OutputWaveformParams(ret)

    def get_position_control_mode(self, max_wait_in_milliseconds: int):
        """
        Returns the position control mode. 
        """
        ret = self.native_api.pz_get_position_control_mode(
            self.device_handle, max_wait_in_milliseconds)
        return ret
    
    def get_position_loop_params(self, max_wait_in_milliseconds: int):
        """
        Returns the position loop settings structure.
        """
        ret = self.native_api.pz_get_position_loop_params(
            self.device_handle, max_wait_in_milliseconds)
        return PZ_PositionLoopParams(ret)

    def get_slew_rate_params(self, max_wait_in_milliseconds: int):
        """
        Returns the slew rate settings structure. 
        """
        ret = self.native_api.pz_get_slew_rate_params(
            self.device_handle, max_wait_in_milliseconds)
        return PZ_SlewRateParams(ret)

    def get_status(self, max_wait_in_milliseconds: int):
        """
        Returns the current status on the device.
        """
        ret = self.native_api.pz_get_status(
            self.device_handle, max_wait_in_milliseconds)
        return ret

    def get_status_bits(self, max_wait_milliseconds: int):
        """
        Returns the status bits. 
        """
        ret = self.native_api.pz_get_status_bits(
            self.device_handle, max_wait_milliseconds)
        return ret

    def get_status_item(self, status_item_id: TLMC_StatusItemIds, status_item: TLMC_StatusItem):
        """
        Returns a single state status item. 
        """
        ret = self.native_api.get_status_item(self.device_handle, status_item_id, status_item)
        return ret
    
    def get_status_item_count(self):
        """
        Returns the number of available status items. 
        """
        ret = self.native_api.get_status_item_count(self.device_handle)
        return ret

    def get_status_items(self, start_index: int, number_of_items: int, number_of_items_copied: int):
        """
        Returns all of the available status items. 
        """
        ret = self.native_api.get_status_items(self, start_index, number_of_items, number_of_items_copied)
        return ret

    def restore_to_factory_defaults(self):
        """
        Sets the stage back to it's default settings.
        """
        self.native_api.restore_to_factory_defaults(self.device_handle)

    def set_aux_io_software_states(self, new_state: int):
        """
        Changes the aux io software state.
        """
        self.native_api.set_aux_io_software_states(
            self.device_handle, new_state)

    def set_enable_state(self, enable_state: TLMC_EnableState):
        """
        Enables the motor channel. 
        """
        self.native_api.set_enable_state(self.device_handle, enable_state)

    def set_io_configuration_params(self, port_number: TLMC_IoPortNumber, mode: TLMC_IoPortMode, trigger_out_source: TLMC_IoPortSource):
        """
        Changs the IO port settings.
        """
        self.native_api.set_io_configuration_params(
            self.device_handle, port_number, mode, trigger_out_source)

    def set_io_position_trigger_enable_state(self, new_enable_state: TLMC_IoPositionTriggerEnableState, 
                                             max_wait_in_milliseconds: int):
        """
        Changes the IO position trigger enable state. 
        """
        self.native_api.set_io_position_trigger_enable_state(
            self.device_handle, new_enable_state, max_wait_in_milliseconds)

    def set_io_trigger_params(self,  trigger_in_mode: TLMC_IoTriggerInMode, trigger_in_polarity: TLMC_IoTriggerPolarity,
                              trigger_in_source: TLMC_IoTriggerInSource, trigger_out_mode: TLMC_IoTriggerOutMode, 
                              trigger_out_polarity: TLMC_IoTriggerPolarity,
                              trigger_out_forward_start_position: int, trigger_out_forward_interval: int,
                              trigger_out_forward_number_of_pulses: int, trigger_out_reverse_start_position: int,
                              trigger_out_reverse_interval: int, trigger_out_reverse_number_of_pulses: int,
                              trigger_out_pulse_width: int, trigger_out_number_of_cycles: int):
        """
        Changes the IO trigger settings.
        """
        self.native_api.set_io_trigger_params(self.device_handle,  trigger_in_mode, trigger_in_polarity,
                                              trigger_in_source, trigger_out_mode, trigger_out_polarity,
                                              trigger_out_forward_start_position, trigger_out_forward_interval,
                                              trigger_out_forward_number_of_pulses, trigger_out_reverse_start_position,
                                              trigger_out_reverse_interval, trigger_out_reverse_number_of_pulses,
                                              trigger_out_pulse_width, trigger_out_number_of_cycles)

    def set_max_output_voltage(self, max_output_voltage: int):
        """
        Changes the max output voltage. 
        """
        self.native_api.pz_set_max_output_voltage(
            self.device_handle, max_output_voltage)

    def set_output_voltage(self, new_output_voltage: int):
        """
        Changes the output voltage.
        """
        self.native_api.pz_set_output_voltage(
            self.device_handle, new_output_voltage)
        
    def set_output_voltage_source_params(self, voltage_source: TLMC_PZ_OutputVoltageControlSource):
        """
        Changes the output source settings. 
        """
        self.native_api.pz_set_ouput_voltage_source_params(
            self.device_handle, voltage_source)

    def set_output_waveform_lookup_table_sample(self, index: int, voltage: int):
        """
        Changes the output waveform look up table used. 
        """
        self.native_api.pz_set_output_waveform_lookup_table_sample(
            self.device_handle, index, voltage)

    def set_output_waveform_params(self, mode: TLMC_PZ_OutputWaveformOperartingMode, 
                                   num_of_samples_per_cycle: int,
                                   num_of_cycles: int, sample_delay: int, pre_cycle_delay: int,
                                   post_cycle_delay: int, output_trigger_start_index: int,
                                   output_trigger_width: int, num_of_samples_between_triggers: int):
        """
        Changes the output waveform settings being used. 
        """
        self.native_api.pz_set_ouput_waveform_params(self, mode, num_of_samples_per_cycle,
                                                     num_of_cycles, sample_delay, pre_cycle_delay,
                                                     post_cycle_delay, output_trigger_start_index,
                                                     output_trigger_width, num_of_samples_between_triggers)

    def start_output_waveform(self):
        """
        Initiates the designated waveform.
        """
        self.native_api.pz_start_output_waveform(self.device_handle)

    def stop_output_waveform(self):
        """
        Cancels the output waveform. 
        """
        self.native_api.pz_stop_output_waveform(self.device_handle)

    def set_position(self, new_position: int):
        """
        Changes the current position. Controller needs to be in closed loop mode. 
        """
        self.native_api.pz_set_position(self.device_handle, new_position)

    def set_position_control_mode(self, new_control_mode: TLMC_PZ_PositionControlMode):
        """
        Changes the current controle mode. (Open vs closed loop)
        """
        self.native_api.pz_set_position_control_mode(
            self.device_handle, new_control_mode)

    def set_position_loop_params(self, proportional: int, integral: int):
        """
        Changes the position loop settings. 
        """
        self.native_api.pz_set_position_loop_params(
            self.device_handle, proportional, integral)

    def set_slew_rate_params(self, open_slew_rate: int, closed_slew_rate: int):
        """
        Changes the slew rate settings. 
        """
        self.native_api.pz_set_slew_rate_params(
            self, open_slew_rate, closed_slew_rate)

    def set_zero(self, max_wait_in_milliseconds):
        """
        Zero the controller channel. 
        """
        self.native_api.pz_set_zero(self.device_handle, max_wait_in_milliseconds)
