import ctypes as ct
from coreir.base import CoreIRType
from coreir.lib import libcoreir_sim_c
import coreir.module
import coreir.context

def make_charptr_arr(path):
    return (ct.c_char_p * len(path))(*(p.encode() for p in path))

def make_bool_arr(val):
    return (ct.c_bool * len(val))(*(ct.c_bool(v) for v in val))

class CORESimulatorState(ct.Structure):
    pass

CORESimulatorState_p = ct.POINTER(CORESimulatorState)

class CORESimValue(ct.Structure):
    pass

CORESimValue_p = ct.POINTER(CORESimValue)

class SimulatorState(CoreIRType):
    @staticmethod
    def make(module):
        state = libcoreir_sim_c.CORENewSimulatorState(module.ptr)
        return SimulatorState(state, module.context)

    def __init__(self, pointer, context):
        super().__init__(pointer, context)
        self.state = pointer

    def __del__(self):
        libcoreir_sim_c.COREDeleteSimulatorState(self.state)

    def reset_circuit(self):
        libcoreir_sim_c.CORESimResetCircuit(self.state)

    def get_value(self, inst_path, port_selects):
        cinst_path = make_charptr_arr(inst_path)
        cport_selects = make_charptr_arr(port_selects)
        val = libcoreir_sim_c.CORESimGetValueByOriginalName(self.state, cinst_path, len(cinst_path), cport_selects, len(cport_selects))
        val_len = libcoreir_sim_c.CORESimValueGetLength(val)
        return [libcoreir_sim_c.CORESimValueGetBit(val, i) for i in range(0, val_len)]

    def set_main_clock(self, path):
        cpath = make_charptr_arr(path)
        libcoreir_sim_c.CORESimSetMainClock(self.state, cpath, len(cpath))

    def set_clock_value(self, path, lastval, curval):
        cpath = make_charptr_arr(path)
        assert(isinstance(lastval, bool) and isinstance(curval, bool))
        libcoreir_sim_c.CORESimSetClock(self.state, cpath, len(cpath), lastval, curval)

    def get_clock_cycles(self, path):
        cpath = make_charptr_arr(path)
        return libcoreir_sim_c.CORESimGetClockCycles(self.state, cpath, len(cpath))

    def set_value(self, path, new_val):
        cpath = make_charptr_arr(path)
        if isinstance(new_val, bool) or new_val is 0 or new_val is 1:
            new_val = [new_val]
        bool_arr = make_bool_arr(new_val)

        libcoreir_sim_c.CORESimSetValue(self.state, cpath, len(cpath), bool_arr, len(new_val))

    def step(self):
        libcoreir_sim_c.CORESimStepMainClock(self.state)

    def run(self):
        libcoreir_sim_c.CORESimRun(self.state)

    def run_half_cycle(self):
        libcoreir_sim_c.CORESimRunHalfCycle(self.state)

    def execute(self):
        libcoreir_sim_c.CORESimExecute(self.state)

    def rewind(self, num_halfsteps):
        return libcoreir_sim_c.CORESimRewind(self.state, ct.c_int(num_halfsteps))

    def set_watchpoint(self, insts, ports, val):
        cinsts = make_charptr_arr(insts)
        cports = make_charptr_arr(ports)
        bool_arr = make_bool_arr(val)
        libcoreir_sim_c.CORESimSetWatchPointByOriginalName(self.state, cinsts, len(cinsts), cports, len(cports), bool_arr, len(val))

    def delete_watchpoint(self, insts, ports):
        cinsts = make_charptr_arr(insts)
        cports = make_charptr_arr(ports)
        libcoreir_sim_c.CORESimDeleteWatchPointByOriginalName(self.state, cinsts, len(cinsts), cports, len(cports))
