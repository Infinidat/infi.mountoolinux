__import__("pkg_resources").declare_namespace(__name__)

from ..base import MountManagerBaseClass

from .mount import SolarisMountRepositoryMixin
from .supported_fs import SolarisSupportedFileSystemsMixin
from .mounter import SolarisMounterMixin

class SolarisMountManager(MountManagerBaseClass, SolarisMountRepositoryMixin, SolarisSupportedFileSystemsMixin, SolarisMounterMixin):
    pass
