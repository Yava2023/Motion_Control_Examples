# xa_error_factory.py (patched)
from xa_sdk.shared.tlmc_type_structures import TLMC_ResultCodes


class XADeviceException(Exception):
    def __init__(self, message: str, error_code: int):
        super().__init__(message)
        self.error_code = int(error_code)

    def __str__(self):
        return f"{super().__str__()} (code={self.error_code})"


class XAErrorFactory:
    @staticmethod
    def convert_return(return_code: int):
        """
        Returns an Exception instance that you can raise, or None if success.

        Usage:
            if rc != TLMC_ResultCodes.Success:
                raise XAErrorFactory.convert_return(rc)
        """
        if int(return_code) == int(TLMC_ResultCodes.Success):
            return None

        messages = {
            TLMC_ResultCodes.FunctionNotSupported:           "Function not supported",
            TLMC_ResultCodes.DeviceNotFound:                 "Device not found",
            TLMC_ResultCodes.DeviceNotSupported:             "Device not supported",
            TLMC_ResultCodes.Timeout:                        "Timeout",
            TLMC_ResultCodes.Fail:                           "Operation failed",
            TLMC_ResultCodes.InsufficientFirmware:           "Device firmware is too old",
            TLMC_ResultCodes.AlreadyStarted:                 "Already started",
            TLMC_ResultCodes.StartRequired:                  "API startup required",
            TLMC_ResultCodes.AllocationError:                "Allocation error",
            TLMC_ResultCodes.InternalError:                  "Internal error",
            TLMC_ResultCodes.InvalidHandle:                  "Invalid handle",
            TLMC_ResultCodes.InvalidArgument:                "Invalid argument",
            TLMC_ResultCodes.ItemIsReadOnly:                 "Item is read-only",
            TLMC_ResultCodes.LoadParamsError:                "Load params error",
            TLMC_ResultCodes.TransportError:                 "Transport error",
            TLMC_ResultCodes.TransportClosed:                "Transport closed",
            TLMC_ResultCodes.TransportNotAvailable:          "Transport not available",
            TLMC_ResultCodes.SharingModeNotAvailable:        "Sharing mode not available",
            TLMC_ResultCodes.NotInitialized:                 "Not initialized",
            TLMC_ResultCodes.NoFreeHandles:                  "No free handles",
            TLMC_ResultCodes.VerificationFailure:            "Verification failure",
            TLMC_ResultCodes.DataNotLoaded:                  "Data not loaded",
            TLMC_ResultCodes.ConnectedProductNotSupported:   "Connected product not supported",
            TLMC_ResultCodes.SimulationCreationError:        "Simulation creation error",
            TLMC_ResultCodes.ConnectedProductNotSet:         "Connected product not set",
            # Missing before: defined in the header
            TLMC_ResultCodes.CalibrationFileNotPresent:      "Calibration file not present",
        }

        msg = messages.get(return_code, f"Unknown error (code={int(return_code)})")
        return XADeviceException(msg, return_code)