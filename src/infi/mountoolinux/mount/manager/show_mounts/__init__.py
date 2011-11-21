from bunch import Bunch
from re import compile, MULTILINE

from logging import getLogger
log = getLogger()

class MountEntry(object):
    @classmethod
    def from_groupdict(cls, groupdict):
        return cls(**groupdict)

    def __init__(self, fsname, dirname, typename, opts=dict(), freq=0, passno=0):
        self._bunch = Bunch(fsname=fsname, dirname=dirname,
                          typename=typename, opts=opts,
                          freq=freq, passno=passno)

    def get_fsname(self):
        """:returns: name of mounted file system"""
        return self._bunch.fsname

    def get_dirname(self):
        """:returns: file system path prefix"""
        return self._bunch.dirname

    def get_typename(self):
        """:returns: mount type"""
        return self._bunch.typename

    def get_opts(self):
        """:returns: mount options"""
        return self._bunch.opts

    def get_freq(self):
        """:returns: dump frequency in days"""
        return self._bunch.freq

    def get_passno(self):
        """:returns: pass number on parallel fsck"""
        return self._bunch.passno

class MountRepositoryMixin(object):
    def _read_file(self, path):
        from os.path import exists
        if not exists(path):
            return ''
        with open(path) as fd:
            return fd.read()

    def _read_fstab(self):
        return self._read_file("/etc/fstab")

    def _read_mtab_from_proc(self):
        return self._read_file("/etc/mtab")

    def _translate_value(self, value):
        if value is None:
            return True
        if value.isdigit():
            return int(value)
        return value

    def _parse_options_in_entries(self, entries):
        pattern = compile(OPTION_PATTERN)
        for entry in entries:
            string = entry["opts"]
            results = {}
            for match in pattern.finditer(string):
                key = match.groupdict().get("key")
                value = match.groupdict().get("value")
                results[key] = self._translate_value(value)
            entry["opts"] = results
        return entries

    def _get_list_of_groupdicts_from_mtab(self):
        pattern = compile(MOUNT_ENTRY_PATTERN, MULTILINE)
        string = self._read_mtab_from_proc()
        log.debug("mtab content = \n{}".format(string))
        results = [match.groupdict() for match in pattern.finditer(string)]
        return self._parse_options_in_entries(results)

    def get_mounts_from_mtab(self):
        return [MountEntry.from_groupdict(groupdict) for groupdict in self._get_list_of_groupdicts_from_mtab()]

    def _get_list_of_groupdicts_from_fstab(self):
        pattern = compile(MOUNT_ENTRY_PATTERN, MULTILINE)
        string = self._read_fstab()
        log.debug("fstab content = \n{}".format(string))
        results = [match.groupdict() for match in pattern.finditer(string)]
        return self._parse_options_in_entries(results)

    def get_mounts_from_fstab(self):
        return [MountEntry.from_groupdict(groupdict) for groupdict in self._get_list_of_groupdicts_from_fstab()]

    def is_path_mounted(self, dirname):
        return any(item.get_dirname() == dirname for item in self.get_mounts_from_mtab())

    def is_fs_mounted(self, fsname):
        return any(item.get_fsname() == fsname for item in self.get_mounts_from_mtab())

    def is_entry_in_fstab(self, entry):
        for item in self.get_mounts_from_fstab():
            if item.get_fsname() == entry.get_fsname() and item.get_dirname() == entry.get_dirname():
                return True
        return False

FSNAME_PATTERN = r"(?P<fsname>[a-zA-Z0-9=/_\-@:\.]+)"
DIRNAME_PATTERN = r"(?P<dirname>[a-zA-Z0-9=/_\-]+)"
TYPNAME_PATTERN = r"(?P<typename>[a-zA-Z0-9_\.]+)"
STRING_PATTERN = r"[a-zA-Z0-9_\-]+"
OPTION_PATTERN = r"(?P<key>{})(?:=(?P<value>{}))?".format(STRING_PATTERN, STRING_PATTERN)
OPTS_PATTERN = r"(?P<opts>[a-zA-Z0-9_\-=,\.]+)"
FREQ_PATTERN = r"(?P<freq>\d*)"
PASSNO_PATTERN = r"(?P<passno>\d*)"

DELIMITER = r"[ \t]+"

ENTRY_PATTERN = r"^{fsname}{delimiter}{dirname}{delimiter}{typename}{delimiter}{opts}{delimiter}{freq}{delimiter}{passno}$"
MOUNT_ENTRY_PATTERN = ENTRY_PATTERN.format(delimiter=DELIMITER,
                                           fsname=FSNAME_PATTERN,
                                           dirname=DIRNAME_PATTERN,
                                           typename=TYPNAME_PATTERN,
                                           opts=OPTS_PATTERN,
                                           freq=FREQ_PATTERN,
                                           passno=PASSNO_PATTERN)
