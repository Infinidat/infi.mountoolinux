import platform
import re
from munch import Munch
from ...base.mount import MountRepositoryMixin

from logging import getLogger
log = getLogger()

class LinuxMountRepositoryMixin(MountRepositoryMixin):
    def _read_fstab(self):
        return self._read_file("/etc/fstab")

    def _read_mtab(self):
        return self._read_file("/etc/mtab")

    def _parse_options_for_entry(self, entry):
        string = entry["opts"]
        results = {}
        pattern = re.compile(OPTION_PATTERN)
        for match in pattern.finditer(string):
            key = match.groupdict().get("key")
            value = match.groupdict().get("value")
            results[key] = self._translate_value(value)
        entry["opts"] = results

    def _get_list_of_groupdicts_from_mtab(self):
        pattern = re.compile(MOUNT_ENTRY_PATTERN_LINUX, re.MULTILINE)
        string = self._read_mtab()
        log.debug("mtab content = \n{}".format(string))
        results = [match.groupdict() for match in pattern.finditer(string)]
        return self._parse_options_in_entries(results)

    def _get_list_of_groupdicts_from_fstab(self):
        pattern = re.compile(MOUNT_ENTRY_PATTERN_LINUX, re.MULTILINE)
        string = self._read_fstab()
        log.debug("fstab content = \n{}".format(string))
        results = [match.groupdict() for match in pattern.finditer(string)]
        return self._parse_options_in_entries(results)


WORD_PATTERN = r"[^# \t\n\r\f\v]+"
FSNAME_PATTERN = r"(?P<fsname>{})".format(WORD_PATTERN)
DIRNAME_PATTERN = r"(?P<dirname>{})".format(WORD_PATTERN)
TYPNAME_PATTERN = r"(?P<typename>{})".format(WORD_PATTERN)
STRING_PATTERN = r"[^,=# \t\n\r\f\v]+"
OPTION_PATTERN = r"(?P<key>{})(?:=(?P<value>{}))?".format(STRING_PATTERN, STRING_PATTERN)
OPTS_PATTERN = r"(?P<opts>{})".format(WORD_PATTERN)
FREQ_PATTERN = r"(?P<freq>\d*)"
PASSNO_PATTERN = r"(?P<passno>[\-\d]*)"
SEP = r"[ \t]+"

MOUNT_ENTRY_PATTERN_LINUX = r"^{fsname}{sep}{dirname}{sep}{typename}{sep}{opts}{sep}{freq}{sep}{passno}$".format(
                                           sep=SEP,
                                           fsname=FSNAME_PATTERN,
                                           dirname=DIRNAME_PATTERN,
                                           typename=TYPNAME_PATTERN,
                                           opts=OPTS_PATTERN,
                                           freq=FREQ_PATTERN,
                                           passno=PASSNO_PATTERN)
