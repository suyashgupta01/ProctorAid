import ctypes

def lock_pc():
    ctypes.windll.user32.LockWorkStation()