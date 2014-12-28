
import platform
from .show_mounts import MountEntry
from .supported_file_systems import SupportedFileSystemsMixin
from .mounter import MounterMixin

if platform.system().lower() == 'sunos':
	from .show_mounts import SolarisMountRepositoryMixin as OSMountRepositoryMixin
	from .mounter import SolarisMounterMixin as OSMounterMixin
else:
	from .show_mounts import LinuxMountRepositoryMixin as OSMountRepositoryMixin
	from .mounter import LinuxMounterMixin as OSMounterMixin

class MountManagerBaseClass(object):
    pass

class MountManager(MountManagerBaseClass, OSMountRepositoryMixin, SupportedFileSystemsMixin, OSMounterMixin):
    pass

__all__ = ["MountManager", "MountEntry", ]
