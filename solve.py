from qiling.const import QL_VERBOSE
from qiling.os.mapper import QlFsMappedObject
from qiling import *
import os


def level1(ql):
    ql.mem.map(0x1000, 0x1000) #hex(0x1337//4096*4096)
    ql.mem.write(0x1337, ql.pack16(1337))

def uname_syscall(ql, address, *args, **kw):
    buf = b'QilingOS'.ljust(65, b'\x00')
    buf += b'qiling'.ljust(65, b'\x00')
    buf += b'99.0'.ljust(65, b'\x00')
    buf += b'ChallengeStart'.ljust(65, b'\x00')
    buf += b'ql'.ljust(65, b'\x00')
    buf += b'alsk'.ljust(65, b'\x00')
    ql.mem.write(address, buf)
    regreturn = 0
    return regreturn

def level2(ql):
    ql.set_syscall("uname", uname_syscall)

#https://hackmd.io/@ziqiaokong/BkbGuCJND

class Fake_urandom(QlFsMappedObject):
    def read(self, size):
        if size == 1:
            return b"\xff"
        else:
            return b"\x00" * size

    def fstat(self): # syscall fstat will ignore it if return -1
        return -1

    def close(self):
        return 0

#ssize_t getrandom(void *buf, size_t buflen, unsigned int flags);

def ql_syscall_getrandom(ql, buf, buflen, flags,*args, **kw):
    regreturn = None
    try:
        ql.mem.write(buf, b"\x00" * buflen)
        regreturn = len(data)
    except:
        regreturn = -1

def level3(ql):
    ql.add_fs_mapper("/dev/urandom", Fake_urandom())
    ql.set_syscall("getrandom", ql_syscall_getrandom)

def level4_sol(ql):
    ql.mem.write((ql.reg.rax), b'\x01')

def level4(ql):
    ql.hook_address(level4_sol, ql.base+0x154e40)

def my_rand(ql):
    ql.reg.rip += 2
    ql.reg.rax = 0

def level5(ql):
    ql.set_api('rand', my_rand)


ql = Qiling(["qilinglab-x86_64"], "rootfs/x8664_linux", verbose = QL_VERBOSE.OFF)
ql.base = 0x555555400000
level1(ql)
level2(ql)
level3(ql)
level4(ql)
level5(ql)

ql.run()
