from ctypes import CDLL, create_string_buffer
from ..base.supported_fs import SupportedFileSystemsMixin

LIBC_SO_NAME = "libc.so"
SYSFC_GET_NAME_OPCODE = 2
SYSFC_COUNT_OPCODE = 3
SYSFC_NAME_SIZE = 20

CREATABLE_FS = ["ufs", "zfs", "fat", "fat32", "vfat"]

class SolarisSupportedFileSystemsMixin(SupportedFileSystemsMixin):
    def get_supported_file_systems(self):
        """:returns: a list of mountable filesystems on this host
        :rtype: a list of strings"""
        result = set()
        for name in self._get_filesystem_names_from_libc() + \
                    self._get_list_of_supported_file_systems_by_helpers():
            result.add(name)
        return [name for name in result]

    def get_creatable_file_systems(self):
        supported_fs = self.get_supported_file_systems()
        result = []
        for fs in CREATABLE_FS:
            if fs in supported_fs:
                result.append(fs)
        return result

    def _get_filesystem_names_from_libc(self):
        libc = CDLL(LIBC_SO_NAME)
        fscount = libc.sysfs(SYSFC_COUNT_OPCODE)
        fsname = create_string_buffer(SYSFC_NAME_SIZE)
        result = []
        for i in xrange(1, fscount + 1):
            if not (libc.sysfs(SYSFC_GET_NAME_OPCODE, i, fsname) == -1 or fsname.value == ''):
                result.append(fsname.value)
        return result

    def _get_list_of_supported_file_systems_by_helpers(self):
        from glob import glob
        basedir = "/usr/lib/fs"
        replace_string = "{}/".format(basedir)
        return map(lambda path: path.replace(replace_string, ""),
                   glob("{}*".format(replace_string)))
