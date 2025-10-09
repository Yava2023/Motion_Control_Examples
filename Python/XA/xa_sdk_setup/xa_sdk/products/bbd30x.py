from xa_sdk.shared.xa_shared_types import XADevice
from xa_sdk.shared.xa_shared_types import *
from xa_sdk.native_sdks.xa_sdk import XASDK

class BBD30X(XADevice):
    """
    Thorlabs brushless benchtop DC servo mootor controller.
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

    # Methods generic to every device.
    def add_user_message_to_log(self, user_message):
        return super().add_user_message_to_log(user_message)

    def close(self):
        super().close()

    def disconnect(self):
        super().disconnect()

    def get_device_info(self, max_wait_in_milliseconds):
        return super().get_device_info(max_wait_in_milliseconds)

    def get_hardware_info(self, wait_in_milliseconds: int):
        return super().get_hardware_info(wait_in_milliseconds)

    def get_method_list(self):
        cls = BBD30X
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
        return super().identify()
    
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

    def get_analog_monitor_configuration_params(self, max_wait_in_milliseconds: int):
        """
        Returns the analog monitor settings structure. 
        """
        ret = self.native_api.get_analog_monitor_configuration_params(
            self.device_handle, max_wait_in_milliseconds)
        return AnalogMonitorConfigurationParams(ret)

    def get_aux_io_port_mode(self, port_number: int, max_wait_in_milliseconds: int):
        """
        Returns the aux IO port mode. 
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

    def get_digital_output_params(self, max_wait_in_milliseconds: int):
        """
        Returns the digital output settings structure for the motor. 
        """
        self.native_api.get_digital_output_params(
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
        Returns the IO settings structure.
        """
        ret = self.native_api.get_io_configuration_params(
            self.device_handle, port_number, max_wait_in_milliseconds)
        return IoConfigurationParams(ret)

    def get_lcd_display_params(self, max_wait_in_milliseconds: int):
        """
        Returns the LCD display settings structure. 
        """
        ret = self.native_api.get_lcd_display_params(
            self.device_handle, max_wait_in_milliseconds)
        return LcdDisplayParams(ret)

    def set_analog_monitor_configuration_params(self, monitor_number: int, max_wait_in_milliseconds: int):
        """
        Changes the current monitor settings. 
        """
        self.native_api.set_analog_monitor_configuration_params(
            self.device_handle, monitor_number, max_wait_in_milliseconds)

    def set_aux_io_port_mode(self, port_number: int, new_mode: TLMC_AuxIoPortMode):
        """
        Changes the aux IO port mode. 
        """
        self.native_api.set_aux_io_port_mode(
            self.device_handle, port_number, new_mode)

    def set_aux_io_software_states(self, new_state: int):
        """
        Changes the aux IO software state. 
        """
        self.native_api.set_aux_io_software_states(
            self.device_handle, new_state)

    def set_digital_ouput_params(self, new_ouput_state: TLMC_DigitalOutput):
        """
        Chages the digital output settings used by the motor.
        """
        self.native_api.set_digital_output_params(
            self.device_handle, new_ouput_state)

    def set_io_configuration_params(self, port_number: int, mode: TLMC_IoPortMode, trigger_out_source: TLMC_IoPortSource):
        """
        Changes the IO port settings.
        """
        self.native_api.set_io_configuration_params(
            self.device_handle, port_number, mode, trigger_out_source)

    def set_lcd_display_params(self, knob_sensitivity: int, display_brightness: int, display_timeout: int,
                               display_dim_level: int):
        """
        Changes the LCD display settings.
        """
        self.native_api.set_lcd_display_params(self.device_handle, knob_sensitivity, display_brightness, display_timeout,
                                               display_dim_level)

    def rack_identify(self, channel: int):
        """
        Identify feature, should cause the status LED's to flash. 
        """
        self.native_api.rack_identify(self.device_handle, channel)
