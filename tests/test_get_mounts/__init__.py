from infi import unittest
from contextlib import nested, contextmanager
from .. import MountEntry, LinuxMountRepositoryMixin, SolarisMountRepositoryMixin
from mock import patch
from os.path import dirname, join
from expected import MTAB_REDHAT, MTAB_UBUNTU, MTAB_SOLARIS, \
                     FSTAB_REDHAT, FSTAB_UBUNTU, FSTAB_SOLARIS
import glob

from logging import getLogger
log = getLogger()

#pylint: disable-msg=W0212

DISTRO_LIST = ["ubuntu", "redhat", "solaris"]

class ReadMountFilesTestCase(unittest.TestCase):
    def _get_mount_repository_for_os(self, distro):
        if distro in ["ubuntu", "redhat"]:
            return  LinuxMountRepositoryMixin
        elif distro == "solaris":
            return SolarisMountRepositoryMixin

    @contextmanager
    def patch_getters(self, distro):
        self.assertIn(distro, DISTRO_LIST)
        mount_repository_mixin = self._get_mount_repository_for_os(distro)
        with nested(patch.object(mount_repository_mixin, "_read_fstab"),
                    patch.object(mount_repository_mixin, "_read_mtab")) as \
                    (fstab, mtab):
            with open(join(dirname(__file__), distro, "fstab")) as fd:
                fstab.return_value = fd.read()
            with open(join(dirname(__file__), distro, "mtab")) as fd:
                mtab.return_value = fd.read()
            yield (fstab, mtab)

    @unittest.parameters.iterate("distro", DISTRO_LIST)
    def test_read(self, distro):
        with self.patch_getters(distro):
            actual = self._get_mount_repository_for_os(distro)()._read_fstab()
            self.assertNotEqual(actual, '')
            actual = self._get_mount_repository_for_os(distro)()._read_mtab()
            self.assertNotEqual(actual, '')

    @unittest.parameters.iterate("distro", DISTRO_LIST)
    def test_get_groupdicts_from_mtab(self, distro):
        with self.patch_getters(distro):
            actual = self._get_mount_repository_for_os(distro)()._get_list_of_groupdicts_from_mtab()
            if distro == "ubuntu":
                self.assertEqual(actual, MTAB_UBUNTU)
            elif distro == "redhat":
                self.assertEqual(actual, MTAB_REDHAT)
            elif distro == "solaris":
                self.assertEqual(actual, MTAB_SOLARIS)

    @unittest.parameters.iterate("distro", DISTRO_LIST)
    def test_get_groupdicts_from_fstab(self, distro):
        with self.patch_getters(distro):
            actual = self._get_mount_repository_for_os(distro)()._get_list_of_groupdicts_from_fstab()
            if distro == "ubuntu":
                self.assertEqual(actual, FSTAB_UBUNTU)
            elif distro == "redhat":
                self.assertEqual(actual, FSTAB_REDHAT)
            elif distro == "solaris":
                self.assertEqual(actual, FSTAB_SOLARIS)

    @unittest.parameters.iterate("distro", DISTRO_LIST)
    def test_get_mounts_from_fstab(self, distro):
        with self.patch_getters(distro):
            actual = self._get_mount_repository_for_os(distro)().get_mounts_from_fstab()
            self.assertEqual(len(actual),
                             len(self._get_mount_repository_for_os(distro)()._get_list_of_groupdicts_from_fstab()))
            for instance in actual:
                self.assertIsInstance(instance, MountEntry)

    @unittest.parameters.iterate("distro", DISTRO_LIST)
    def test_get_mounts_from_mtab(self, distro):
        with self.patch_getters(distro):
            actual = self._get_mount_repository_for_os(distro)().get_mounts_from_mtab()
            self.assertEqual(len(actual),
                             len(self._get_mount_repository_for_os(distro)()._get_list_of_groupdicts_from_mtab()))
            for instance in actual:
                self.assertIsInstance(instance, MountEntry)

    def test_is_path_mounted(self):
        with self.patch_getters("redhat"):
            repo = self._get_mount_repository_for_os("redhat")()
            self.assertTrue(repo.is_path_mounted("/"))
            self.assertFalse(repo.is_path_mounted("hello world"))

    def test_is_device_mounted(self):
        with self.patch_getters("redhat"):
            repo = self._get_mount_repository_for_os("redhat")()
            self.assertTrue(repo.is_fs_mounted("/dev/sda1"))
            self.assertFalse(repo.is_fs_mounted("hello world"))

    def test_is_entry_in_fstab(self):
        with self.patch_getters("redhat"):
            repo = self._get_mount_repository_for_os("redhat")()
            entry = repo.get_mounts_from_mtab()[4]
            self.assertTrue(repo.is_entry_in_fstab(entry))
