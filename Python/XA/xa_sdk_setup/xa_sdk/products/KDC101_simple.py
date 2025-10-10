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

        # Move to positions
        motor.move_to(10000)
        motor.move_by(5000)

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
        Get current motor position.

        Returns:
            Current position in device units
        """
        return self._device.native_api.get_position_counter(
            self._device.device_handle,
            self.timeout_ms
        )

    def move_to(self, position: int, wait: bool = True):
        """
        Move to absolute position.

        Args:
            position: Target position in device units
            wait: If True, block until move completes
        """
        timeout = self.timeout_ms if wait else 0
        self._device.native_api.move_absolute(
            self._device.device_handle,
            1,  # MoveMode_Absolute
            position,
            timeout
        )

    def move_by(self, distance: int, wait: bool = True):
        """
        Move by relative distance.

        Args:
            distance: Distance to move (positive or negative) in device units
            wait: If True, block until move completes
        """
        timeout = self.timeout_ms if wait else 0
        self._device.native_api.move_relative(
            self._device.device_handle,
            2,  # MoveMode_Relative
            distance,
            timeout
        )

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
        Configure velocity parameters.

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

    def get_velocity(self) -> tuple[int, int, int]:
        """
        Get current velocity parameters.

        Returns:
            Tuple of (min_velocity, acceleration, max_velocity)
        """
        params = self._device.native_api.get_velocity_params(
            self._device.device_handle,
            self.timeout_ms
        )
        return (params.minVelocity, params.acceleration, params.maxVelocity)

    # ==================== Configuration ====================

    def set_jog_step(self, step_size: int):
        """
        Set the jog step size.

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
        motor.move_to(10000)
        motor.close()
    """
    if not SimpleKDC101._sdk_initialized:
        SimpleKDC101.initialize_sdk(dll_path)

    return SimpleKDC101(serial_number, timeout_ms, auto_enable)