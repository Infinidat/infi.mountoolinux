from munch import Munch

class MountEntry(object):
    @classmethod
    def from_groupdict(cls, groupdict):
        return cls(**groupdict)

    def __init__(self, fsname, dirname, typename, opts=dict(), freq=0, passno=0, mountonboot="yes", createtime=0):
        self._bunch = Munch(fsname=fsname, dirname=dirname,
                          typename=typename, opts=opts,
                          freq=freq, passno=passno, mountonboot=mountonboot, createtime=createtime)

    def get_fsname(self):
        """:returns: name of mounted file system"""
        return self._bunch.fsname

    def get_dirname(self):
        """:returns: file system path prefix"""
        return self._bunch.dirname.replace(r"\040", " ")  # HIP-688 spaces appear different in mtab

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
    
    def get_mountonboot(self):
        """:returns: should mount on boot"""
        return self._bunch.mountonboot

    def get_createtime(self):
        """:returns: creation time of mount"""
        return self._bunch.createtime

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
