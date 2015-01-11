import platform
import re
from munch import Munch
from . import MountEntry

from logging import getLogger
log = getLogger()

class MountRepositoryMixin(object):
    def _get_mount_entry_class(self):
        return MountEntry

    def _read_file(self, path):
        from os.path import exists
        if not exists(path):
            return ''
        with open(path) as fd:
            return fd.read()

    def _translate_value(self, value):
        if value is None:
            return True
        if value.isdigit():
            return int(value)
        return value

    def _parse_options_for_entry(self, entry):
        raise NotImplementedError()

    def _parse_options_in_entries(self, entries):
        for entry in entries:
            self._parse_options_for_entry(entry)
        return entries

    def _get_list_of_groupdicts_from_mtab(self):
        raise NotImplementedError()

    def _get_list_of_groupdicts_from_fstab(self):
        raise NotImplementedError()

    def get_mounts_from_mtab(self):
        return [self._get_mount_entry_class().from_groupdict(groupdict) for groupdict in self._get_list_of_groupdicts_from_mtab()]

    def get_mounts_from_fstab(self):
        return [self._get_mount_entry_class().from_groupdict(groupdict) for groupdict in self._get_list_of_groupdicts_from_fstab()]

    def is_path_mounted(self, dirname):
        return any(item.get_dirname() == dirname for item in self.get_mounts_from_mtab())

    def is_fs_mounted(self, fsname):
        return any(item.get_fsname() == fsname for item in self.get_mounts_from_mtab())

    def is_entry_in_fstab(self, entry):
        for item in self.get_mounts_from_fstab():
            if item.get_fsname() == entry.get_fsname() and item.get_dirname() == entry.get_dirname():
                return True
        return False
