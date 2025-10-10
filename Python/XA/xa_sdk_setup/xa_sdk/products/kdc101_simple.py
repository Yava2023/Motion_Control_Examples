"""
Simplified KDC101 Motor Controller Wrapper

This provides an intuitive interface for common motor control operations
without exposing all the low-level details.
"""

from __future__ import annotations
from typing import Optional
from xa_sdk.products.base import XADevice
from xa_sdk.native_sdks.xa_sdk import XASDK
from xa_sdk.shared.tlmc_type_structures import (
    TLMC_OperatingModes,
    TLMC_EnableStates,
    TLMC_MoveDirection,
    TLMC_ScaleType,
    TLMC_Unit,
)


class SimpleKDC101:
    """
    Simplified wrapper for KDC101 brushed DC motor controller.

    Example usage:
        # Initialize SDK once (required before first use)
        SimpleKDC101.initialize_sdk()

        # Connect to device
        motor = SimpleKDC101("27007297")

        # Basic setup
        motor.enable()
        motor.home()

        # Move to positions (device units)
        motor.move_to(10000)
        motor.move_by(5000)

        # Or use physical units (mm, degrees, etc.)
        motor.move_to_mm(5.0)
        pos_mm = motor.get_position_mm()

        # Query state
        pos = motor.get_position()
        print(f"Current position: {pos}")

        # Cleanup
        motor.disable()
        motor.close()

        # Shutdown SDK when done with all devices
        SimpleKDC101.shutdown_sdk()
    """

    _sdk_initialized = False

    @classmethod
    def initialize_sdk(
            cls,
            dll_path: Optional[str] = None,
            settings_file: Optional[str] = None
    ):
        """
        Initialize the XA SDK. Must be called once before creating any devices.

        Args:
            dll_path: Path to directory containing tlmc_xa_native.dll.
                     If None, uses current directory.
            settings_file: Path to settings file. If None, uses default.
        """
        if cls._sdk_initialized:
            return

        if dll_path is None:
            import os
            dll_path = os.getcwd()

        XASDK.try_load_library(dll_path)
        XASDK.startup(settings_file or "")
        cls._sdk_initialized = True

    @classmethod
    def shutdown_sdk(cls):
        """
        Shutdown the XA SDK. Call this when done with all devices.
        """
        if cls._sdk_initialized:
            XASDK.shutdown()
            cls._sdk_initialized = False

    def __init__(
            self,
            serial_number: str,
            timeout_ms: int = 30000,
            auto_enable: bool = False
    ):
        """
        Initialize connection to KDC101.

        Args:
            serial_number: Device serial number (e.g., "27007297")
            timeout_ms: Default timeout for operations in milliseconds
            auto_enable: If True, automatically enable motor on connection

        Raises:
            RuntimeError: If SDK not initialized. Call initialize_sdk() first.
        """
        if not self._sdk_initialized:
            raise RuntimeError(
                "SDK not initialized. Call SimpleKDC101.initialize_sdk() first."
            )

        self._device = XADevice(
            device=serial_number,
            transport="",
            operating_mode=TLMC_OperatingModes.Default
        )
        self.timeout_ms = timeout_ms

        if auto_enable:
            self.enable()

    # ==================== Connection Management ====================

    def close(self):
        """Close connection to the device."""
        self._device.close()

    # ==================== Enable/Disable ====================

    def enable(self):
        """Enable the motor (turn it on)."""
        self._device.native_api.set_enable_state(
            self._device.device_handle,
            TLMC_EnableStates.EnableState_Enabled
        )

    def disable(self):
        """Disable the motor (turn it off)."""
        self._device.native_api.set_enable_state(
            self._device.device_handle,
            TLMC_EnableStates.EnableState_Disabled
        )

    def is_enabled(self) -> bool:
        """
        Check if motor is enabled.

        Returns:
            True if enabled, False otherwise
        """
        state = self._device.native_api.get_enable_state(
            self._device.device_handle,
            self.timeout_ms
        )
        return state == TLMC_EnableStates.EnableState_Enabled

    # ==================== Unit Conversion ====================

    def to_device_units(
            self,
            physical_value: float,
            scale_type: TLMC_ScaleType = TLMC_ScaleType.TLMC_ScaleType_Distance,
            unit_type: TLMC_Unit = TLMC_Unit.TLMC_Unit_Millimetres
    ) -> int:
        """
        Convert physical units to device units.

        Args:
            physical_value: Value in physical units (e.g., 5.0 mm)
            scale_type: Type of measurement (Distance, Velocity, or Acceleration)
            unit_type: Physical unit (mm, degrees, etc.)

        Returns:
            Value in device units

        Example:
            device_units = motor.to_device_units(5.0, TLMC_ScaleType.TLMC_ScaleType_Distance, TLMC_Unit.TLMC_Unit_Millimetres)
        """
        return self._device.native_api.convert_from_physical_to_device(
            self._device.device_handle,
            scale_type,
            unit_type,
            physical_value
        )

    def to_physical_units(
            self,
            device_value: int,
            scale_type: TLMC_ScaleType = TLMC_ScaleType.TLMC_ScaleType_Distance
    ) -> float:
        """
        Convert device units to physical units.

        Args:
            device_value: Value in device units
            scale_type: Type of measurement (Distance, Velocity, or Acceleration)

        Returns:
            Value in physical units (unit depends on device configuration)

        Example:
            position_mm = motor.to_physical_units(10000, TLMC_ScaleType.TLMC_ScaleType_Distance)
        """
        return self._device.native_api.convert_from_device_units_to_physical(
            self._device.device_handle,
            scale_type,
            device_value
        )

    # ==================== Convenience Conversion Methods ====================

    def to_mm(self, device_units: int) -> float:
        """
        Convert device units to millimeters (convenience method).

        Args:
            device_units: Position in device units

        Returns:
            Position in millimeters
        """
        return self.to_physical_units(device_units, TLMC_ScaleType.TLMC_ScaleType_Distance)

    def from_mm(self, mm: float) -> int:
        """
        Convert millimeters to device units (convenience method).

        Args:
            mm: Position in millimeters

        Returns:
            Position in device units
        """
        return self.to_device_units(mm, TLMC_ScaleType.TLMC_ScaleType_Distance, TLMC_Unit.TLMC_Unit_Millimetres)

    def to_degrees(self, device_units: int) -> float:
        """
        Convert device units to degrees (convenience method).

        Args:
            device_units: Position in device units

        Returns:
            Position in degrees
        """
        return self.to_physical_units(device_units, TLMC_ScaleType.TLMC_ScaleType_Distance)

    def from_degrees(self, degrees: float) -> int:
        """
        Convert degrees to device units (convenience method).

        Args:
            degrees: Position in degrees

        Returns:
            Position in device units
        """
        return self.to_device_units(degrees, TLMC_ScaleType.TLMC_ScaleType_Distance, TLMC_Unit.TLMC_Unit_Degrees)

    # ==================== Homing ====================

    def home(self, wait: bool = True):
        """
        Home the motor to its reference position.

        Args:
            wait: If True, block until homing completes
        """
        timeout = self.timeout_ms if wait else 0
        self._device.native_api.home(self._device.device_handle, timeout)

    # ==================== Position Control ====================

    def get_position(self) -> int:
        """
        Get current motor position in device units.

        Returns:
            Current position in device units
        """
        return self._device.native_api.get_position_counter(
            self._device.device_handle,
            self.timeout_ms
        )

    def get_position_mm(self) -> float:
        """
        Get current motor position in millimeters.

        Returns:
            Current position in mm
        """
        device_pos = self.get_position()
        return self.to_mm(device_pos)

    def get_position_degrees(self) -> float:
        """
        Get current motor position in degrees.

        Returns:
            Current position in degrees
        """
        device_pos = self.get_position()
        return self.to_degrees(device_pos)

    def move_to(self, position: int, wait: bool = True):
        """
        Move to absolute position in device units.

        Args:
            position: Target position in device units
            wait: If True, block until move completes
        """
        # First, set the absolute position parameter
        self._device.native_api.set_move_absolute_params(
            self._device.device_handle,
            position
        )

        # Then execute the move
        timeout = self.timeout_ms if wait else 0
        self._device.native_api.move_absolute(
            self._device.device_handle,
            1,  # MoveMode_Absolute
            position,
            timeout
        )

    def move_to_mm(self, position_mm: float, wait: bool = True):
        """
        Move to absolute position in millimeters.

        Args:
            position_mm: Target position in mm
            wait: If True, block until move completes
        """
        device_units = self.from_mm(position_mm)
        self.move_to(device_units, wait)

    def move_to_degrees(self, position_deg: float, wait: bool = True):
        """
        Move to absolute position in degrees.

        Args:
            position_deg: Target position in degrees
            wait: If True, block until move completes
        """
        device_units = self.from_degrees(position_deg)
        self.move_to(device_units, wait)

    def move_by(self, distance: int, wait: bool = True):
        """
        Move by relative distance in device units.

        Args:
            distance: Distance to move (positive or negative) in device units
            wait: If True, block until move completes
        """
        # First, set the relative distance parameter
        self._device.native_api.set_move_relative_params(
            self._device.device_handle,
            distance
        )

        # Then execute the move
        timeout = self.timeout_ms if wait else 0
        self._device.native_api.move_relative(
            self._device.device_handle,
            2,  # MoveMode_Relative
            distance,
            timeout
        )

    def move_by_mm(self, distance_mm: float, wait: bool = True):
        """
        Move by relative distance in millimeters.

        Args:
            distance_mm: Distance to move (positive or negative) in mm
            wait: If True, block until move completes
        """
        device_units = self.from_mm(distance_mm)
        self.move_by(device_units, wait)

    def move_by_degrees(self, distance_deg: float, wait: bool = True):
        """
        Move by relative distance in degrees.

        Args:
            distance_deg: Distance to move (positive or negative) in degrees
            wait: If True, block until move completes
        """
        device_units = self.from_degrees(distance_deg)
        self.move_by(device_units, wait)

    def jog_forward(self, wait: bool = False):
        """
        Jog motor forward by configured jog step size.

        Args:
            wait: If True, block until jog completes
        """
        timeout = self.timeout_ms if wait else 0
        self._device.native_api.move_jog(
            self._device.device_handle,
            TLMC_MoveDirection.Move_Direction_Forward,
            timeout
        )

    def jog_backward(self, wait: bool = False):
        """
        Jog motor backward by configured jog step size.

        Args:
            wait: If True, block until jog completes
        """
        timeout = self.timeout_ms if wait else 0
        self._device.native_api.move_jog(
            self._device.device_handle,
            TLMC_MoveDirection.Move_Direction_Reverse,
            timeout
        )

    def stop(self, immediate: bool = False):
        """
        Stop motor movement.

        Args:
            immediate: If True, stop immediately; if False, use profiled deceleration
        """
        stop_mode = 2 if immediate else 1  # Immediate : Profiled
        self._device.native_api.stop(
            self._device.device_handle,
            stop_mode,
            self.timeout_ms
        )

    # ==================== Velocity Control ====================

    def set_velocity(
            self,
            max_velocity: int,
            acceleration: int,
            min_velocity: int = 0
    ):
        """
        Configure velocity parameters in device units.

        Args:
            max_velocity: Maximum velocity in device units/sec
            acceleration: Acceleration in device units/sec²
            min_velocity: Minimum velocity (usually 0)
        """
        self._device.native_api.set_velocity_params(
            self._device.device_handle,
            min_velocity,
            acceleration,
            max_velocity
        )

    def set_velocity_physical(
            self,
            max_velocity: float,
            acceleration: float,
            min_velocity: float = 0.0,
            unit_type: TLMC_Unit = TLMC_Unit.TLMC_Unit_Millimetres
    ):
        """
        Configure velocity parameters in physical units.

        Args:
            max_velocity: Maximum velocity (e.g., mm/sec)
            acceleration: Acceleration (e.g., mm/sec²)
            min_velocity: Minimum velocity (usually 0)
            unit_type: Physical unit (mm, degrees, etc.)
        """
        max_vel_dev = self.to_device_units(
            max_velocity, TLMC_ScaleType.TLMC_ScaleType_Velocity, unit_type
        )
        accel_dev = self.to_device_units(
            acceleration, TLMC_ScaleType.TLMC_ScaleType_Acceleration, unit_type
        )
        min_vel_dev = self.to_device_units(
            min_velocity, TLMC_ScaleType.TLMC_ScaleType_Velocity, unit_type
        )

        self.set_velocity(max_vel_dev, accel_dev, min_vel_dev)

    def get_velocity(self) -> tuple[int, int, int]:
        """
        Get current velocity parameters in device units.

        Returns:
            Tuple of (min_velocity, acceleration, max_velocity) in device units
        """
        params = self._device.native_api.get_velocity_params(
            self._device.device_handle,
            self.timeout_ms
        )
        return (params.minVelocity, params.acceleration, params.maxVelocity)

    def get_velocity_physical(self) -> tuple[float, float, float]:
        """
        Get current velocity parameters in physical units.

        Returns:
            Tuple of (min_velocity, acceleration, max_velocity) in physical units
        """
        min_vel_dev, accel_dev, max_vel_dev = self.get_velocity()

        min_vel = self.to_physical_units(min_vel_dev, TLMC_ScaleType.TLMC_ScaleType_Velocity)
        accel = self.to_physical_units(accel_dev, TLMC_ScaleType.TLMC_ScaleType_Acceleration)
        max_vel = self.to_physical_units(max_vel_dev, TLMC_ScaleType.TLMC_ScaleType_Velocity)

        return (min_vel, accel, max_vel)

    # ==================== Configuration ====================

    def set_jog_step(self, step_size: int):
        """
        Set the jog step size in device units.

        Args:
            step_size: Step size in device units
        """
        # Get current params first
        params = self._device.native_api.get_jog_params(
            self._device.device_handle,
            self.timeout_ms
        )

        # Update with new step size
        self._device.native_api.set_jog_params(
            self._device.device_handle,
            params.mode,
            step_size,
            params.minVelocity,
            params.maxVelocity,
            params.acceleration,
            params.stopMode
        )

    def set_jog_step_mm(self, step_size_mm: float):
        """
        Set the jog step size in millimeters.

        Args:
            step_size_mm: Step size in mm
        """
        device_units = self.from_mm(step_size_mm)
        self.set_jog_step(device_units)

    def set_jog_step_degrees(self, step_size_deg: float):
        """
        Set the jog step size in degrees.

        Args:
            step_size_deg: Step size in degrees
        """
        device_units = self.from_degrees(step_size_deg)
        self.set_jog_step(device_units)

    # ==================== Status ====================

    def get_status_bits(self) -> int:
        """
        Get device status as bit flags.

        Returns:
            32-bit status word
        """
        return self._device.native_api.get_universal_status_bits(
            self._device.device_handle,
            self.timeout_ms
        )

    def is_moving(self) -> bool:
        """
        Check if motor is currently moving.

        Returns:
            True if moving, False if stationary
        """
        status_bits = self.get_status_bits()
        # Bits 4-5 indicate motion status
        return (status_bits & 0x30) != 0x00

    # ==================== Device Information ====================

    def get_device_info(self) -> str:
        """
        Get basic device information.

        Returns:
            String with device info
        """
        info = self._device.native_api.get_device_info(self._device.device_handle)
        return f"Model: {info.modelNumber.decode()}, S/N: {info.serialNumber.decode()}"

    # ==================== Convenience Methods ====================

    def reset_position(self, new_position: int = 0):
        """
        Reset the position counter to a specific value without moving.

        Args:
            new_position: New position value (default: 0)
        """
        self._device.native_api.set_position_counter(
            self._device.device_handle,
            new_position
        )

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - ensures cleanup."""
        try:
            self.disable()
        except:
            pass
        self.close()
        return False


# Convenience function for quick usage
def create_kdc101(
        serial_number: str,
        dll_path: Optional[str] = None,
        auto_enable: bool = True,
        timeout_ms: int = 3000
) -> SimpleKDC101:
    """
    Convenience function to create and initialize a KDC101 device.
    Automatically initializes SDK if needed.

    Args:
        serial_number: Device serial number (e.g., "27007297")
        dll_path: Path to DLL directory (None for current dir)
        auto_enable: If True, automatically enable motor
        timeout_ms: Default timeout in milliseconds

    Returns:
        SimpleKDC101 instance ready to use

    Example:
        motor = create_kdc101("27007297")
        motor.home()
        motor.move_to_mm(10.0)
        print(f"Position: {motor.get_position_mm():.3f} mm")
        motor.close()
    """
    if not SimpleKDC101._sdk_initialized:
        SimpleKDC101.initialize_sdk(dll_path)

    return SimpleKDC101(serial_number, timeout_ms, auto_enable)