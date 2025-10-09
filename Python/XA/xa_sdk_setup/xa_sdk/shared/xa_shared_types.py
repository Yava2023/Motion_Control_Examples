# xa_shared_types.py (simplified & robust)
# Purpose: re-export the TLMC_* ctypes structures/enums and provide small helpers
# for decoding fixed-length C char arrays. This avoids drift from the header.

from __future__ import annotations
from typing import Any, Optional

# Import the real ctypes definitions (kept in sync with the C header)
from xa_sdk.shared.tlmc_type_structures import (
    # Common structs
    TLMC_DeviceInfo, TLMC_HardwareInfo, TLMC_ConnectedProductInfo, TLMC_RichResponse,
    TLMC_Setting, TLMC_AdcInputs, TLMC_VelocityParams, TLMC_GeneralMoveParams,
    TLMC_HomeParams, TLMC_IoConfigurationParams, TLMC_IoTriggerParams, TLMC_JogParams,
    TLMC_JoystickParams, TLMC_KcubeIoTriggerParams, TLMC_KcubeMmiParams,
    TLMC_KcubePositionTriggerParams, TLMC_LcdDisplayParams, TLMC_LcdMoveParams,
    TLMC_LimitSwitchParams, TLMC_MotorOutputParams, TLMC_MoveAbsoluteParams,
    TLMC_MoveRelativeParams, TLMC_PositionLoopParams, TLMC_PowerParams,
    TLMC_ProfileModeParams, TLMC_StageAxisParams, TLMC_StepperLoopParams,
    TLMC_StepperStatus, TLMC_TrackSettleParams, TLMC_TriggerParamsForDcBrushless,
    TLMC_TriggerParamsForStepper, TLMC_UniversalStatus,

    # Piezo (PZ)
    TLMC_PZ_MaxOutputVoltageParams, TLMC_PZ_OutputVoltageControlSourceParams,
    TLMC_PZ_OutputWaveformLookupTableSample, TLMC_PZ_OutputWaveformParams,
    TLMC_PZ_PositionLoopParams, TLMC_PZ_SlewRateParams, TLMC_PZ_Status,

    # Enums (import what you commonly use; you can extend this list)
    TLMC_ResultCodes, TLMC_OperatingModes, TLMC_EndOfMoveMessagesModes,
    TLMC_MoveModes, TLMC_StopModes, TLMC_Units, TLMC_ScaleTypes,
    TLMC_KcubeMmiLockStates, TLMC_JogStopModes, TLMC_LcdKnobModes,
    TLMC_IoTriggerPolarity, TLMC_IoTriggerInModes, TLMC_IoTriggerOutModes,
    TLMC_AuxIoPortModes, TLMC_IoPortModes, TLMC_EnableStates,
    TLMC_PZ_OutputVoltageControlSources, TLMC_PZ_OutputWaveformOperatingModes,
)

# Optional aliases with shorter names (pure re-exports)
DeviceInfo = TLMC_DeviceInfo
HardwareInfo = TLMC_HardwareInfo
ConnectedProductInfo = TLMC_ConnectedProductInfo
RichResponse = TLMC_RichResponse
Setting = TLMC_Setting
AdcInputs = TLMC_AdcInputs
VelocityParams = TLMC_VelocityParams
GeneralMoveParams = TLMC_GeneralMoveParams
HomeParams = TLMC_HomeParams
IoConfigurationParams = TLMC_IoConfigurationParams
IoTriggerParams = TLMC_IoTriggerParams
JogParams = TLMC_JogParams
JoystickParams = TLMC_JoystickParams
KcubeIoTriggerParams = TLMC_KcubeIoTriggerParams
KcubeMmiParams = TLMC_KcubeMmiParams
KcubePositionTriggerParams = TLMC_KcubePositionTriggerParams
LcdDisplayParams = TLMC_LcdDisplayParams
LcdMoveParams = TLMC_LcdMoveParams
LimitSwitchParams = TLMC_LimitSwitchParams
MotorOutputParams = TLMC_MotorOutputParams
MoveAbsoluteParams = TLMC_MoveAbsoluteParams
MoveRelativeParams = TLMC_MoveRelativeParams
PositionLoopParams = TLMC_PositionLoopParams
PowerParams = TLMC_PowerParams
ProfileModeParams = TLMC_ProfileModeParams
StageAxisParams = TLMC_StageAxisParams
StepperLoopParams = TLMC_StepperLoopParams
StepperStatus = TLMC_StepperStatus
TrackSettleParams = TLMC_TrackSettleParams
TriggerParamsForDcBrushless = TLMC_TriggerParamsForDcBrushless
TriggerParamsForStepper = TLMC_TriggerParamsForStepper
UniversalStatus = TLMC_UniversalStatus

PZ_MaxOutputVoltageParams = TLMC_PZ_MaxOutputVoltageParams
PZ_OutputVoltageControlSourceParams = TLMC_PZ_OutputVoltageControlSourceParams
PZ_OutputWaveformLookupTableSample = TLMC_PZ_OutputWaveformLookupTableSample
PZ_OutputWaveformParams = TLMC_PZ_OutputWaveformParams
PZ_PositionLoopParams = TLMC_PZ_PositionLoopParams
PZ_SlewRateParams = TLMC_PZ_SlewRateParams
PZ_Status = TLMC_PZ_Status

# --- Helpers for fixed-length C char arrays (char[N]) ---

def c_char_array_to_str(char_array: Any, encoding: str = "utf-8") -> str:
    """
    Convert a ctypes c_char * N inline array (e.g., partNumber[16]) to Python str.
    Example:
        pn = c_char_array_to_str(device_info.partNumber)
    """
    try:
        raw = bytes(char_array)
        return raw.split(b"\x00", 1)[0].decode(encoding, errors="ignore")
    except Exception:
        return ""

def safe_str(x: Optional[bytes | bytearray | memoryview | str]) -> str:
    """Best-effort string conversion that tolerates bytes/None and strips trailing NUL."""
    if x is None:
        return ""
    if isinstance(x, (bytes, bytearray, memoryview)):
        return bytes(x).split(b"\x00", 1)[0].decode("utf-8", "ignore")
    return str(x)