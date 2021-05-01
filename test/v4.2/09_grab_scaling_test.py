from win32api import GetSystemMetrics
import ctypes


def get_monitor_scaling():
    user32 = ctypes.windll.user32
    w_orig = GetSystemMetrics(0)
    user32.SetProcessDPIAware()
    [w, h] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]
    return float(("{:.2f}".format(w/w_orig)))


print("Scaling of this monitor is {}".format(get_monitor_scaling()))
