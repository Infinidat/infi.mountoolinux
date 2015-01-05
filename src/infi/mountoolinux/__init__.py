__import__("pkg_resources").declare_namespace(__name__)

__all__ = ['get_mount_manager']

from logging import getLogger
from infi.exceptools import chain
from infi.os_info import get_platform_string
from infi.pyutils.lazy import cached_function

logger = getLogger(__name__)

def _get_platform_specific_mountmanager_class():
    from .base import MountManager as PlatformMountManager
    from brownie.importing import import_string
    plat = get_platform_string().split('-')[0]
    platform_module_string = "{}.{}".format(__name__, plat)
    platform_module = import_string(platform_module_string)
    try:
        PlatformMountManager = getattr(platform_module, "{}MountManager".format(plat.capitalize()))
    except AttributeError:
        msg = "Failed to import platform-specific mount manager"
        logger.exception(msg)
        raise chain(ImportError(msg))
    return PlatformMountManager

@cached_function
def get_mount_manager():
    """returns a global instance of a `infi.mount_utils.base.MountManager`. """
    return _get_platform_specific_mountmanager_class()()
