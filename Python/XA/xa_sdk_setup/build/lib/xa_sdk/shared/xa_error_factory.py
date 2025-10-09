from xa_sdk.shared.tlmc_type_structures import TLMC_ResultCodes

class XADeviceException(Exception):
    def __init__(self, message, error_code):
        super().__init__(message)
        self.error_code = error_code

class XAErrorFactory:

    def __init__(self):
        pass

    @staticmethod
    def convert_return(return_code):
        ex = None
        match return_code:
            case TLMC_ResultCodes.Success:
                pass
            case TLMC_ResultCodes.FunctionNotSupported:
                ex = XADeviceException(
                    message="Function not supported, error code 1", error_code=return_code)
                pass
            case TLMC_ResultCodes.DeviceNotFound:
                ex = XADeviceException(
                    message="Device not found, error code 2", error_code=return_code)
                pass
            case TLMC_ResultCodes.DeviceNotSupported:
                ex = XADeviceException(
                    message="Device not supported, error code 3", error_code=return_code)
                pass
            case TLMC_ResultCodes.Timeout:
                ex = XADeviceException(
                    message="Timeout error, error code 4", error_code=return_code)
                pass
            case TLMC_ResultCodes.Fail:
                ex = XADeviceException(
                    message="Method failed, error code 5", error_code=return_code)
                pass
            
            case TLMC_ResultCodes.InsufficientFirmware:
                ex = XADeviceException(
                    message="Device firmware is to old, error code 6", error_code=return_code)
                pass
                
            case TLMC_ResultCodes.AlreadyStarted:
                ex = XADeviceException(
                    message="AlreadyStarted, error code 7", error_code=return_code)
                pass

            case TLMC_ResultCodes.StartRequired:
                ex = XADeviceException(
                    message="XA startup required, error code 8", error_code=return_code)
                pass

            case TLMC_ResultCodes.AllocationError:
                ex = XADeviceException(
                    message="Allocation error, error code 9", error_code=return_code)
                pass
            case TLMC_ResultCodes.InternalError:
                ex = XADeviceException(
                    message="Internal error detected, error code 10", error_code=return_code)
                pass
            case TLMC_ResultCodes.InvalidHandle:
                ex = XADeviceException(
                    message="Invalid Handle, error code 11", error_code=return_code)
                pass
            case TLMC_ResultCodes.InvalidArgument:
                ex = XADeviceException(
                    message="Invalid Argument, error code 12", error_code=return_code)
                pass
            case TLMC_ResultCodes.ItemIsReadOnly:
                ex = XADeviceException(
                    message="Item is Read Only, error code 13", error_code=return_code)
                pass
            
            case TLMC_ResultCodes.LoadParamsError:
                ex = XADeviceException(
                    message="Load params failed, error code 14", error_code=return_code)
                pass

            case TLMC_ResultCodes.TransportError:
                ex = XADeviceException(
                    message="Transport error, error code 15", error_code=return_code)
                pass

            case TLMC_ResultCodes.TransportClosed:
                ex = XADeviceException(
                    message="Transport is closed, error code 16", error_code=return_code)
                pass   

            case TLMC_ResultCodes.TransportNotAvailable:
                ex = XADeviceException(
                    message="Transport not available, error code 17", error_code=return_code)
                pass
                
            case TLMC_ResultCodes.SharingModeNotAvailable:
                ex = XADeviceException(
                    message="Sharing mode is not available, error code 18", error_code=return_code)
                pass
                
            case TLMC_ResultCodes.NotInitialized:
                ex = XADeviceException(
                    message="Device not initialized, error code 19", error_code=return_code)
                pass
            
            case TLMC_ResultCodes.NoFreeHandles:
                ex = XADeviceException(
                    message="No free handles available, error code 20", error_code=return_code)
                pass
            
            
            case TLMC_ResultCodes.VerificationFailure:
                ex = XADeviceException(
                    message="Verification failure, error code 21", error_code=return_code)
                pass
            
            case TLMC_ResultCodes.DataNotLoaded:
                ex = XADeviceException(
                    message="Data not loaded, error code 22", error_code=return_code)
                pass

            case TLMC_ResultCodes.ConnectedProductNotSupported:
                ex = XADeviceException(
                    message="Connected product not supported, error code 23", error_code=return_code)
                pass
            case TLMC_ResultCodes.SimulationCreationError:
                ex = XADeviceException(
                    message="Simulation failed to start, error code 24", error_code=return_code)
                pass
            case TLMC_ResultCodes.ConnectedProductNotSet:
                ex = XADeviceException(
                    message="Simulation failed to start, error code 25", error_code=return_code)
                pass
        return ex
