from ..base.mounter import MounterMixin, execute_mount

class SolarisMounterMixin(MounterMixin):
    FSTAB_PATH = "/etc/vfstab"

    def _get_entry_format(self, entry):
        return entry.get_format_solaris()

    def mount_entry(self, entry):
        args = ["-F", entry.get_typename(), entry.get_fsname(), entry.get_dirname()]
        args.extend(self._format_options(entry))
        execute_mount(args)
