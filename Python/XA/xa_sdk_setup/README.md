# Thorlabs XA SDK Python Wrapper

This is the python wrapper for the thorlabs xa sdk. It uses the ctypes library to wrap around the native xa_native.dll. The python wrapper does NOT contain the DLL, the user will need to set up their environment so their application can find the DLL. This can be done using XASDK.try_load_library but other ways include adding the DLL to the working directory of the program or adding the DLL directory to the PATH environment variable (either manually or in python at runtime).
