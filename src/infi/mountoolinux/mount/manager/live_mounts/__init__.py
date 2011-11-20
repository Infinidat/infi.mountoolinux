from bunch import Bunch

class MountEntry(object):
    def __init__(self, fsname, dirname, typename, opts, freq, passno):
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

FSNAME_PATTERN = r"[a-zA-Z0-9=/_-]*"
DIRNAME_PATTERN = FSNAME_PATTERN
TYPNAME_PATTERN = r"[a-zA-Z0-9]*"
OPTS_PATTERN = r".*"
FREQ_PATTERN = r"\d*"
PASSNO_PATTERN = FREQ_PATTERN

MOUNT_ENTRY_PATTERN = r"^[^#]{fsname}\t{dirname}\t{typename}\t{opts}\t{freq}\t{passno}$"

