from munch import Munch
from ...base.mount import MountEntry

class SolarisMountEntry(MountEntry):
    def __init__(self, fsname, dirname, typename, opts=dict(), freq=0, passno='-', mountonboot="yes", createtime=0):
        super(SolarisMountEntry, self).__init__(fsname, dirname, typename, opts, freq, passno, mountonboot, createtime)

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
        string_double_sep = "\t\t".join(str(item) for item in \
                        [self.get_fsname(), '-', self.get_dirname().replace("none", '-'), self.get_typename()])
        string_one_sep = "\t".join(str(item) for item in \
                        [self.get_passno(), self.get_mountonboot(), self._str_options().replace('', '-')])
        return "\t".join([string_double_sep, string_one_sep])
