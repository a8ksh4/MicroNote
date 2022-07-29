
data = b''
# data = []

def clear():
    global data
    data = b''

def readinto(n=-1):
    return None

def write(b):
    global data
    data += b
    return len(b)