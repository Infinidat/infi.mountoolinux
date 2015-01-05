from ..base.mounter import MounterMixin, execute_mount

class LinuxMounterMixin(MounterMixin):
    def _get_entry_format(self, entry):
        return entry.get_format_linux()

    def mount_entry(self, entry):
        args = ["-t", entry.get_typename(), entry.get_fsname(), entry.get_dirname()]
        args.extend(self._format_options(entry))
        execute_mount(args)
