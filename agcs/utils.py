import socket
import os
import pwd, grp
import random
from string import ascii_letters as _letters
from string import digits as _digits

__all__ = [
    'num_cpus', 'get_ip',
    'Puser', 'Pgroup',
]

def random_string(length=12, chars=_letters+_digits):
    return ''.join(
        random.choice(chars) for i in range(length)
    )

def num_cpus():
    return hasattr(os, 'sysconf') and (
        os.sysconf('SC_NPROCESSORS_ONLN')
    ) or 1


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


class Host(object):

    def __init__(self, ip=None):
        self._ip = ip and ip or get_ip()
        self._name, self._cnames, self._ips = (
            socket.gethostbyaddr(self._ip)
        )

    @property
    def cnames(self):
        return self._cnames

    @property
    def ips(self):
        return self._ips

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def ip(self):
        return self._ip

    @ip.setter
    def ip(self, addr):
        self._name =  socket.gethostbyaddr(addr)
        self._ip = addr


class Puser(object):

    def __init__(self, uid=None, name=None):
        if uid:
            self._pwd = pwd.getpwuid(uid)
        elif name:
            self._pwd = pwd.getpwnam(name)
        else:
            self._pwd = pwd.getpwuid(os.getuid())

    @property
    def name(self):
        return self._pwd.pw_name

    @property
    def id(self):
        return self._pwd.pw_uid

    @property
    def home(self):
        return self._pwd.pw_dir

    @property
    def shell(self):
        return self._pwd.pw_shell


class Pgroup:

    def __init__(self, gid=None, name=None):
        if gid:
            self._grp = grp.getgrgid(gid)
        elif name:
            self._grp = grp.getgrnam(name)
        else:
            self._grp = grp.getgrgid(os.getgid())

    @property
    def name(self):
        return self._grp.gr_name

    @property
    def id(self):
        return self._grp.gr_gid

    @property
    def mem(self):
        return self._grp.gr_mem
