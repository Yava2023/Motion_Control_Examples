from abc import ABCMeta, abstractmethod
# Interface to describe the functions needed in the SDK


class NativeSDKInterface(metaclass=ABCMeta):

    def __init__(self):
        pass

    @abstractmethod
    def add_user_message_to_log(self, user_message):
        pass

    @abstractmethod
    def close(self, handle):
        pass

    @abstractmethod
    def convert_from_device_units_to_physical(self, handle, TLMC_scale_type, device_value):
        pass

    @abstractmethod
    def convert_from_physical_to_device(self, handle, TLMC_scale_type, TLMC_unit_type, physical_value):
        pass

    @abstractmethod
    def create_simulation(self, pDescription):
        pass

    @abstractmethod
    def disconnect(self, handle):
        pass

    @abstractmethod
    def get_adc_inputs(self, handle, max_wait_in_milliseconds):
        pass

    @abstractmethod
    def get_analog_monitor_configuration_params(self, handle, monitor_number, max_wait_in_milliseconds):
        pass

    @abstractmethod
    def get_api_version(self):
        pass

    @abstractmethod
    def get_aux_io_port_mode(self, handle, port_number, max_wait_in_milliseconds):
        pass

    @abstractmethod
    def get_aux_io_software_states(self, handle, max_wait_in_milliseconds):
        pass

    @abstractmethod
    def get_bow_index(self, handle, index_val, max_wait_in_milliseconds):
        pass

    @abstractmethod
    def get_connected_product(self, handle):
        pass

    @abstractmethod
    def get_connected_product_info(self, handle):
        pass

    @abstractmethod
    def get_connected_products_supported(self, handle):
        pass

    @abstractmethod
    def get_current_loop_params(self, handle, loop_scenario, max_wait_in_milliseconds):
        pass

    @abstractmethod
    def get_dc_pid_params(self, handle, max_wait_in_milliseconds):
        pass

    @abstractmethod
    def get_device_info(self, handle, max_wait_in_milliseconds):
        pass

    @abstractmethod
    def get_device_list_item_count(self):
        pass

    @abstractmethod
    def get_device_list_items(self, source_start_index, number_of_items, pNumber_of_items_copied):
        pass

    @abstractmethod
    def get_digital_input_states(self, handle, max_wait_in_milliseconds):
        pass

    @abstractmethod
    def get_digital_output_params(self, handle, max_wait_in_milliseconds):
        pass

    @abstractmethod
    def get_enable_state(self, handle, max_wait_in_milliseconds):
        pass

    @abstractmethod
    def get_encoder_counter(self, handle, max_wait_in_milliseconds):
        pass

    @abstractmethod
    def get_general_move_params(self, handle, general_move_params,
                                max_wait_in_milliseconds):
        pass

    @abstractmethod
    def get_hardware_info(self, handle, max_wait_in_milliseconds):
        pass

    @abstractmethod
    def get_home_params(self, handle, max_wait_in_milliseconds):
        pass

    @abstractmethod
    def get_io_configuration_number_of_ports_supported(self, handle):
        pass

    @abstractmethod
    def get_io_configuration_params(self, handle, port_number, max_wait_in_milliseconds):
        pass

    @abstractmethod
    def get_io_position_trigger_enable_state(self, handle, max_wait_in_milliseconds):
        pass

    @abstractmethod
    def get_io_trigger_params(self, handle, max_wait_in_milliseconds):
        pass

    @abstractmethod
    def get_joystick_params(self, handle, max_wait_in_milliseconds):
        pass

    @abstractmethod
    def get_kcube_io_trigger_params(self, handle, max_wait_in_milliseconds):
        pass

    @abstractmethod
    def get_kcube_mmi_lock_state(self, handle, max_wait_in_milliseconds):
        pass

    @abstractmethod
    def get_kcube_mmi_params(self, handle, max_wait_in_milliseconds):
        pass

    @abstractmethod
    def get_kcube_position_trigger_params(self, handle, max_wait_in_milliseconds):
        pass

    @abstractmethod
    def get_lcd_display_params(self, handle, max_wait_in_milliseconds):
        pass

    @abstractmethod
    def get_lcd_move_params(self, handle, max_wait_in_milliseconds):
        pass

    @abstractmethod
    def get_limit_switch_params(self, handle, max_wait_in_milliseconds):
        pass

    @abstractmethod
    def get_motor_output_params(self, handle, max_wait_in_milliseconds):
        pass

    @abstractmethod
    def get_move_absolute_params(self, absolute_params, max_wait_in_milliseconds):
        pass

    @abstractmethod
    def get_move_jog_params(self, jog_params, max_wait_in_milliseconds):
        pass

    @abstractmethod
    def get_move_relative_params(self, handle, move_relative_params, max_wait_in_millisecond):
        pass

    @abstractmethod
    def get_position_counter(self, handle, max_wait_in_milliseconds):
        pass

    @abstractmethod
    def get_position_loop_params(self, handle, position_loop_scenario, max_wait_in_milliseconds):
        pass

    @abstractmethod
    def get_power_params(self, handle, max_wait_in_milliseconds):
        pass

    @abstractmethod
    def get_profiled_mode_params(self, handle, max_wait_in_milliseconds):
        pass

    @abstractmethod
    def get_rack_bay_occupied_state(self, handle, bay_number, occupied_state, max_wait_in_milliseconds):
        pass

    @abstractmethod
    def get_rich_response(self, handle):
        pass

    @abstractmethod
    def get_setting(self, handle, pSettings_name, max_wait_in_milliseconds):
        pass

    @abstractmethod
    def get_setting_count(self, handle):
        pass

    @abstractmethod
    def get_setting_discrete_values(self, handle, pSettings_name, pBuffer, buffer_length, result_length):
        pass

    @abstractmethod
    def get_settings(self, handle, source_start_index, number_of_items, pNumber_of_items_copied):
        pass

    @abstractmethod
    def get_settings_as_string(self, handle, pBuffer, buffer_length, pResult_length, TLMC_setting_string_format, include_read_only_items):
        pass

    @abstractmethod
    def get_status_item(self, handle, status_item_id):
        pass

    @abstractmethod
    def get_status_item_count(self, handle):
        pass

    @abstractmethod
    def get_status_items(self, handle, start_index, number_of_items,
                         pNumber_of_items_copies):
        pass

    @abstractmethod
    def get_stage_axis_params(self, handle, max_wait_in_milliseconds):
        pass

    @abstractmethod
    def get_stepper_loop_params(self, handle, max_wait_in_milliseconds):
        pass

    @abstractmethod
    def get_stepper_status(self, handle, max_wait_in_milliseconds):
        pass

    @abstractmethod
    def get_track_settle_params(self, handle, max_wait_in_milliseconds):
        pass

    @abstractmethod
    def get_trigger_params_for_dc_brushless(self, handle, max_wait_in_milliseconds):
        pass

    @abstractmethod
    def get_trigger_params_for_stepper(self, handle, max_wait_in_milliseconds):
        pass

    @abstractmethod
    def get_universal_status(self, handle, max_wait_in_milliseconds):
        pass

    @abstractmethod
    def get_universal_status_bits(self, handle, max_wait_in_milliseconds):
        pass

    @abstractmethod
    def get_velocity_params(self, handle, velocity_params, max_wait_in_milliseconds):
        pass

    @abstractmethod
    def home(self, max_wait_in_milliseconds):
        pass

    @abstractmethod
    def identify(self):
        pass

    @abstractmethod
    def move_absolute(self, handle, move_mode, position, max_wait_in_milliseconds):
        pass

    @abstractmethod
    def move_continuous(self, handle, direction, max_wait_in_milliseconds):
        pass

    @abstractmethod
    def move_jog(self, handle, direction, max_wait_in_milliseconds):
        pass

    @abstractmethod
    def move_relative(self, handle, move_mode, distance, max_wait_in_milliseconds):
        pass
    
    @abstractmethod
    def open(self, handle, transport_type, operating_mode):
        pass

    @abstractmethod
    def persist_params(self, handle, parameter_group_id):
        pass

    @abstractmethod
    def pz_get_max_output_voltage_params(self, handle, max_wait_in_milliseconds):
        pass

    @abstractmethod
    def pz_get_max_travel(self, handle, max_wait_in_milliseconds):
        pass

    @abstractmethod
    def pz_get_output_voltage(self, handle, max_wait_in_milliseconds):
        pass

    @abstractmethod
    def pz_get_output_voltage_control_source_params(self, handle, max_wait_in_milliseconds):
        pass

    @abstractmethod
    def pz_get_output_waveform_params(self, handle, max_wait_in_millisecconds):
        pass

    @abstractmethod
    def pz_get_position(self, handle, position, max_wait_in_milliseconds):
        pass

    @abstractmethod
    def pz_get_position_control_mode(self, handle, control_mode, max_wait_in_milliseconds):
        pass

    @abstractmethod
    def pz_get_position_loop_params(self, handle, max_wait_in_milliseconds):
        pass

    @abstractmethod
    def pz_get_slew_rate_params(self, handle, slew_rate_params, max_wait_in_milliseconds):
        pass

    @abstractmethod
    def pz_get_status(self, handle, max_wait_in_milliseconds):
        pass

    @abstractmethod
    def pz_get_status_bits(self, handle, max_wai_milliseconds):
        pass

    @abstractmethod
    def pz_set_max_output_voltage(self, handle, max_output_voltage):
        pass

    @abstractmethod
    def pz_set_output_voltage(self, handle, new_output_voltage):
        pass
    
    @abstractmethod
    def pz_set_output_voltage_control_source_params(self, handle, voltage_source):
        pass

    @abstractmethod
    def pz_set_output_waveform_lookup_table_sample(self, handle, index, voltage):
        pass

    @abstractmethod
    def pz_set_output_waveform_params(self, handle, mode, num_of_samples_per_cycle,
                                      num_of_cycles, sample_delay, pre_cycle_delay,
                                      post_cycle_delay, output_trigger_start_index,
                                      output_trigger_width, num_of_samples_between_triggers):
        pass

    @abstractmethod
    def pz_set_position(self, handle, new_position):
        pass

    @abstractmethod
    def pz_set_position_control_mode(self, handle, new_control_mode):
        pass

    @abstractmethod
    def pz_set_position_loop_params(self, handle, proportional, integral):
        pass

    @abstractmethod
    def pz_set_slew_rate_params(self, handle, open_slew_rate, closed_slew_rate):
        pass

    @abstractmethod
    def pz_set_zero(self, handle, max_wait_in_milliseconds):
        pass

    @abstractmethod
    def pz_start_output_waveform(self, handle):
        pass

    @abstractmethod
    def pz_stop_output_waveform(self, handle):
        pass

    @abstractmethod
    def rack_identify(self, handle, channel):
        pass

    @abstractmethod
    def remove_simulation(self, pDescription):
        pass

    @abstractmethod
    def restore_to_factory_defaults(self, handle):
        pass

    @abstractmethod
    def set_analog_monitor_configuration_params(self, handle, monitor_number, motor_channel, system_variable, scale, offset):
        pass

    @abstractmethod
    def set_aux_io_port_mode(self, handle, port_number, new_mode):
        pass

    @abstractmethod
    def set_aux_io_software_states(self, handle, new_state):
        pass

    @abstractmethod
    def set_bow_index(self, handle, new_bow_index):
        pass

    @abstractmethod
    def set_connected_product(self, handle, product_name):
        pass

    @abstractmethod
    def set_connected_product_info(self, handle, product_name, axis_type, movement_type, unit_type,
                                   distance_scale_factor, velocity_scale_factor,
                                   acceleration_scale_factor, min_position, max_position,
                                   max_velocity, max_acceleration):
        pass

    @abstractmethod
    def set_current_loop_params(self, handle, loop_scenario, phase, proportional, integral,
                                integral_limit, integral_dead_band, feed_fwrd):
        pass

    @abstractmethod
    def set_dc_pid_params(self, handle, proportional, integral, derivative, integral_limit, filter_control):
        pass

    @abstractmethod
    def set_digital_output_params(self, handle, new_output_state):
        pass

    @abstractmethod
    def set_enable_state(self, handle, enable_state):
        pass

    @abstractmethod
    def set_encoder_counter(self, handle, new_encoder_counter):
        pass

    @abstractmethod
    def set_end_of_message_mode(self, handle, mode):
        pass

    @abstractmethod
    def set_general_move_params(self, handle, backlash_distance):
        pass

    @abstractmethod
    def set_home_params(self, handle, direction, limit_switch, velocity, offset_distance):
        pass

    @abstractmethod
    def set_io_configuration_params(self, handle, port_number, mode, trigger_out_source):
        pass

    @abstractmethod
    def set_io_position_trigger_enable_state(self, handle, new_enable_state, max_wait_in_milliseconds):
        pass

    @abstractmethod
    def set_io_trigger_params(self, handle, trigger_in_mode, trigger_in_polarity,
                              trigger_in_source, trigger_out_mode, trigger_out_polarity,
                              trigger_out_forward_start_position, trigger_out_forward_interval,
                              trigger_out_forward_number_of_pulses, trigger_out_reverse_start_position,
                              trigger_out_reverse_interval, trigger_out_reverse_number_of_pulses,
                              trigger_out_pulse_width, trigger_out_number_of_cycles):
        pass

    @abstractmethod
    def set_joystick_params(self, handle, low_gear_velocity, high_gear_velocity, low_gear_acceleration, high_gear_acceleration, direction_sense):
        pass

    @abstractmethod
    def set_kcube_io_trigger_params(self, handle, trigger_one_mode, trigger_one_polarity,
                                    trigger_two_mode, trigger_two_polarity):
        pass

    @abstractmethod
    def set_kcube_mmi_lock_state(self, handle, lock_state):
        pass

    @abstractmethod
    def set_kcube_mmi_params(self, handle, joystick_mode, joystick_velocity, joystick_acceleration,
                             joystick_direction_sense, position_one, position_two,
                             display_brightness, display_timeout, display_dim_level,
                             position_three, joystick_sensitivity):
        pass

    @abstractmethod
    def set_kcube_position_trigger_params(self, handle, fwrd_start_position, fwrd_interval,
                                          fwrd_number_of_pulses, rev_start_position,
                                          rev_interval, rev_number_of_pulses, pulse_width,
                                          number_of_cycles):
        pass

    @abstractmethod
    def set_lcd_display_params(self, handle, knob_sensitivity, display_brightness, display_timeout,
                               display_dim_level):
        pass

    @abstractmethod
    def set_lcd_move_params(self, handle, knob_mode, jog_step_size, acceleration,
                            max_velocity, jog_stop_mode, preset_position):
        pass

    @abstractmethod
    def set_limit_switch_params(self, handle, clockwise_limit_mode, counter_clockwise_limit_mode,
                                clockwise_soft_limit, counter_clockwise_soft_limit, soft_limit_operating_mode):
        pass

    @abstractmethod
    def set_motor_output_params(self, handle, current_limit, energy_limit, motor_limit, motor_bias):
        pass

    @abstractmethod
    def set_move_absolute_params(self, absolute_distance):
        pass

    @abstractmethod
    def set_move_jog_params(self, handle, jog_mode, step_size, min_velcoity, max_velocity, acceleration, stop_mode, direction_sense):
        pass

    @abstractmethod
    def set_move_relative_params(self, handle, move_relative_distance):
        pass

    @abstractmethod
    def set_position_counter(self, handle, new_position_counter):
        pass

    @abstractmethod
    def set_position_loop_params(self, handle, position_loop_scenario, proportional, integral, integral_limit,
                                 derivative, servo_cycles, scale, velocity_feed_fwrd,
                                 acceleration_feed_fwrd, error_limit):
        pass

    @abstractmethod
    def set_power_params(self, handle, rest_factor, move_factor):
        pass

    @abstractmethod
    def set_profiled_mode_params(self, handle, mode, jerk):
        pass

    @abstractmethod
    def set_setting(self, handle, pSettings_name):
        pass

    @abstractmethod
    def set_settings_from_string(self, handle, pSettings_name):
        pass

    @abstractmethod
    def set_stage_axis_params(self, handle, type_id, axis_id, part_number, serial_number,
                              counts_per_unit, min_position, max_position,
                              max_acceleration, max_decceleration, max_velcoity,
                              gear_box_ratio):
        pass

    @abstractmethod
    def set_status_mode(self, handle, operating_mode):
        pass

    @abstractmethod
    def set_stepper_loop_params(self, handle, loop_mode, proportional, integral,
                                differential, output_clip, output_tolerance,
                                microsteps_per_ecount):
        pass

    @abstractmethod
    def set_track_settle_params(self, handle, settle_time, settle_window, track_window):
        pass

    @abstractmethod
    def set_trigger_params_for_for_dc_brushless(self, handle, mode):
        pass

    @abstractmethod
    def set_trigger_params_for_stepper(self, handle, trigger_mode):
        pass

    @abstractmethod
    def set_velocity_params(self, min_velocity, max_velocity, acceleration):
        pass

    @abstractmethod
    def shutdown(self):
        pass

    @abstractmethod
    def startup(self, pSettings_file_name):
        pass

    @abstractmethod
    def stop(self, handle, stop_mode, max_wait_in_milliseconds):
        pass

    @abstractmethod
    def try_load_library(self, current_path):
        pass
