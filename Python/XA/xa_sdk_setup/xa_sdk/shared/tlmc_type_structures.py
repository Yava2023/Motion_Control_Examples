# tlmc_type_structures.py  — Corrected to match tlmc_xa_native_api.h
# - All enums are IntEnum/IntFlag with correct integer values (no trailing commas).
# - All structs/unions align field names, types, and pack(1) to the header.
# - Field names used by tlmc_core.py are present (e.g., productId, gearboxRatio, openLoopSlewRate, joystickSensitivity).
# - Only minimal aliases are provided; if you need more compatibility shims, say the word.

from enum import IntEnum, IntFlag, auto
from ctypes import (
    c_uint8, c_uint16, c_uint32, c_int8, c_int16, c_int32, c_longlong, c_double, c_bool,
    c_char, c_size_t, Structure, Union
)

# ----------------
#   Enumerations
# ----------------

class TLMC_AnalogMonitorMotorChannel(IntEnum):
    TLMC_AnalogMonitorMotorChannel_1 = 0x0001
    TLMC_AnalogMonitorMotorChannel_2 = 0x0002

class TLMC_AnalogMonitorNumber(IntEnum):
    TLMC_AnalogueMonitorNumber_1 = 0x0001
    TLMC_AnalogueMonitorNumber_2 = 0x0002

class TLMC_AnalogMonitorSystemVariable(IntEnum):
    TLMC_AnalogMonitorSystemVariable_PositionError = 0x0001
    TLMC_AnalogMonitorSystemVariable_Position = 0x0002
    TLMC_AnalogMonitorSystemVariable_MotorCurrentPhaseA = 0x0003
    TLMC_AnalogMonitorSystemVariable_MotorCurrentPhaseB = 0x0004
    TLMC_AnalogMonitorSystemVariable_MotorCurrentPhaseC = 0x0005
    TLMC_AnalogMonitorSystemVariable_MotorCurrent = 0x0006

class TLMC_AuxIoPortMode(IntEnum):
    TLMC_AuxIoPortMode_None = 0x0000
    TLMC_AuxIoPortMode_SoftwareControlled = 0x0001
    TLMC_AuxIoPortMode_EncoderOutput = 0x0002

class TLMC_AuxIoPortNumber(IntEnum):
    TLMC_AuxIoPortNumber_None = 0x0000
    TLMC_AuxIoPortNumber_Port1 = 0x0001
    TLMC_AuxIoPortNumber_Port2 = 0x0002
    TLMC_AuxIoPortNumber_Port3 = 0x0004

class TLMC_BowIndex(IntEnum):
    TLMC_BowIndex_Trapezoidal = 0
    TLMC_BowIndex_SCurve1 = 1
    TLMC_BowIndex_SCurve2 = 2
    TLMC_BowIndex_SCurve3 = 3
    TLMC_BowIndex_SCurve4 = 4
    TLMC_BowIndex_SCurve5 = 5
    TLMC_BowIndex_SCurve6 = 6
    TLMC_BowIndex_SCurve7 = 7
    TLMC_BowIndex_SCurve8 = 8
    TLMC_BowIndex_SCurve9 = 9
    TLMC_BowIndex_SCurve10 = 10
    TLMC_BowIndex_SCurve11 = 11
    TLMC_BowIndex_SCurve12 = 12
    TLMC_BowIndex_SCurve13 = 13
    TLMC_BowIndex_SCurve14 = 14
    TLMC_BowIndex_SCurve15 = 15
    TLMC_BowIndex_SCurve16 = 16
    TLMC_BowIndex_SCurve17 = 17
    TLMC_BowIndex_SCurve18 = 18

class TLMC_ConnectedProductAxisType(IntEnum):
    TLMC_ConnectedProductAxisType_Unknown = 0
    TLMC_ConnectedProductAxisType_Single = 1
    TLMC_ConnectedProductAxisType_Rotary = 2
    TLMC_ConnectedProductAxisType_X = 3
    TLMC_ConnectedProductAxisType_Y = 4
    TLMC_ConnectedProductAxisType_Z = 5
    TLMC_ConnectedProductAxisType_Pitch = 6
    TLMC_ConnectedProductAxisType_Roll = 7
    TLMC_ConnectedProductAxisType_Yaw = 8
    TLMC_ConnectedProductAxisType_Goniometer = 9

class TLMC_ConnectedProductMovementType(IntEnum):
    TLMC_ConnectedProductMovementType_Unknown = 0
    TLMC_ConnectedProductMovementType_Linear = 1
    TLMC_ConnectedProductMovementType_RotaryContinuous = 2
    TLMC_ConnectedProductMovementType_RotaryFixedRange = 3

class TLMC_CurrentLoopPhase(IntEnum):
    TLMC_CurrentLoopPhase_A = 0x0000
    TLMC_CurrentLoopPhase_B = 0x0001
    TLMC_CurrentLoopPhase_AB = 0x0002

class TLMC_CurrentLoopScenario(IntEnum):
    TLMC_CurrentLoopScenario_Single = 0x0000
    TLMC_CurrentLoopScenario_Normal = 0x0001
    TLMC_CurrentLoopScenario_Settled = 0x0002

class TLMC_DcPidUpdateFilter(IntFlag):
    TLMC_DcPidUpdateFilter_None = 0x0000
    TLMC_DcPidUpdateFilter_IntegralLimit = 0x0001
    TLMC_DcPidUpdateFilter_Derivative = 0x0002
    TLMC_DcPidUpdateFilter_Integral = 0x0004
    TLMC_DcPidUpdateFilter_Proportional = 0x0008
    TLMC_DcPidUpdateFilter_All = (
        TLMC_DcPidUpdateFilter_IntegralLimit
        | TLMC_DcPidUpdateFilter_Derivative
        | TLMC_DcPidUpdateFilter_Integral
        | TLMC_DcPidUpdateFilter_Proportional
    )

class TLMC_DeviceFamily(IntEnum):
    TLMC_DeviceFamily_ThorlabsMotionControl = 0

class TLMC_DeviceType(IntEnum):
    TLMC_DeviceType_Bbd30xBaseUnit = 0
    TLMC_DeviceType_Bbd30xLogicalChannel = 1
    TLMC_DeviceType_Bpc301 = 2
    TLMC_DeviceType_Bpc30xBaseUnit = 3
    TLMC_DeviceType_Bpc30xLogicalChannel = 4
    TLMC_DeviceType_Bsc20xBaseUnit = 5
    TLMC_DeviceType_Bsc20xLogicalChannel = 6
    TLMC_DeviceType_Kbd101 = 7
    TLMC_DeviceType_Kdc101 = 8
    TLMC_DeviceType_Kpz101 = 9
    TLMC_DeviceType_Kst101 = 10
    TLMC_DeviceType_Kst201 = 11
    TLMC_DeviceType_Tbd001 = 12
    TLMC_DeviceType_LinearTranslationStage = 13  # present in header

class TLMC_DeviceListChange(IntEnum):
    TLMC_DeviceListChange_EntryAdded = 0
    TLMC_DeviceListChange_EntryRemoved = 1

class TLMC_DigitalInput(IntFlag):
    TLMC_DigitalInput_None = 0x00000000
    TLMC_DigitalInput_1 = 0x00000001
    TLMC_DigitalInput_2 = 0x00000002
    TLMC_DigitalInput_3 = 0x00000004
    TLMC_DigitalInput_4 = 0x00000008
    TLMC_DigitalInput_All = (TLMC_DigitalInput_1 | TLMC_DigitalInput_2 | TLMC_DigitalInput_3 | TLMC_DigitalInput_4)

class TLMC_DigitalOutput(IntFlag):
    TLMC_DigitalOutput_None = 0x00
    TLMC_DigitalOutput_1 = 0x01
    TLMC_DigitalOutput_2 = 0x02
    TLMC_DigitalOutput_3 = 0x04
    TLMC_DigitalOutput_4 = 0x08
    TLMC_DigitalOutput_All = (TLMC_DigitalOutput_1 | TLMC_DigitalOutput_2 | TLMC_DigitalOutput_3 | TLMC_DigitalOutput_4)

class TLMC_EnableState(IntEnum):
    TLMC_Enabled = 0x01
    TLMC_Disabled = 0x02

class TLMC_HardLimitOperatingModes(IntEnum):
    HardLimitOperatingMode_SwitchIgnored = 0x0001
    HardLimitOperatingMode_SwitchContactMakes = 0x0002
    HardLimitOperatingMode_SwitchContactBreaks = 0x0003
    HardLimitOperatingMode_SwitchContactMakesWhenHoming = 0x0004
    HardLimitOperatingMode_SwitchContactBreaksWhenHoming = 0x0005
    HardLimitOperatingMode_SwitchUseIndexMarkForHoming = 0x0006
    HardLimitOperatingMode_SwitchesSwapped = 0x0080

class TLMC_HomeDirections(IntEnum):
    HomeDirection_Forward = 0x0001
    HomeDirection_Reverse = 0x0002

class TLMC_HomeLimitSwitches(IntEnum):
    HomeLimitSwitch_Reverse = 0x0001
    HomeLimitSwitch_Forward = 0x0004

class TLMC_IoPortMode(IntEnum):
    TLMC_IoPortMode_DigitalInput = 0x0000
    TLMC_IoPortMode_DigitalOutput = 0x0001
    TLMC_IoPortMode_AnalogOutput = 0x0002

class TLMC_IoPortNumber(IntEnum):
    TLMC_IoPortNumber_Port1 = 0x0001
    TLMC_IoPortNumber_Port2 = 0x0002
    TLMC_IoPortNumber_Port3 = 0x0003

class TLMC_IoPortSource(IntEnum):
    TLMC_IoPortSource_Software = 0x0000
    TLMC_IoPortSource_Channel1 = 0x0001
    TLMC_IoPortSource_Channel2 = 0x0002
    TLMC_IoPortSource_Channel3 = 0x0003

class TLMC_IoPositionTriggerEnableState(IntEnum):
    TLMC_IoPositionTriggerEnableState_Armed = 0x01
    TLMC_IoPositionTriggerEnableState_Canceled = 0x02

class TLMC_IoTriggerInMode(IntEnum):
    TLMC_IoTriggerInMode_Disabled = 0x0000
    TLMC_IoTriggerInMode_GeneralPurpose = 0x0001
    TLMC_IoTriggerInMode_TriggersRelativeMove = 0x0002
    TLMC_IoTriggerInMode_TriggersAbsoluteMove = 0x0003
    TLMC_IoTriggerInMode_TriggersHomeMove = 0x0004

class TLMC_IoTriggerInSource(IntEnum):
    TLMC_IoTriggerInSource_Software = 0x0000
    TLMC_IoTriggerInSource_BNC1 = 0x0001
    TLMC_IoTriggerInSource_BNC2 = 0x0002
    TLMC_IoTriggerInSource_BNC3 = 0x0003

class TLMC_IoTriggerOutMode(IntEnum):
    TLMC_IoTriggerOutMode_GeneralPurpose = 0x000A
    TLMC_IoTriggerOutMode_ActiveDuringMotion = 0x000B
    TLMC_IoTriggerOutMode_ActiveAtMaxVelocity = 0x000C
    TLMC_IoTriggerOutMode_PulsedInForwardDirection = 0x000D
    TLMC_IoTriggerOutMode_PulsedInReverseDirection = 0x000E
    TLMC_IoTriggerOutMode_PulsedInBothDirections = 0x000F
    TLMC_IoTriggerOutMode_ActiveAtForwardLimit = 0x0010
    TLMC_IoTriggerOutMode_ActiveAtReverseLimit = 0x0011
    TLMC_IoTriggerOutMode_ActiveAtBothLimits = 0x0012

class TLMC_IoTriggerPolarity(IntEnum):
    TLMC_IoTriggerPolarity_ActiveIsLogicHigh = 0x0001
    TLMC_IoTriggerPolarity_ActiveIsLogicLow = 0x0002

class TLMC_JogModes(IntEnum):
    JogMode_Continuous = 0x0001
    JogMode_SingleStep = 0x0002

class TLMC_JogStopModes(IntEnum):
    JogStopMode_Immediate = 0x0001
    JogStopMode_Profiled = 0x0002

class TLMC_JoystickDirectionSense(IntEnum):
    TLMC_JoystickDirectionSense_Positive = 0x0001
    TLMC_JoystickDirectionSense_Negative = 0x0002

class TLMC_KcubeIoTriggerMode(IntEnum):
    TLMC_KcubeIoTriggerMode_Disabled = 0x0000
    TLMC_KcubeIoTriggerMode_GeneralPurposeInput = 0x0001
    TLMC_KcubeIoTriggerMode_InputTriggersRelativeMove = 0x0002
    TLMC_KcubeIoTriggerMode_InputTriggersAbsoluteMove = 0x0003
    TLMC_KcubeIoTriggerMode_InputTriggersHomeMove = 0x0004
    TLMC_KcubeIoTriggerMode_GeneralPurposeOutput = 0x000A
    TLMC_KcubeIoTriggerMode_OutputActiveDuringMotion = 0x000B
    TLMC_KcubeIoTriggerMode_OutputActiveAtMaxVelocity = 0x000C
    TLMC_KcubeIoTriggerMode_OutputPulsedInForwardDirection = 0x000D
    TLMC_KcubeIoTriggerMode_OutputPulsedInReverseDirection = 0x000E
    TLMC_KcubeIoTriggerMode_OutputPulsedInBothDirections = 0x000F

class TLMC_KcubeIoTriggerPolarity(IntEnum):
    TLMC_KcubeIoTriggerPolarity_ActiveIsLogicHigh = 0x0001
    TLMC_KcubeIoTriggerPolarity_ActiveIsLogicLow = 0x0002

class TLMC_KcubeMmi_JoystickDirectionSense(IntEnum):
    TLMC_KcubeMmi_JoystickDirectionSense_Disabled = 0x0000
    TLMC_KcubeMmi_JoystickDirectionSense_Normal = 0x0001
    TLMC_KcubeMmi_JoystickDirectionSense_Inverted = 0x0002

class TLMC_KcubeMmi_JoystickMode(IntEnum):
    TLMC_KcubeMmi_JoystickMode_ControlsVelocity = 0x0001
    TLMC_KcubeMmi_JoystickMode_Jogs = 0x0002
    TLMC_KcubeMmi_JoystickMode_GoesToPosition = 0x0003

class TLMC_KcubeMmiLockState(IntEnum):
    TLMC_KcubeMmiLockState_Locked = 0x01
    TLMC_KcubeMmiLockState_Unlocked = 0x02

class TLMC_LcdKnobMode(IntEnum):
    TLMC_LcdKnobMode_Velocity = 0x0001
    TLMC_LcdKnobMode_Jog = 0x0002

class TLMC_LogLevel(IntEnum):
    TLMC_LogLevel_Critical = 0x0002
    TLMC_LogLevel_Error = 0x0003
    TLMC_LogLevel_Warning = 0x0004
    TLMC_LogLevel_Information = 0x0005

class TLMC_LogCategoryFilter(IntFlag):
    TLMC_LogCategoryFilter_User = 0x00000001
    TLMC_LogCategoryFilter_Internal = 0x00000002
    TLMC_LogCategoryFilter_Communication = 0x00000004
    TLMC_LogCategoryFilter_NativeApi = 0x00000008
    TLMC_LogCategoryFilter_All = 0xFFFFFFFF

class TLMC_MoveModes(IntEnum):
    MoveMode_Absolute = 0
    MoveMode_AbsoluteToProgrammedPosition = auto()
    MoveMode_Relative = auto()
    MoveMode_RelativeByProgrammedDistance = auto()
    MoveMode_ContinuousForward = auto()
    MoveMode_ContinuousReverse = auto()
    MoveMode_JogForward = auto()
    MoveMode_JogReverse = auto()

class TLMC_MoveDirection(IntEnum):
    Move_Direction_Forward = 0
    Move_Direction_Reverse = 1

class TLMC_OperatingModes(IntFlag):
    StatusPushedByController = 0x00000000
    ManualStatusPolling = 0x00000001
    AutomaticStatusPolling = 0x00000002
    DoNotChangeStatusPollingMode = 0x00000004
    SendEndOfMoveMessages = 0x00000100
    DoNotSendEndOfMoveMessages = 0x00000200
    DoNotLoadParamsOnConnect = 0x00010000
    DoNotSendDisconnectOnFinalClose = 0x00020000
    DoNotAutoSetConnectedProduct = 0x00040000
    DoNotSendNoFlashProgrammingOnConnect = 0x00080000
    Apt = (StatusPushedByController | SendEndOfMoveMessages)
    Kinesis = (AutomaticStatusPolling | SendEndOfMoveMessages)
    Default = Apt
    Expert = (DoNotChangeStatusPollingMode | DoNotLoadParamsOnConnect | DoNotSendDisconnectOnFinalClose | DoNotAutoSetConnectedProduct)

class TLMC_ParameterGroupId(IntEnum):
    TLMC_ParameterGroupId_Unspecified = 0x0000
    TLMC_ParameterGroupId_JogParams = 0x0416
    TLMC_ParameterGroupId_LimitSwitchParams = 0x0423
    TLMC_ParameterGroupId_GenMoveParams = 0x043A
    TLMC_ParameterGroupId_HomeParams = 0x0440
    TLMC_ParameterGroupId_JoystickParams = 0x04E6
    TLMC_ParameterGroupId_BowIndex = 0x04F4
    TLMC_ParameterGroupId_StepperLoopParams = 0x0529

class TLMC_PositionLoopScenario(IntEnum):
    TLMC_PositionLoopScenario_Single = 0x0000
    TLMC_PositionLoopScenario_Stationary = 0x0001
    TLMC_PositionLoopScenario_Accelerating = 0x0002
    TLMC_PositionLoopScenario_AtConstantVelocity = 0x0003

class TLMC_ProfileMode(IntEnum):
    TLMC_ProfileMode_Trapezoidal = 0x0000
    TLMC_ProfileMode_VelocityContouring = 0x0001
    TLMC_ProfileMode_SCurve = 0x0002
    TLMC_ProfileMode_ElectronicGear = 0x0003

class TLMC_PZ_OutputVoltageControlSource(IntEnum):
    TLMC_PZ_OutputVoltageControlSource_SoftwareOnly = 0x0000
    TLMC_PZ_OutputVoltageControlSource_ExternalSignal = 0x0001
    TLMC_PZ_OutputVoltageControlSource_Knob = 0x0002

class TLMC_PZ_OutputWaveformOperatingMode(IntEnum):
    TLMC_PZ_OutputWaveformOperatingMode_Continuous = 0x0001
    TLMC_PZ_OutputWaveformOperatingMode_FixedNumberOfCycles = 0x0002
    TLMC_PZ_OutputWaveformOperatingMode_OutputTriggerEnabled = 0x0004
    TLMC_PZ_OutputWaveformOperatingMode_InputTriggerEnabled = 0x0008
    TLMC_PZ_OutputWaveformOperatingMode_OutputTriggerRisingEdge = 0x0010
    TLMC_PZ_OutputWaveformOperatingMode_InputTriggerRisingEdge = 0x0020
    TLMC_PZ_OutputWaveformOperatingMode_OutputGated = 0x0040
    TLMC_PZ_OutputWaveformOperatingMode_TriggerRepeats = 0x0080

class TLMC_PZ_PositionControlMode(IntEnum):
    TLMC_PZ_PositionControlMode_OpenLoop = 0x01
    TLMC_PZ_PositionControlMode_ClosedLoop = 0x02
    TLMC_PZ_PositionControlMode_OpenLoopSmooth = 0x03
    TLMC_PZ_PositionControlMode_ClosedLoopSmooth = 0x04

class TLMC_PZ_StatusBits(IntEnum):
    TLMC_PZ_StatusBit_ActuatorConnected = 0x00000001
    TLMC_PZ_StatusBit_Zeroed = 0x00000010
    TLMC_PZ_StatusBit_Zeroing = 0x00000020
    TLMC_PZ_StatusBit_ExternalStrainGaugeConnected = 0x00000100
    TLMC_PZ_StatusBit_ClosedLoopPositionControl = 0x00000400
    TLMC_PZ_StatusBit_MaxOutputVoltageLow = 0x00001000
    TLMC_PZ_StatusBit_MaxOutputVoltageMedium = 0x00002000
    TLMC_PZ_StatusBit_MaxOutputVoltageHigh = 0x00004000
    TLMC_PZ_StatusBit_DigitalInput1 = 0x00100000
    TLMC_PZ_StatusBit_DigitalInput2 = 0x00200000
    TLMC_PZ_StatusBit_DigitalInput3 = 0x00400000
    TLMC_PZ_StatusBit_DigitalInput4 = 0x00800000
    TLMC_PZ_StatusBit_DigitalInput5 = 0x01000000
    TLMC_PZ_StatusBit_DigitalInput6 = 0x02000000
    TLMC_PZ_StatusBit_DigitalInput7 = 0x04000000
    TLMC_PZ_StatusBit_DigitalInput8 = 0x08000000
    TLMC_PZ_StatusBit_Active = 0x20000000
    TLMC_PZ_StatusBit_Enabled = 0x80000000

class TLMC_PZ_VoltageLimit(IntEnum):
    TLMC_PZ_VoltageLimit_75Volts = 0x0002
    TLMC_PZ_VoltageLimit_100Volts = 0x0004
    TLMC_PZ_VoltageLimit_150Volts = 0x0008

class TLMC_RackBayNumber(IntEnum):
    TLMC_RackBayNumber_1 = 0x0000
    TLMC_RackBayNumber_2 = 0x0001
    TLMC_RackBayNumber_3 = 0x0002
    TLMC_RackBayNumber_4 = 0x0003
    TLMC_RackBayNumber_5 = 0x0004
    TLMC_RackBayNumber_6 = 0x0005
    TLMC_RackBayNumber_7 = 0x0006
    TLMC_RackBayNumber_8 = 0x0007
    TLMC_RackBayNumber_9 = 0x0008
    TLMC_RackBayNumber_10 = 0x0009
    TLMC_RackBayNumber_11 = 0x000A
    TLMC_RackBayNumber_12 = 0x000B

class TLMC_RackBayOccupiedState(IntEnum):
    TLMC_RackBayState_Occupied = 0x0001
    TLMC_RackBayState_Empty = 0x0002

class TLMC_ResultCodes(IntEnum):
    Success = 0
    FunctionNotSupported = 1
    DeviceNotFound = 2
    DeviceNotSupported = 3
    Timeout = 4
    Fail = 5
    InsufficientFirmware = 6
    AlreadyStarted = 7
    StartRequired = 8
    AllocationError = 9
    InternalError = 10
    InvalidHandle = 11
    InvalidArgument = 12
    ItemIsReadOnly = 13
    LoadParamsError = 14
    TransportError = 15
    TransportClosed = 16
    TransportNotAvailable = 17
    SharingModeNotAvailable = 18
    NotInitialized = 19
    NoFreeHandles = 20
    VerificationFailure = 21
    DataNotLoaded = 22
    ConnectedProductNotSupported = 23
    SimulationCreationError = 24
    ConnectedProductNotSet = 25
    CalibrationFileNotPresent = 26

class TLMC_ScaleType(IntEnum):
    TLMC_ScaleType_None = 0
    TLMC_ScaleType_Distance = 1
    TLMC_ScaleType_Velocity = 2
    TLMC_ScaleType_Acceleration = 3
    TLMC_ScaleType_Voltage = 4
    TLMC_ScaleType_Brightness = 5
    TLMC_ScaleType_Time = 6
    TLMC_ScaleType_Deceleration = 7
    TLMC_ScaleType_Jerk = 8
    TLMC_ScaleType_RescaledProportion = 9
    TLMC_ScaleType_SlewRate = 10

class TLMC_SettingStringFormat(IntEnum):
    TLMC_SettingStringFormat_SemiStructured = 0
    TLMC_SettingStringFormat_Json = 1

class TLMC_SoftLimitOperatingModes(IntEnum):
    TLMC_SoftLimitOperatingMode_FeatureNotSupported = 0x0000
    TLMC_SoftLimitOperatingMode_Ignored = 0x0001
    TLMC_SoftLimitOperatingMode_StopImmediate = 0x0002
    TLMC_SoftLimitOperatingMode_StopProfiled = 0x0003
    TLMC_SoftLimitOperatingMode_RestrictMoves = 0x0004
    TLMC_SoftLimitOperatingMode_FilterWheelConnected = 0x0040
    TLMC_SoftLimitOperatingMode_RotationalStageConnected = 0x0080

class TLMC_StageAxis_AxisId(IntEnum):
    TLMC_StageAxisId_Unknown = 0x0001
    TLMC_StageAxisId_Rotary = 0x0003
    TLMC_StageAxisId_X = 0x0010
    TLMC_StageAxisId_Y = 0x0011
    TLMC_StageAxisId_Single = 0x0012

class TLMC_StageAxis_TypeId(IntEnum):  # actually Stage Product Id in header
    TLMC_StageAxisType_Unknown = 0x0001
    TLMC_StageAxisType_MLS203_X = 0x0010
    TLMC_StageAxisType_MLS203_Y = 0x0011
    TLMC_StageAxisType_DDS = 0x0012
    TLMC_StageAxisType_DDR = 0x0075

class TLMC_StatusItemIds(IntEnum):
    StatusItemId_Active = 0
    StatusItemId_ActuatorConnected = 1
    StatusItemId_BusOvercurrent = 2
    StatusItemId_BusCurrentFault = 3
    StatusItemId_BusVoltageFault = 4
    StatusItemId_ClockwiseHardLimit = 5
    StatusItemId_CounterclockwiseHardLimit = 6
    StatusItemId_ClockwiseSoftLimit = 7
    StatusItemId_CommutationError = 8
    StatusItemId_Connected = 9
    StatusItemId_CounterclockwiseSoftLimit = 10
    StatusItemId_ClosedLoopPositionControl = 11
    StatusItemId_DigitalInput1 = 12
    StatusItemId_DigitalInput2 = 13
    StatusItemId_DigitalInput3 = 14
    StatusItemId_DigitalInput4 = 15
    StatusItemId_DigitalInput5 = 16
    StatusItemId_DigitalInput6 = 17
    StatusItemId_DigitalInput7 = 18
    StatusItemId_DigitalInput8 = 19
    StatusItemId_E2PROMFailure = 20
    StatusItemId_Enabled = 21
    StatusItemId_EncoderCount = 22
    StatusItemId_EncoderFault = 23
    StatusItemId_Error = 24
    StatusItemId_ExternalStrainGaugeConnected = 25
    StatusItemId_Homing = 26
    StatusItemId_HomingFailed = 27
    StatusItemId_Homed = 28
    StatusItemId_Initializing = 29
    StatusItemId_InstrumentError = 30
    StatusItemId_Interlock = 31
    StatusItemId_IonBusVoltage = 32
    StatusItemId_IonInstructionError = 33
    StatusItemId_IonCommutationError = 34
    StatusItemId_IonOvercurrent = 35
    StatusItemId_IonOvertemperature = 36
    StatusItemId_IonReceiveTimeout = 37
    StatusItemId_IonInterlockOpen = 38
    StatusItemId_IonPhaseInitializationFailed = 39
    StatusItemId_JoggingClockwise = 40
    StatusItemId_JoggingCounterclockwise = 41
    StatusItemId_MotorCurrent = 42
    StatusItemId_MotorOvercurrent = 43
    StatusItemId_MovingClockwise = 44
    StatusItemId_MovingCounterclockwise = 45
    StatusItemId_OutputVoltage = 46
    StatusItemId_Overcurrent = 47
    StatusItemId_Overload = 48
    StatusItemId_Overtemperature = 49
    StatusItemId_PhaseInitializationFailure = 50
    StatusItemId_Position = 51
    StatusItemId_PositionError = 52
    StatusItemId_PowerOk = 53
    StatusItemId_Settled = 54
    StatusItemId_Tracking = 55
    StatusItemId_UnrecognisedError = 56
    StatusItemId_Velocity = 57
    StatusItemId_VelocityLimitExceeded = 58
    StatusItemId_Zeroed = 59
    StatusItemId_Zeroing = 60

class TLMC_StepperStatusBits(IntEnum):
    TLMC_StepperStatusBit_ClockwiseHardLimit = 0x00000001
    TLMC_StepperStatusBit_CounterclockwiseHardLimit = 0x00000002
    TLMC_StepperStatusBit_MovingClockwise = 0x00000010
    TLMC_StepperStatusBit_MovingCounterclockwise = 0x00000020
    TLMC_StepperStatusBit_JoggingClockwise = 0x00000040
    TLMC_StepperStatusBit_JoggingCounterclockwise = 0x00000080
    TLMC_StepperStatusBit_Homing = 0x00000200
    TLMC_StepperStatusBit_Homed = 0x00000400
    TLMC_StepperStatusBit_DigitalInput1 = 0x00100000
    TLMC_StepperStatusBit_DigitalInput2 = 0x00200000
    TLMC_StepperStatusBit_Enabled = 0x80000000

class TLMC_StepperLoopParams_LoopMode(IntEnum):
    TLMC_StepperLoopParams_LoopMode_Open = 0x0001
    TLMC_StepperLoopParams_LoopMode_Closed = 0x0002

class TLMC_StopModes(IntEnum):
    StopMode_Immediate = 1
    StopMode_Profiled = 2

class TLMC_TriggerModesForDcBrushless(IntEnum):
    TLMC_TriggerModesForDcBrushless_InputActiveIsLogicHigh = 0x01
    TLMC_TriggerModesForDcBrushless_InputTriggersRelativeMove = 0x02
    TLMC_TriggerModesForDcBrushless_InputTriggersAbsoluteMove = 0x04
    TLMC_TriggerModesForDcBrushless_InputTriggersHomeMove = 0x08
    TLMC_TriggerModesForDcBrushless_OutputActiveIsLogicHigh = 0x10
    TLMC_TriggerModesForDcBrushless_OutputActiveDuringMotion = 0x20
    TLMC_TriggerModesForDcBrushless_OutputActiveWhenMotionComplete = 0x40
    TLMC_TriggerModesForDcBrushless_OutputActiveAtMaxVelocity = 0x80

class TLMC_TriggerModesForStepper(IntEnum):
    TLMC_TriggerModesForStepper_None = 0x00
    TLMC_TriggerModesForStepper_InputTriggerEnabled = 0x01
    TLMC_TriggerModesForStepper_OutputTriggerEnabled = 0x02
    TLMC_TriggerModesForStepper_OutputTriggerFollowsInputTrigger = 0x04
    TLMC_TriggerModesForStepper_OutputActiveUntilMoveEnd = 0x08
    TLMC_TriggerModesForStepper_InputTriggersRelativeMove = 0x10
    TLMC_TriggerModesForStepper_InputTriggersAbsoluteMove = 0x20
    TLMC_TriggerModesForStepper_InputTriggersHomeMove = 0x40
    TLMC_TriggerModesForStepper_OutputTriggerSoftwareInitiated = 0x80

class TLMC_Unit(IntEnum):
    TLMC_Unit_Unspecified = 0
    TLMC_Unit_Millimetres = 1
    TLMC_Unit_Degrees = 2
    TLMC_Unit_Radians = 3
    TLMC_Unit_Cycles = 4
    TLMC_Unit_Micrometres = 5
    TLMC_Unit_Volts = 6
    TLMC_Unit_EncoderCounts = 7
    TLMC_Unit_EncoderCountsPerCycle = 8
    TLMC_Unit_EncoderCountsPerCyclePerCycle = 9
    TLMC_Unit_Minutes = 10
    TLMC_Unit_Microseconds = 11
    TLMC_Unit_MillimetresPerSecondPerSecondPerSecond = 12
    TLMC_Unit_Percentage = 13
    TLMC_Unit_VoltsPerMillisecond = 14
    TLMC_Unit_Milliseconds = 15

class TLMC_UniversalStatusBits(IntEnum):
    TLMC_UniversalStatusBit_ClockwiseHardLimit = 0x00000001
    TLMC_UniversalStatusBit_CounterclockwiseHardLimit = 0x00000002
    TLMC_UniversalStatusBit_ClockwiseSoftLimit = 0x00000004
    TLMC_UniversalStatusBit_CounterclockwiseSoftLimit = 0x00000008
    TLMC_UniversalStatusBit_MovingClockwise = 0x00000010
    TLMC_UniversalStatusBit_MovingCounterclockwise = 0x00000020
    TLMC_UniversalStatusBit_JoggingClockwise = 0x00000040
    TLMC_UniversalStatusBit_JoggingCounterclockwise = 0x00000080
    TLMC_UniversalStatusBit_Connected = 0x00000100
    TLMC_UniversalStatusBit_Homing = 0x00000200
    TLMC_UniversalStatusBit_Homed = 0x00000400
    TLMC_UniversalStatusBit_Initializing = 0x00000800
    TLMC_UniversalStatusBit_Tracking = 0x00001000
    TLMC_UniversalStatusBit_Settled = 0x00002000
    TLMC_UniversalStatusBit_PositionError = 0x00004000
    TLMC_UniversalStatusBit_InstrumentError = 0x00008000
    TLMC_UniversalStatusBit_Interlock = 0x00010000
    TLMC_UniversalStatusBit_Overtemperature = 0x00020000
    TLMC_UniversalStatusBit_BusVoltageFault = 0x00040000
    TLMC_UniversalStatusBit_CommutationError = 0x00080000
    TLMC_UniversalStatusBit_DigitalInput1 = 0x00100000
    TLMC_UniversalStatusBit_DigitalInput2 = 0x00200000
    TLMC_UniversalStatusBit_DigitalInput3 = 0x00400000
    TLMC_UniversalStatusBit_DigitalInput4 = 0x00800000
    TLMC_UniversalStatusBit_Overload = 0x01000000
    TLMC_UniversalStatusBit_EncoderFault = 0x02000000
    TLMC_UniversalStatusBit_Overcurrent = 0x04000000
    TLMC_UniversalStatusBit_BusCurrentFault = 0x08000000
    TLMC_UniversalStatusBit_PowerOk = 0x10000000
    TLMC_UniversalStatusBit_Active = 0x20000000
    TLMC_UniversalStatusBit_Error = 0x40000000
    TLMC_UniversalStatusBit_Enabled = 0x80000000

class TLMC_ValueType(IntEnum):
    TLMC_ValueType_int64 = 0
    TLMC_ValueType_bool = 1
    TLMC_ValueType_string = 2

class TLMC_Wait(IntEnum):
    TLMC_NoWait = 0
    TLMC_InfiniteWait = -1
    TLMC_Unused = 0

# ----------------
#  Unions/Structs
# ----------------

class TLMC_Value(Union):
    _pack_ = 1
    _fields_ = [
        ("int64Value", c_longlong),
        ("boolValue", c_bool),
        ("string", c_char * 24),
    ]

class TLMC_ApiVersion(Structure):
    _pack_ = 1
    _fields_ = [
        ("major", c_uint16),
        ("minor", c_uint16),
        ("patch", c_uint16),
        ("build", c_uint32),
        ("prereleaseLabel", c_char * 32),
        ("displayString", c_char * 64),
    ]

class TLMC_AdcInputs(Structure):
    _pack_ = 1
    _fields_ = [
        ("adcInput1", c_uint16),
        ("adcInput2", c_uint16),
    ]

class TLMC_AnalogMonitorConfigurationParams(Structure):
    _pack_ = 1
    _fields_ = [
        ("motorChannel", c_uint16),
        ("systemVariable", c_uint16),
        ("scale", c_int32),
        ("offset", c_int32),
    ]

class TLMC_AnalogMonitorConfigurationParamsChangedNotificationData(Structure):
    _pack_ = 1
    _fields_ = [("monitorNumber", c_uint16)]

class TLMC_AuxIoPortModeChangedNotificationData(Structure):
    _pack_ = 1
    _fields_ = [("portNumber", c_uint16)]

class TLMC_ConnectedProductInfo(Structure):
    _pack_ = 1
    _fields_ = [
        ("productName", c_char * 64),
        ("partNumber", c_char * 16),
        ("axisType", c_uint16),
        ("movementType", c_uint16),
        ("unitType", c_uint16),
        ("distanceScaleFactor", c_double),
        ("velocityScaleFactor", c_double),
        ("accelerationScaleFactor", c_double),
        ("minPosition", c_double),
        ("maxPosition", c_double),
        ("maxVelocity", c_double),
        ("maxAcceleration", c_double),
    ]

class TLMC_CurrentLoopParams(Structure):
    _pack_ = 1
    _fields_ = [
        ("phase", c_uint16),
        ("proportional", c_uint16),
        ("integral", c_uint16),
        ("integralLimit", c_uint16),
        ("integralDeadBand", c_uint16),
        ("feedForward", c_uint16),
    ]

class TLMC_CurrentLoopParamsChangedNotificationData(Structure):
    _pack_ = 1
    _fields_ = [("scenario", c_uint16)]

class TLMC_DcPidParams(Structure):
    _pack_ = 1
    _fields_ = [
        ("proportional", c_uint32),
        ("integral", c_uint32),
        ("derivative", c_uint32),
        ("integralLimit", c_uint32),
        ("filterControl", c_uint16),
    ]

class TLMC_FirmwareVersion(Structure):
    _pack_ = 1
    _fields_ = [
        ("minorVersion", c_uint8),
        ("interimVersion", c_uint8),
        ("majorVersion", c_uint8),
        ("reserved", c_uint8),
    ]

class TLMC_DeviceInfo(Structure):
    _pack_ = 1
    _fields_ = [
        ("deviceFamily", c_uint8),
        ("deviceType", c_uint32),
        ("partNumber", c_char * 8),
        ("device", c_char * 64),
        ("transport", c_char * 128),
        ("parentDevice", c_char * 64),
        ("deviceTypeDescription", c_char * 256),
    ]

class TLMC_GeneralMoveParams(Structure):
    _pack_ = 1
    _fields_ = [("backlashDistance", c_int32)]

class TLMC_HardwareInfo(Structure):
    _pack_ = 1
    _fields_ = [
        ("serialNumber", c_uint32),
        ("partNumber", c_char * 8),
        ("type", c_uint16),
        ("firmwareVersion", TLMC_FirmwareVersion),  # corrected
        ("notes", c_char * 48),
        ("deviceDependantData", c_char * 12),
        ("hardwareVersion", c_uint16),
        ("modificationState", c_uint16),
        ("numChannels", c_uint16),
    ]

class TLMC_HomeParams(Structure):
    _pack_ = 1
    _fields_ = [
        ("direction", c_uint16),
        ("limitSwitch", c_uint16),
        ("velocity", c_uint32),
        ("offsetDistance", c_int32),
    ]

class TLMC_IoConfigurationParams(Structure):
    _pack_ = 1
    _fields_ = [
        ("mode", c_uint16),
        ("triggerOutSource", c_uint16),
    ]

class TLMC_IoConfigurationParamsChangedNotificationData(Structure):
    _pack_ = 1
    _fields_ = [("portNumber", c_uint16)]

class TLMC_IoTriggerParams(Structure):
    _pack_ = 1
    _fields_ = [
        ("triggerInMode", c_uint16),
        ("triggerInPolarity", c_uint16),
        ("triggerInSource", c_uint16),
        ("triggerOutMode", c_uint16),
        ("triggerOutPolarity", c_uint16),
        ("triggerOutForwardStartPosition", c_int32),
        ("triggerOutForwardInterval", c_int32),
        ("triggerOutForwardNumberOfPulses", c_int32),
        ("triggerOutReverseStartPosition", c_int32),
        ("triggerOutReverseInterval", c_int32),
        ("triggerOutReverseNumberOfPulses", c_int32),
        ("triggerOutPulseWidth", c_uint32),
        ("triggerOutNumberOfCycles", c_uint32),
        ("reserved", c_int8 * 8),
    ]

class TLMC_JogParams(Structure):
    _pack_ = 1
    _fields_ = [
        ("mode", c_uint16),
        ("stepSize", c_int32),
        ("minVelocity", c_uint32),
        ("acceleration", c_uint32),
        ("maxVelocity", c_uint32),
        ("stopMode", c_uint16),
    ]

class TLMC_JoystickParams(Structure):
    _pack_ = 1
    _fields_ = [
        ("lowGearMaxVelocity", c_uint32),
        ("highGearMaxVelocity", c_uint32),
        ("lowGearAcceleration", c_uint32),
        ("highGearAcceleration", c_uint32),
        ("directionSense", c_uint16),
    ]

class TLMC_KcubeIoTriggerParams(Structure):
    _pack_ = 1
    _fields_ = [
        ("trigger1Mode", c_uint16),
        ("trigger1Polarity", c_uint16),
        ("trigger2Mode", c_uint16),
        ("trigger2Polarity", c_uint16),
        ("reserved", c_int8 * 12),
    ]

class TLMC_StepperLoopParams(Structure):
    _pack_ = 1
    _fields_ = [
        ("loopMode", c_uint16),
        ("proportional", c_int32),
        ("integral", c_int32),
        ("differential", c_int32),
        ("outputClip", c_int32),
        ("outputTolerance", c_int32),
        ("microstepsPerEncoderCount", c_uint32),
        ("reserved", c_uint8 * 8),
    ]

class TLMC_KcubeMmiParams(Structure):
    _pack_ = 1
    _fields_ = [
        ("joystickMode", c_uint16),
        ("joystickMaxVelocity", c_uint32),
        ("joystickAcceleration", c_uint32),
        ("joystickDirectionSense", c_uint16),
        ("presetPosition1", c_int32),
        ("presetPosition2", c_int32),
        ("displayBrightness", c_uint16),
        ("displayTimeout", c_uint16),
        ("displayDimLevel", c_uint16),
        ("presetPosition3", c_int32),
        ("joystickSensitivity", c_uint16),   # corrected spelling
        ("reserved", c_uint8 * 2),
    ]

class TLMC_KcubePositionTriggerParams(Structure):
    _pack_ = 1
    _fields_ = [
        ("forwardStartPosition", c_int32),
        ("forwardInterval", c_uint32),
        ("forwardNumberOfPulses", c_uint32),
        ("reverseStartPosition", c_int32),
        ("reverseInterval", c_uint32),
        ("reverseNumberOfPulses", c_uint32),
        ("pulseWidth", c_uint32),
        ("numberOfCycles", c_uint32),
        ("reserved", c_uint8 * 12),
    ]

class TLMC_LcdDisplayParams(Structure):
    _pack_ = 1
    _fields_ = [
        ("knobSensitivity", c_int16),
        ("displayBrightness", c_uint16),
        ("displayTimeout", c_uint16),
        ("displayDimLevel", c_uint16),
        ("reserved", c_uint8 * 20),
    ]

class TLMC_LcdMoveParams(Structure):
    _pack_ = 1
    _fields_ = [
        ("knobMode", c_uint16),
        ("jogStepSize", c_int32),
        ("acceleration", c_int32),
        ("maxVelocity", c_int32),
        ("jogStopMode", c_uint16),
        ("presetPosition", c_int32 * 3),
        ("reserved", c_uint8 * 20),
    ]

class TLMC_LimitSwitchParams(Structure):
    _pack_ = 1
    _fields_ = [
        ("clockwiseHardLimitOperatingMode", c_uint16),
        ("counterclockwiseHardLimitOperatingMode", c_uint16),
        ("clockwiseSoftLimit", c_int32),
        ("counterclockwiseSoftLimit", c_int32),
        ("softLimitOperatingMode", c_uint16),
    ]

class TLMC_MotorOutputParams(Structure):
    _pack_ = 1
    _fields_ = [
        ("continuousCurrentLimit", c_uint16),
        ("energyLimit", c_uint16),
        ("motorLimit", c_uint16),
        ("motorBias", c_uint16),
        ("reserved", c_int8 * 4),
    ]

class TLMC_MoveAbsoluteParams(Structure):
    _pack_ = 1
    _fields_ = [("absolutePosition", c_int32)]

class TLMC_MoveRelativeParams(Structure):
    _pack_ = 1
    _fields_ = [("relativeDistance", c_int32)]

class TLMC_Notification(Structure):
    _pack_ = 1
    _fields_ = [
        ("id", c_int32),
        ("data", c_size_t),         # uintptr_t
        ("dataLength", c_uint32),
    ]

class TLMC_PositionLoopParams(Structure):
    _pack_ = 1
    _fields_ = [
        ("proportional", c_uint16),
        ("integral", c_uint16),
        ("integralLimit", c_uint32),
        ("derivative", c_uint16),
        ("servoCycles", c_uint16),
        ("scale", c_uint16),
        ("velocityFeedForward", c_uint16),
        ("accelerationFeedForward", c_uint16),
        ("errorLimit", c_uint32),
    ]

class TLMC_PositionLoopParamsChangedNotificationData(Structure):
    _pack_ = 1
    _fields_ = [("scenario", c_uint16)]

class TLMC_PowerParams(Structure):
    _pack_ = 1
    _fields_ = [
        ("restFactor", c_uint16),
        ("moveFactor", c_uint16),
    ]

class TLMC_ProfiledModeParams(Structure):
    _pack_ = 1
    _fields_ = [
        ("mode", c_uint16),
        ("jerk", c_uint32),
        ("reserved", c_int8 * 4),
    ]

class TLMC_PZ_OutputWaveformParams(Structure):
    _pack_ = 1
    _fields_ = [
        ("mode", c_uint16),
        ("numberOfSamplesPerCycle", c_uint16),
        ("numberOfCycles", c_int32),
        ("interSampleDelay", c_int32),
        ("preCycleDelay", c_int32),
        ("postCycleDelay", c_int32),
        ("outputTriggerStartIndex", c_uint16),
        ("outputTriggerWidth", c_int32),
        ("numberOfSamplesBetweenTriggerRepetition", c_uint16),
    ]

class TLMC_PZ_OutputWaveformLookupTableSample(Structure):
    _pack_ = 1
    _fields_ = [
        ("index", c_uint16),
        ("voltage", c_int16),
    ]

class TLMC_PZ_MaxOutputVoltageParams(Structure):
    _pack_ = 1
    _fields_ = [
        ("maxOutputVoltage", c_uint16),
        ("voltageLimit", c_uint16),
    ]

class TLMC_PZ_OutputVoltageControlSourceParams(Structure):
    _pack_ = 1
    _fields_ = [("source", c_uint16)]

class TLMC_PZ_PositionLoopParams(Structure):
    _pack_ = 1
    _fields_ = [
        ("proportional", c_uint16),
        ("integral", c_uint16),
    ]

class TLMC_PZ_Status(Structure):
    _pack_ = 1
    _fields_ = [
        ("outputVoltage", c_int16),
        ("position", c_int16),
        ("statusBits", c_uint32),
    ]

class TLMC_PZ_SlewRateParams(Structure):
    _pack_ = 1
    _fields_ = [
        ("openLoopSlewRate", c_uint16),    # corrected name
        ("closedLoopSlewRate", c_uint16),
    ]

class TLMC_RichResponse(Structure):
    _pack_ = 1
    _fields_ = [
        ("messageId", c_uint16),
        ("code", c_uint16),
        ("notes", c_char * 64),
    ]

class TLMC_Response(Structure):
    _pack_ = 1
    _fields_ = [
        ("messageId", c_uint16),
        ("code", c_uint16),
    ]

class TLMC_Setting(Structure):
    _pack_ = 1
    _fields_ = [
        ("valueType", c_uint8),
        ("isValueSet", c_bool),
        ("value", TLMC_Value),              # union
        ("scaleType", c_uint16),
        ("unitType", c_uint16),
        ("name", c_char * 128),
        ("displayName", c_char * 128),
        ("isReadOnly", c_bool),
        ("hasDiscreteValues", c_bool),
        ("hasMin", c_bool),
        ("hasMax", c_bool),
        ("minValue", TLMC_Value),
        ("maxValue", TLMC_Value),
    ]

class TLMC_SettingItemChangedNotificationData(Structure):
    _pack_ = 1
    _fields_ = [("settingName", c_char * 128)]

class TLMC_StageAxisParams(Structure):
    _pack_ = 1
    _fields_ = [
        ("productId", c_uint16),        # corrected name (was typeId)
        ("axisId", c_uint16),
        ("partNumber", c_char * 16),
        ("serialNumber", c_uint32),
        ("countsPerUnit", c_uint32),
        ("minPosition", c_int32),
        ("maxPosition", c_int32),
        ("maxAcceleration", c_uint32),
        ("maxDeceleration", c_uint32),
        ("maxVelocity", c_uint32),
        ("gearboxRatio", c_uint16),     # corrected casing (was gearBoxRatio)
        ("reserved", c_uint8 * 22),
    ]

class TLMC_StatusItem(Structure):
    _pack_ = 1
    _fields_ = [
        ("id", c_int32),
        ("valueType", c_uint8),
        ("value", TLMC_Value),          # union
    ]

class TLMC_StatusItemChangedNotificationData(Structure):
    _pack_ = 1
    _fields_ = [
        ("count", c_uint16),
        ("ids", c_size_t),              # pointer in native; represent as uintptr_t
    ]

class TLMC_StepperStatus(Structure):
    _pack_ = 1
    _fields_ = [
        ("position", c_int32),
        ("encoderCount", c_int32),
        ("statusBits", c_uint32),       # corrected (was int32)
    ]

class TLMC_TrackSettleParams(Structure):
    _pack_ = 1
    _fields_ = [
        ("settleTime", c_uint16),
        ("settleWindow", c_uint16),
        ("trackWindow", c_uint16),
        ("reserved", c_uint8 * 4),
    ]

class TLMC_TriggerParamsForDcBrushless(Structure):
    _pack_ = 1
    _fields_ = [("modes", c_uint8)]

class TLMC_TriggerParamsForStepper(Structure):
    _pack_ = 1
    _fields_ = [("modes", c_uint8)]

class TLMC_UniversalStatus(Structure):
    _pack_ = 1
    _fields_ = [
        ("position", c_int32),
        ("velocity", c_int16),
        ("motorCurrent", c_int16),
        ("statusBits", c_uint32),
    ]

class TLMC_VelocityParams(Structure):
    _pack_ = 1
    _fields_ = [
        ("minVelocity", c_uint32),
        ("acceleration", c_uint32),
        ("maxVelocity", c_uint32),
    ]

# ---------------------------------------------------------------------
# Additions/aliases to align names used by the SDK and wrappers
# ---------------------------------------------------------------------

# End-of-move messages (not present originally; matches the header values)
from enum import IntEnum
class TLMC_EndOfMoveMessagesModes(IntEnum):
    TLMC_EndOfMoveMessagesMode_Enabled  = 0x01
    TLMC_EndOfMoveMessagesMode_Disabled = 0x02

# Plural aliases for enums defined with singular class names
TLMC_Units               = TLMC_Unit
TLMC_ScaleTypes          = TLMC_ScaleType
TLMC_LcdKnobModes        = TLMC_LcdKnobMode
TLMC_KcubeMmiLockStates  = TLMC_KcubeMmiLockState
TLMC_IoTriggerInModes    = TLMC_IoTriggerInMode
TLMC_IoTriggerOutModes   = TLMC_IoTriggerOutMode
TLMC_AuxIoPortModes      = TLMC_AuxIoPortMode
TLMC_IoPortModes         = TLMC_IoPortMode
TLMC_EnableStates        = TLMC_EnableState   # <-- fixes your current import error

# PZ enums – plural names expected by some modules
TLMC_PZ_OutputVoltageControlSources  = TLMC_PZ_OutputVoltageControlSource
TLMC_PZ_OutputWaveformOperatingModes = TLMC_PZ_OutputWaveformOperatingMode

# Stage enums – sometimes referenced with these names
TLMC_StageAxisIds     = TLMC_StageAxis_AxisId      # header: TLMC_StageAxisId
TLMC_StageProductIds  = TLMC_StageAxis_TypeId      # header: TLMC_StageProductId

# Profile mode params – your file defines TLMC_ProfiledModeParams (with 'd')
# but other modules import TLMC_ProfileModeParams
TLMC_ProfileModeParams = TLMC_ProfiledModeParams
