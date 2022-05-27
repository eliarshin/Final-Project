import base64
import win32api
import win32con
import win32gui
import win32ui
'''
We will use windows graphics device interface to
activate the correct properties, screen size and etc.

'''
def get_dimensions(): # this function return us the siize of the desktop 
    width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
    height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
    left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
    top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)
    return (width, height, left, top)

def screenshot(name='screenshot'):
    hdesktop = win32gui.GetDesktopWindow() # handling the desktop screen window
    width, height, left, top = get_dimensions()
    desktop_device_content = win32gui.GetWindowDC(hdesktop) # creating device content # https://www.programcreek.com/python/example/89821/win32gui.GetWindowDC - titles, scroll menu etc
    img_device_content = win32ui.CreateDCFromHandle(desktop_device_content) # create device content from what we hanlded before
    memory_device_content = img_device_content.CreateCompatibleDC() # create memory based on the device content we got - here we store untill we write the bitmap bytes to file
    screenshot = win32ui.CreateBitmap() # define bitmap object
    screenshot.CreateCompatibleBitmap(img_device_content, width, height)
    memory_device_content.SelectObject(screenshot)

    memory_device_content.BitBlt((0,0), (width, height),
    img_device_content, (left, top), win32con.SRCCOPY) # we copy every bit to memory based content like memcpy
    screenshot.SaveBitmapFile(memory_device_content, f'{name}.bmp') # save the content we bitmapped as file
    memory_device_content.DeleteDC()
    win32gui.DeleteObject(screenshot.GetHandle())



def run():
    screenshot()
    with open('screenshot.bmp') as f:
        img = f.read()
    return img

if __name__ == '__main__':
    screenshot()