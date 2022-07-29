# This came from here:
# https://forum.micropython.org/viewtopic.php?f=18&t=7399

import io
import os
import machine

_MP_STREAM_POLL = const(3)
_MP_STREAM_POLL_RD = const(0x0001)

_timer = machine.Timer(-1)

# Simple buffering stream to support the dupterm requirements.
class InjectStream(io.IOBase):
    def __init__(self):
        self._data = bytearray()

    def inject(self, data):
        self._data += data

        # Needed for ESP32.
        if hasattr(os, 'dupterm_notify'):
            os.dupterm_notify(None)

    def readinto(self, buf):
        if not self._data:
            return None
        b = min(len(buf), len(self._data))
        buf[:b] = self._data[:b]
        self._data = self._data[b:]
        return b

    def read(self, sz=None):
        d = self._data
        self._data[:] = b''
        return d

    def ioctl(self, op, arg):
        if op == _MP_STREAM_POLL:
            if self._data:
                return _MP_STREAM_POLL_RD
        return 0

    def write(self, buf):
        pass

stream = InjectStream()
os.dupterm(stream)

# call this from your key handler (e.g. pin interrupt?)
# stream.inject('input to type')