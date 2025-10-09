from xa_sdk.native_sdks.xa_sdk import XASDK # type: ignore
from xa_sdk.products.kdc101 import KDC101  # type: ignore

# 1) Load the DLL from its folder once at startup (if needed):
XASDK.try_load_library("")

# 2) Startup the API:
XASDK.startup(None)

# 3) Open your device (example)
k = KDC101(device="12345678", transport="usb", operating_mode=0)

# 4) Identify (LED flash), then close
k.identify()
k.close()

# 5) Shutdown the API when your app exits
XASDK.shutdown()