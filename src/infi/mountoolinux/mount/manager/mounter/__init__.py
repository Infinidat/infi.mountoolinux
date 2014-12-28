from infi.mountoolinux.mount.errors import MountException
from infi.exceptools import chain

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

from infi.pyutils.contexts import contextmanager

class MounterMixin(object):
    FSTAB_PATH = "/etc/fstab"

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

    @contextmanager
    def _get_fstab_context(self, mode='a'):
        with open("/etc/fstab", mode) as fd:
            yield fd

    def _read_fstab(self):
        with open("/etc/fstab", 'r') as fd:
            return fd.read()

    def _get_entry_format(self, entry):
        raise NotImplementedError

    def mount_entry(self, entry):
        raise NotImplementedError

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

class LinuxMounterMixin(MounterMixin):
    def _get_entry_format(self, entry):
        return entry.get_format_linux()

    def mount_entry(self, entry):
        args = ["-t", entry.get_typename(), entry.get_fsname(), entry.get_dirname()]
        args.extend(self._format_options(entry))
        execute_mount(args)

class SolarisMounterMixin(MounterMixin):
    FSTAB_PATH = "/etc/vfstab"

    def _get_entry_format(self, entry):
        return entry.get_format_solaris()

    def mount_entry(self, entry):
        args = ["-F", entry.get_typename(), entry.get_fsname(), entry.get_dirname()]
        args.extend(self._format_options(entry))
        execute_mount(args)
