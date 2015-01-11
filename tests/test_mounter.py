from unittest import SkipTest
from infi import unittest
from contextlib import nested, contextmanager
from infi.mountoolinux.base import MountEntry
from mock import patch
from platform import platform

DISTRO_LIST = ["linux", "solaris"]
MOUNT_FS_FLAG = {
    "linux": "-t",
    "solaris": "-F"
}

def _get_mount_entry_for_os(distro):
    if distro == "linux":
        from infi.mountoolinux.linux.mount import LinuxMountEntry
        return LinuxMountEntry
    elif distro == "solaris":
        from infi.mountoolinux.solaris.mount import SolarisMountEntry
        return SolarisMountEntry

def _get_mounter_mixin_for_os(distro):
    if distro == "linux":
        from infi.mountoolinux.linux import LinuxMounterMixin
        return LinuxMounterMixin
    elif distro == "solaris":
        from infi.mountoolinux.solaris import SolarisMounterMixin
        return SolarisMounterMixin

def _get_mount_repository_mixin_for_os(distro):
    if distro == "linux":
        from infi.mountoolinux.linux.mount import LinuxMountRepositoryMixin
        return LinuxMountRepositoryMixin
    elif distro == "solaris":
        from infi.mountoolinux.solaris.mount import SolarisMountRepositoryMixin
        return SolarisMountRepositoryMixin

class MounterTestCase(unittest.TestCase):
    @contextmanager
    def patch_execute(self):
        from infi.mountoolinux.base import mounter
        with patch.object(mounter, "execute") as execute:
            yield execute

    @unittest.parameters.iterate("distro", DISTRO_LIST)
    def test_mount__without_options(self, distro):
        with self.patch_execute() as execute:
            entry = _get_mount_entry_for_os(distro)("foo" , "bar", "baz")
            _get_mounter_mixin_for_os(distro)().mount_entry(entry)
        execute.assert_called_once_with("mount", "{} baz foo bar".format(MOUNT_FS_FLAG[distro]).split())

    @unittest.parameters.iterate("distro", DISTRO_LIST)
    def test_umount(self, distro):
        with self.patch_execute() as execute:
            entry = _get_mount_entry_for_os(distro)("foo" , "bar", "baz")
            _get_mounter_mixin_for_os(distro)().umount_entry(entry)
        execute.assert_called_once_with("umount", "bar".split())

    @unittest.parameters.iterate("distro", DISTRO_LIST)
    def test_mount__with_options(self, distro):
        with self.patch_execute() as execute:
            entry = _get_mount_entry_for_os(distro)("foo" , "bar", "baz", {"rw":True, "relatime":True,
                                                      "size":"501668k",
                                                      "mode":755})
            _get_mounter_mixin_for_os(distro)().mount_entry(entry)
        execute.assert_called_once_with("mount", "{} baz foo bar -o relatime,rw,mode=755,size=501668k".format(MOUNT_FS_FLAG[distro]).split())

class MaintainingFSTabTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from platform import platform
        if not platform().lower() in ["solaris", "linux"]:
            raise SkipTest("This TestCase runs only on Linux and Solaris")

    def setUp(self):
        self._fstab = ''
        self._mount_entry = _get_mount_entry_for_os(platform().lower())
        self._mounter_mixin = _get_mounter_mixin_for_os(platform().lower())
        self._mount_repository_mixin = _get_mount_repository_mixin_for_os(platform().lower())

    @contextmanager
    def patch_fstab(self):
        with nested(patch.object(self._mount_repository_mixin, "_read_fstab"),
                    patch.object(self._mounter_mixin, "_read_fstab"),
                    patch.object(self._mounter_mixin, "_get_fstab_context")) as (mock1, mock2, mock3):
            def read_side_effect(*args, **kwargs):
                return self._fstab

            @contextmanager
            def write_side_effect(*argv, **kwargs):
                mode = argv[0] if argv is not () else 'a'
                _self = self
                if mode == 'w':
                    self._fstab = ''
                class MockFD(object):
                    def write(self, string):
                        _self._fstab += string

                yield MockFD()

            mock1.side_effect = read_side_effect
            mock2.side_effect = read_side_effect
            mock3.side_effect = write_side_effect
            yield

    def test_add_entry_to_fstab(self):
        with self.patch_fstab():
            entry = self._mount_entry("foo" , "bar", "baz", {"rw":True, "relatime":True,
                                                      "size":"501668k",
                                                      "mode":755})
            self.assertFalse(self._mount_repository_mixin().is_entry_in_fstab(entry))
            self._mounter_mixin().add_entry_to_fstab(entry)
            self.assertTrue(self._mount_repository_mixin().is_entry_in_fstab(entry))

    def test_remove_entry_from_fstab(self):
        with self.patch_fstab():
            entry = MountEntry("foo" , "bar", "baz", {"rw":True, "relatime":True,
                                                      "size":"501668k",
                                                      "mode":755})
            second_entry = MountEntry("foo1" , "bar1", "baz1", {"rw":True, "relatime":True,
                                                      "size":"501668k",
                                                      "mode":755})
            self._mounter_mixin().add_entry_to_fstab(entry)
            self._mounter_mixin().add_entry_to_fstab(second_entry)
            self.assertTrue(self._mount_repository_mixin().is_entry_in_fstab(entry))
            self._mounter_mixin().remove_entry_from_fstab(entry)
            self.assertFalse(self._mount_repository_mixin().is_entry_in_fstab(entry))
            self.assertTrue(self._mount_repository_mixin().is_entry_in_fstab(second_entry))
