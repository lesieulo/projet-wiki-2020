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
