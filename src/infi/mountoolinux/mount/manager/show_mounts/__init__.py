from bunch import Bunch
import re

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

    def _str_options(self):
        if self.get_opts().keys() == []:
            return ''
        options = ''
        for key, value in self.get_opts().items():
            if value is True:
                options += "{},".format(key)
            else:
                options += "{}={},".format(key, value)
        return options.strip(',')

    def __str__(self):
        return "\t".join(str(item) for item in \
                         [self.get_fsname(), self.get_dirname(), self.get_typename(),
                         self._str_options(), self.get_freq(), self.get_passno()])

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

    def _parse_options_for_entry(self, entry):
        string = entry["opts"]
        results = {}
        pattern = re.compile(OPTION_PATTERN)
        for match in pattern.finditer(string):
            key = match.groupdict().get("key")
            value = match.groupdict().get("value")
            results[key] = self._translate_value(value)
        entry["opts"] = results

    def _parse_options_in_entries(self, entries):
        for entry in entries:
            self._parse_options_for_entry(entry)
        return entries

    def _get_list_of_groupdicts_from_mtab(self):
        pattern = re.compile(MOUNT_ENTRY_PATTERN, re.MULTILINE)
        string = self._read_mtab_from_proc()
        log.debug("mtab content = \n{}".format(string))
        results = [match.groupdict() for match in pattern.finditer(string)]
        return self._parse_options_in_entries(results)

    def get_mounts_from_mtab(self):
        return [MountEntry.from_groupdict(groupdict) for groupdict in self._get_list_of_groupdicts_from_mtab()]

    def _get_list_of_groupdicts_from_fstab(self):
        pattern = re.compile(MOUNT_ENTRY_PATTERN, re.MULTILINE)
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

WORD_PATTERN = r"[^# \t\n\r\f\v]+"
FSNAME_PATTERN = r"(?P<fsname>{})".format(WORD_PATTERN)
DIRNAME_PATTERN = r"(?P<dirname>{})".format(WORD_PATTERN)
TYPNAME_PATTERN = r"(?P<typename>{})".format(WORD_PATTERN)
STRING_PATTERN = r"[^,=# \t\n\r\f\v]+"
OPTION_PATTERN = r"(?P<key>{})(?:=(?P<value>{}))?".format(STRING_PATTERN, STRING_PATTERN)
OPTS_PATTERN = r"(?P<opts>{})".format(WORD_PATTERN)
FREQ_PATTERN = r"(?P<freq>\d*)"
PASSNO_PATTERN = r"(?P<passno>\d*)"

SEP = r"[ \t]+"

ENTRY_PATTERN = r"^{fsname}{sep}{dirname}{sep}{typename}{sep}{opts}{sep}{freq}{sep}{passno}$"
MOUNT_ENTRY_PATTERN = ENTRY_PATTERN.format(sep=SEP,
                                           fsname=FSNAME_PATTERN,
                                           dirname=DIRNAME_PATTERN,
                                           typename=TYPNAME_PATTERN,
                                           opts=OPTS_PATTERN,
                                           freq=FREQ_PATTERN,
                                           passno=PASSNO_PATTERN)
