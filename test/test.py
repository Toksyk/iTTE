import ctypes
import os
import platform
from ctypes import get_last_error

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
lib_dir = os.path.join(parent_dir, "lib")
try:
    if platform.system() == "Windows":
        dll_path = os.path.join(lib_dir, "iTTE.dll")
        os.add_dll_directory(lib_dir)
        kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
        kernel32.SetDllDirectoryW(lib_dir)
        itte = ctypes.CDLL(dll_path)
    else:
        dll_path = os.path.join(lib_dir, "iTTE.so")
        os.environ['LD_LIBRARY_PATH'] = lib_dir
        itte = ctypes.CDLL(dll_path)
except Exception as e:
    error_code = get_last_error()
    print(f"Error loading DLL: {e}")
    print(f"Last Windows error code: {error_code}")

func = itte.testbind_c
func(1000) #test functionality