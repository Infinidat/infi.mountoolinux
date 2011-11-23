
from .show_mounts import MountRepositoryMixin, MountEntry
from .supported_file_systems import SupportedFileSystemsMixin
from .mounter import MounterMixin

class MountManagerBaseClass(object):
    pass

class MountManager(MountManagerBaseClass, MountRepositoryMixin, SupportedFileSystemsMixin, MounterMixin):
    pass

__all__ = ["MountManager", "MountEntry", ]
