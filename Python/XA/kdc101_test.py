import time

from xa_sdk.products.kdc101_simple import SimpleKDC101  # type: ignore

SimpleKDC101.initialize_sdk("")

sn_number_yaw = "27007297" #yaw
sn_number_pitch = "27271036"

yaw_device = SimpleKDC101(sn_number_yaw)
pitch_device = SimpleKDC101(sn_number_pitch)

#homing
yaw_device.home()
pitch_device.home()

#close connection
yaw_device.close()
pitch_device.close()

# close sdk
SimpleKDC101.shutdown_sdk()