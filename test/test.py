#import ctypes
#import os
#import platform
#from ctypes import get_last_error
#
#parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#lib_dir = os.path.join(parent_dir, "lib")
#try:
#    if platform.system() == "Windows":
#        dll_path = os.path.join(lib_dir, "iTTE.dll")
#        os.add_dll_directory(lib_dir)
#        kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
#        kernel32.SetDllDirectoryW(lib_dir)
#        itte = ctypes.CDLL(dll_path)
#    else:
#        dll_path = os.path.join(lib_dir, "iTTE.so")
#        os.environ['LD_LIBRARY_PATH'] = lib_dir
#        itte = ctypes.CDLL(dll_path)
#except Exception as e:
#    error_code = get_last_error()
#    print(f"Error loading DLL: {e}")
#    print(f"Last Windows error code: {error_code}")
#
#func = itte.testbind_c
#func(1000) #test functionality
import ctypes # <3 ctypes

itte = ctypes.CDLL("./iTTE.so") # load the library (jest the dll loads static libraries too)

# testbind_c
func = itte.testbind_c
func.restype = None
func.argtypes = [ctypes.c_int]
func(1000) # test if connected, if this fails you can basically stop the rest of the code from executing

# Init
# args: int*, int*a
# returns: char**
Initialize = itte.Init_c
Initialize.restype = ctypes.POINTER(ctypes.POINTER(ctypes.c_char))
Initialize.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)]

rows = ctypes.c_int() # ################### INITIALIZE ENGINE ###################
cols = ctypes.c_int()
game_c_ptr = Initialize(ctypes.byref(rows), ctypes.byref(cols))

num_rows = rows.value
num_cols = cols.value

# remake the vector from main in here because ctypes suck and no stl types implementation
game = []
for i in range(num_rows):
    row_list = []
    for j in range(num_cols):
        # get each character and defrenence pointer
        # convert each byte to a character
        row_list.append(game_c_ptr[i][j].decode('ascii'))
    game.append(row_list)

# render
# args: char**, int, int
# returns: void
update = itte.render_c
update.restype = None
update.argtypes = [ctypes.POINTER(ctypes.POINTER(ctypes.c_char)), ctypes.c_int, ctypes.c_int]

# convert back to char** before calling
# might be not optimized, i could keep the original pointer but eh who cares :333
c_char = ctypes.c_char * num_cols
c_char_ptr = ctypes.POINTER(c_char)
c_rows = (c_char_ptr * num_rows)()

for i in range(num_rows):
    # remake the whole array
    char_row = c_char(*[ord(c) for c in game[i]])
    c_rows[i] = ctypes.cast(char_row, c_char_ptr)

# finally, render
update(ctypes.cast(c_rows, ctypes.POINTER(ctypes.POINTER(ctypes.c_char))), num_rows, num_cols)

# FREE NBA MEMORYBOY
end = itte.endscene_c
end.restype = None
end.argtypes = [ctypes.POINTER(ctypes.POINTER(ctypes.c_char)), ctypes.c_int]
end(game_c_ptr, num_rows)
