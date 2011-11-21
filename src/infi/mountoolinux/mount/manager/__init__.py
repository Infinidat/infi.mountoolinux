
from .show_mounts import MountRepositoryMixin
from .supported_file_systems import SupportedFileSystemsMixin

class MountManagerBaseClass(object):
    pass

class MountManager(MountManagerBaseClass, MountRepositoryMixin, SupportedFileSystemsMixin):
    pass
