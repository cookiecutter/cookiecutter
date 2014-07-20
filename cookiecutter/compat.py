import platform

PLATFORM = platform.system().lower()

OSX = 'darwin' in PLATFORM

# See http://stackoverflow.com/questions/1387222/reliably-detect-windows-in-python/1387228#1387228
# 	another option is to use all(platform.win32_ver())
# 	per http://bugs.python.org/issue19143
WINDOWS = not OSX and 'win' in PLATFORM