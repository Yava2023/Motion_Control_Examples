from xa_sdk.shared.xa_shared_types import XADevice
from xa_sdk.shared.xa_shared_types import *
from xa_sdk.native_sdks.xa_sdk import XASDK

class BPC30X(XADevice):
    """
    Thorlabs benchtop piezo motor controller.
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
        cls = BPC30X
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
    
    def set_setting(self, pSettings_name):
        super().set_setting(pSettings_name)

    def set_settings_from_string(self, pSettings_name):
        return super().set_settings_from_string(pSettings_name)

    def set_end_of_message_mode(self, mode):
        super().set_end_of_message_mode(mode)


    # Methods unique to motor types (moves and settings parameters)
    def __init__(self, handle, connection_type, operating_mode):
        super().__init__()
        self.native_api = XASDK()
        self.device_handle = handle
        device = self.native_api.open(handle, connection_type, operating_mode)
        if device.value > 0:
            self.device_handle = device

    def get_digital_output_params(self, max_wait_in_milliseconds: int):
        """
        Returns the output state of the digital output pins. 
        """
        self.native_api.get_digital_output_params(
            self.device_handle, max_wait_in_milliseconds)

    def rack_identify(self, channel: int):
        """
        Causes the LED's on the controller to flash to signal a connection.
        """
        self.native_api.rack_identify(self.device_handle, channel)

    def set_digital_ouput_params(self, new_ouput_state: TLMC_DigitalOutput):
        """
        Sets the output state of the digital output pins. 
        Triggering might need to be disabled for this to be used. 
        """
        self.native_api.set_digital_output_params(
            self.device_handle, new_ouput_state)
