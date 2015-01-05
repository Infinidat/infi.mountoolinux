__import__("pkg_resources").declare_namespace(__name__)

import platform
from .mount import MountEntry, MountRepositoryMixin
from .supported_fs import SupportedFileSystemsMixin
from .mounter import MounterMixin

class MountManagerBaseClass(object):
    pass

class MountManager(MountManagerBaseClass, MountRepositoryMixin, SupportedFileSystemsMixin, MounterMixin):
    pass
