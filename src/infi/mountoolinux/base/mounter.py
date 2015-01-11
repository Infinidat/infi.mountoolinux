from ..exceptions import MountException
from infi.exceptools import chain
from infi.pyutils.contexts import contextmanager

def execute(commandname, args):
    from logging import getLogger
    log = getLogger()
    debug = log.debug

    from infi.execute import execute as _execute
    debug('executing {} {}'.format(commandname, ' '.join(args)))
    subprocess = _execute([commandname] + args)
    debug('waiting for it')
    subprocess.wait()
    debug('returncode = %s', subprocess.get_returncode())
    debug('stdout = %s', subprocess.get_stdout())
    debug('stderr = %s', subprocess.get_stderr())
    if subprocess.get_returncode() != 0:
        raise chain(MountException(subprocess.get_returncode()))

def execute_mount(args):
    execute("mount", args)

def execute_umount(args):
    execute("umount", args)

class MounterMixin(object):
    def _format_options(self, entry):
        if entry.get_opts().keys() == []:
            return []
        options = ''
        for key, value in entry.get_opts().items():
            if value is True:
                options += "{},".format(key)
            else:
                options += "{}={},".format(key, value)
        return ["-o", options.strip(',')]

    def _get_fstab_path(self):
        return "/etc/fstab"

    @contextmanager
    def _get_fstab_context(self, mode='a'):
        from os.path import exists
        if not exists(self._get_fstab_path()):
            raise IOError()
        with open(self._get_fstab_path(), mode) as fd:
            yield fd

    def _read_fstab(self):
        with open(self._get_fstab_path(), 'r') as fd:
            return fd.read()

    def _get_entry_format(self, entry):
        raise NotImplementedError()

    def mount_entry(self, entry):
        raise NotImplementedError()

    def umount_entry(self, entry):
        args = [entry.get_dirname(), ]
        execute_umount(args)

    def add_entry_to_fstab(self, entry):
        with self._get_fstab_context() as fd:
            fd.write("{}\n".format(self._get_entry_format(entry)))

    def remove_entry_from_fstab(self, entry):
        content = self._read_fstab()
        line_to_remove = self._get_entry_format(entry).strip()
        with self._get_fstab_context('w') as fd:
            for line in [line.strip() for line in content.splitlines()]:
                if line_to_remove == line:
                    continue
                fd.write("{}\n".format(line))
