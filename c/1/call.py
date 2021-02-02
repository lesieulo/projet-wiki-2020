from ctypes import *

# gcc -shared -o liblev.so -fPIC lev.c

libLev = CDLL("./liblev.so")

libLev.connect() 

n = libLev.addNum(20,33)
print("add", n)

d = libLev.distance(b"niche", b"chiens")
print("lev", d)

l = libLev.lenchar(b"coucou")
print("len", l)

x = libLev.creer_tableau()
print(type(x), x)
g = (c_char*16).from_address(x)
print(type(g), g)




'''
import binascii
import numpy as np




dataSize = 32 * 32
#call the c function to get the data memory pointer
cMemoryPointer = x
newpnt = cast(cMemoryPointer, POINTER(c_ubyte))
# and construct an array using this data
DataBytes = np.ctypeslib.as_array(newpnt, (dataSize,)) #no internal copy
print("the mid byte of the data in python side is ", DataBytes[dataSize//2])
'''