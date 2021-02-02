from ctypes import *
x = CDLL('x.so')
x.read.argtypes = POINTER(c_int16),c_size_t
x.read.restype = None
p = (c_int16*5)()
x.read(p,len(p))
print(list(p))

