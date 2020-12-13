from ctypes import *

libLev = CDLL("./liblev.so")

libLev.connect() 

n = libLev.addNum(20,33)
print("add", n)

d = libLev.distance("niche", "chiens")
print("lev", d)

# libLev.lenchar.argtypes = [c_char_p] 
l = libLev.lenchar("coucou")
print("len", l)