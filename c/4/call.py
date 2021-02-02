from ctypes import cdll, c_int, POINTER, ARRAY, byref

LIB = cdll.LoadLibrary("x.so")

LIB.testDLL()

func = LIB.getResponse
itype = c_int
func.argtypes = [POINTER(ARRAY(itype,3))]
func.restype = c_int

chashes = (itype * 3)(*[0,1,2])
print(chashes)

func(byref(chashes))

print(chashes)
print(list(chashes))
