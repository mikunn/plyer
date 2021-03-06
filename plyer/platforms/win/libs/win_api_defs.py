''' Defines ctypes windows api.
'''

__all__ = ('GUID', 'get_DLLVERSIONINFO', 'MAKEDLLVERULL',
           'get_NOTIFYICONDATAW', 'CreateWindowExW', 'WindowProc',
           'DefWindowProcW', 'get_WNDCLASSEXW', 'GetModuleHandleW',
           'RegisterClassExW', 'UpdateWindow', 'LoadImageW',
           'Shell_NotifyIconW', 'DestroyIcon', 'UnregisterClassW',
           'DestroyWindow', 'LoadIconW')

import ctypes
from ctypes import (Structure, windll, sizeof, byref, POINTER, memset,
                    WINFUNCTYPE)
from ctypes.wintypes import (DWORD, HICON, HWND, UINT, WCHAR, WORD, BYTE,
    LPCWSTR, LPWSTR, INT, LPVOID, HINSTANCE, HMENU, LPARAM, WPARAM,
    HBRUSH, HMODULE, ATOM, BOOL, HANDLE, LONG, HHOOK)
LRESULT = LPARAM
HRESULT = HANDLE
HCURSOR = HICON



class GUID(Structure):
    _fields_ = [
        ('Data1', DWORD),
        ('Data2', WORD),
        ('Data3', WORD),
        ('Data4', BYTE * 8)
    ]


class DLLVERSIONINFO(Structure):
    _fields_ = [
        ('cbSize', DWORD),
        ('dwMajorVersion', DWORD),
        ('dwMinorVersion', DWORD),
        ('dwBuildNumber', DWORD),
        ('dwPlatformID', DWORD),
    ]

def get_DLLVERSIONINFO(*largs):
    version_info = DLLVERSIONINFO(*largs)
    version_info.cbSize = sizeof(DLLVERSIONINFO)
    return version_info

def MAKEDLLVERULL(major, minor, build, sp):
    return (major << 48) | (minor << 32) | (build << 16) | sp


NOTIFYICONDATAW_fields = [
    ("cbSize", DWORD),
    ("hWnd", HWND),
    ("uID", UINT),
    ("uFlags", UINT),
    ("uCallbackMessage", UINT),
    ("hIcon", HICON),
    ("szTip", WCHAR * 128),
    ("dwState", DWORD),
    ("dwStateMask", DWORD),
    ("szInfo", WCHAR * 256),
    ("uVersion", UINT),
    ("szInfoTitle", WCHAR * 64),
    ("dwInfoFlags", DWORD),
    ("guidItem", GUID),
    ("hBalloonIcon", HICON),
]

class NOTIFYICONDATAW(Structure):
    _fields_ = NOTIFYICONDATAW_fields[:]


class NOTIFYICONDATAW_V3(Structure):
    _fields_ = NOTIFYICONDATAW_fields[:-1]


class NOTIFYICONDATAW_V2(Structure):
    _fields_ = NOTIFYICONDATAW_fields[:-2]


class NOTIFYICONDATAW_V1(Structure):
    _fields_ = NOTIFYICONDATAW_fields[:6]

NOTIFYICONDATA_V3_SIZE = sizeof(NOTIFYICONDATAW_V3)
NOTIFYICONDATA_V2_SIZE = sizeof(NOTIFYICONDATAW_V2)
NOTIFYICONDATA_V1_SIZE = sizeof(NOTIFYICONDATAW_V1)

def get_NOTIFYICONDATAW(*largs):
    notify_data = NOTIFYICONDATAW(*largs)

    # get shell32 version to find correct NOTIFYICONDATAW size
    DllGetVersion = windll.Shell32.DllGetVersion
    DllGetVersion.argtypes = [POINTER(DLLVERSIONINFO)]
    DllGetVersion.restype = HRESULT

    version = get_DLLVERSIONINFO()
    if DllGetVersion(version):
        raise Exception('Cannot get Windows version numbers.')
    v = MAKEDLLVERULL(version.dwMajorVersion, version.dwMinorVersion,
                      version.dwBuildNumber, version.dwPlatformID)

    # from the version info find the NOTIFYICONDATA size
    if v >= MAKEDLLVERULL(6, 0, 6, 0):
        notify_data.cbSize = sizeof(NOTIFYICONDATAW)
    elif v >= MAKEDLLVERULL(6, 0, 0, 0):
        notify_data.cbSize = NOTIFYICONDATA_V3_SIZE
    elif v >= MAKEDLLVERULL(5, 0, 0, 0):
        notify_data.cbSize = NOTIFYICONDATA_V2_SIZE
    else:
        notify_data.cbSize = NOTIFYICONDATA_V1_SIZE
    return notify_data


CreateWindowExW = windll.User32.CreateWindowExW
CreateWindowExW.argtypes = [DWORD, ATOM, LPCWSTR, DWORD, INT, INT, INT, INT,
                            HWND, HMENU, HINSTANCE, LPVOID]
CreateWindowExW.restype = HWND

GetModuleHandleW = windll.Kernel32.GetModuleHandleW
GetModuleHandleW.argtypes = [LPCWSTR]
GetModuleHandleW.restype = HMODULE

WindowProc = WINFUNCTYPE(LRESULT, HWND, UINT, WPARAM, LPARAM)
DefWindowProcW = windll.User32.DefWindowProcW
DefWindowProcW.argtypes = [HWND, UINT, WPARAM, LPARAM]
DefWindowProcW.restype = LRESULT


class WNDCLASSEXW(Structure):
    _fields_ = [
        ('cbSize', UINT),
        ('style', UINT),
        ('lpfnWndProc', WindowProc),
        ('cbClsExtra', INT),
        ('cbWndExtra', INT),
        ('hInstance', HINSTANCE),
        ('hIcon', HICON),
        ('hCursor', HCURSOR),
        ('hbrBackground', HBRUSH),
        ('lpszMenuName', LPCWSTR),
        ('lpszClassName', LPCWSTR),
        ('hIconSm', HICON),
    ]

def get_WNDCLASSEXW(*largs):
    wnd_class = WNDCLASSEXW(*largs)
    wnd_class.cbSize = sizeof(WNDCLASSEXW)
    return wnd_class

RegisterClassExW = windll.User32.RegisterClassExW
RegisterClassExW.argtypes = [POINTER(WNDCLASSEXW)]
RegisterClassExW.restype = ATOM

UpdateWindow = windll.User32.UpdateWindow
UpdateWindow.argtypes = [HWND]
UpdateWindow.restype = BOOL

LoadImageW = windll.User32.LoadImageW
LoadImageW.argtypes = [HINSTANCE, LPCWSTR, UINT, INT, INT, UINT]
LoadImageW.restype = HANDLE

Shell_NotifyIconW = windll.Shell32.Shell_NotifyIconW
Shell_NotifyIconW.argtypes = [DWORD, POINTER(NOTIFYICONDATAW)]
Shell_NotifyIconW.restype = BOOL

DestroyIcon = windll.User32.DestroyIcon
DestroyIcon.argtypes = [HICON]
DestroyIcon.restype = BOOL

UnregisterClassW = windll.User32.UnregisterClassW
UnregisterClassW.argtypes = [ATOM, HINSTANCE]
UnregisterClassW.restype = BOOL

DestroyWindow = windll.User32.DestroyWindow
DestroyWindow.argtypes = [HWND]
DestroyWindow.restype = BOOL

LoadIconW = windll.User32.LoadIconW
LoadIconW.argtypes = [HINSTANCE, LPCWSTR]
LoadIconW.restype = HICON
