
from ...errors import MountExceptionFactory

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
        raise MountExceptionFactory.create(subprocess.get_stderr())

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
                options += "{}{},".format(key, value)
        return ["-o", options.strip(',')]

    def mount_entry(self, entry):
        args = ["-t", entry.get_typename(), entry.get_fsname(), entry.get_fsname()]
        args.extend(self._format_options(entry))
        execute_mount(args)

    def umount_entry(self, entry):
        args = [entry.get_dirname(), ]
        execute_umount(args)

    def add_entry_to_fstab(self, entry):
        raise NotImplementedError()

    def remove_entry_from_fstab(self, entry):
        raise NotImplementedError()
