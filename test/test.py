import ctypes #<3 ctypes
itte = ctypes.CDLL("./iTTE.so") #locate the library
func = itte.testbind_c
func(1000) #test functionality
