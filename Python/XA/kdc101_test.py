import time

from xa_sdk.products.kdc101 import KDC101  # type: ignore
from xa_sdk.shared.xa_error_factory import XADeviceException  # type: ignore
from xa_sdk.shared.tlmc_type_structures import *  # type: ignore
from xa_sdk.native_sdks.xa_sdk import XASDK  # type: ignore

XASDK.try_load_library("")
XASDK.startup("")

sn_number = "27007297"

device = KDC101(sn_number, "", TLMC_OperatingModes.Default)

# device.set_enable_state(TLMC_ChannelEnableStates.ChannelEnabled)

# device.home(TLMC_Wait.TLMC_InfiniteWait)

# print(device.get_connected_product_info())