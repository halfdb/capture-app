import time
from ctypes import *

lib = CDLL('./ocr/ocr.so')

read = lib.read

lastResult = lib.lastResult
lastResult.restype = c_char_p

__all__ = ['read', 'lastResult']


if __name__ == '__main__':
    read(12, 3, 629, 31)
    time.sleep(1)
    print(lastResult())
