import ctypes as ct
from coreir.base import CoreIRType
from coreir.lib import libcoreir_c
import coreir.module
import coreir.context

def make_cpath(self, path):
    arr_type = ct.c_char_p * len(path)
    carr = arr_type()
    for i in range(0, len(path)):
        carr[i] = ct.c_char_p(path[i].encode())

    return carr

def make_bool_arr(val):
    bool_arr_t = ct.c_bool * len(val)
    bool_arr = bool_arr_t()
    for i in range(0, len(val)):
        bool_arr[i] = ct.c_bool(val[i])

    return bool_arr

class CORESimulatorState(ct.Structure):
    pass

CORESimulatorState_p = ct.POINTER(CORESimulatorState)

class CORESimValue(ct.Structure):
    pass

CORESimValue_p = ct.POINTER(CORESimValue)

class SimulatorState(CoreIRType):
    def __init__(self, module):
        self.state = libcoreir_c.CORENewSimulatorState(module)

    def get_value(self, path):
        cpath = make_cpath(path)
        val = libcoreir_c.CORESimGetValue(self.state, ct.byref(cpath[0]), len(cpath))
        val_len = libcoreir_c.CORESimValueGetLength(val)
        return [libcoreir_c.CORESimValueGetBit(val, i).value for i in range(0, val)]

    def set_value(self, path, new_val):
        cpath = make_cpath(path)
        bool_arr = make_bool_arr(new_val)
        
        libcoreir_c.CORESimSetValue(self.state, ct.byref(cpath), len(cpath), ct.byref(bool_arr))
    
    def step(self):
        libcoreir_c.CORESimStepMainClock(self.state)

    def run(self):
        libcoreir_c.CORESimRun(self.state)

    def execute(self):
        libcoreir_c.CORESimExecute(self.state)

    def rewind(self, num_halfsteps):
        return libcoreir_c.CORESimRewind(self.state, ct.c_int(num_halfsteps)).value

    def set_watchpoint(self, path, val):
        cpath = make_cpath(path)
        bool_arr = make_bool_arr(val)
        libcoreir_c.CORESimSetWatchPoint(self.state, ct.byref(cpath), len(cpath), ct.byref(bool_arr))
