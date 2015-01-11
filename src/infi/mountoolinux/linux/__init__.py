__import__("pkg_resources").declare_namespace(__name__)

from ..base import MountManagerBaseClass

from .mount import LinuxMountRepositoryMixin
from .supported_fs import LinuxSupportedFileSystemsMixin
from .mounter import LinuxMounterMixin

class LinuxMountManager(MountManagerBaseClass, LinuxMountRepositoryMixin, LinuxSupportedFileSystemsMixin, LinuxMounterMixin):
    pass
