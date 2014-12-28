from infi import unittest
from contextlib import nested, contextmanager
from .. import LinuxMounterMixin, SolarisMounterMixin, MounterMixin
from ...show_mounts import MountEntry
from mock import patch

DISTRO_LIST = ["redhat", "solaris"]
MOUNT_FS_FLAG = {
    "redhat": "-t",
    "solaris": "-F"
}

class MounterTestCase(unittest.TestCase):
    def _get_mounter_mixin_for_os(self, distro):
        if distro in ["ubuntu", "redhat"]:
            return LinuxMounterMixin
        elif distro == "solaris":
            return SolarisMounterMixin

    @contextmanager
    def patch_execute(self):
        from ... import mounter
        with patch.object(mounter, "execute") as execute:
            yield execute

    @unittest.parameters.iterate("distro", DISTRO_LIST)
    def test_mount__without_options(self, distro):
        with self.patch_execute() as execute:
            entry = MountEntry("foo" , "bar", "baz")
            self._get_mounter_mixin_for_os(distro)().mount_entry(entry)
        execute.assert_called_once_with("mount", "{} baz foo bar".format(MOUNT_FS_FLAG[distro]).split())

    @unittest.parameters.iterate("distro", DISTRO_LIST)
    def test_umount(self, distro):
        with self.patch_execute() as execute:
            entry = MountEntry("foo" , "bar", "baz")
            self._get_mounter_mixin_for_os(distro)().umount_entry(entry)
        execute.assert_called_once_with("umount", "bar".split())

    @unittest.parameters.iterate("distro", DISTRO_LIST)
    def test_mount__with_options(self, distro):
        with self.patch_execute() as execute:
            entry = MountEntry("foo" , "bar", "baz", {"rw":True, "relatime":True,
                                                      "size":"501668k",
                                                      "mode":755})
            self._get_mounter_mixin_for_os(distro)().mount_entry(entry)
        execute.assert_called_once_with("mount", "{} baz foo bar -o relatime,rw,mode=755,size=501668k".format(MOUNT_FS_FLAG[distro]).split())

class MaintainingFSTabTestCase(unittest.TestCase):
    def setUp(self):
        self._fstab = ''

    @contextmanager
    def patch_fstab(self):
        from ... import OSMountRepositoryMixin, OSMounterMixin
        with nested(patch.object(OSMountRepositoryMixin, "_read_fstab"),
                    patch.object(OSMounterMixin, "_read_fstab"),
                    patch.object(OSMounterMixin, "_get_fstab_context")) as (mock1, mock2, mock3):
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
        from ... import OSMountRepositoryMixin, OSMounterMixin
        with self.patch_fstab():
            entry = MountEntry("foo" , "bar", "baz", {"rw":True, "relatime":True,
                                                      "size":"501668k",
                                                      "mode":755})
            self.assertFalse(OSMountRepositoryMixin().is_entry_in_fstab(entry))
            OSMounterMixin().add_entry_to_fstab(entry)
            self.assertTrue(OSMountRepositoryMixin().is_entry_in_fstab(entry))

    def test_remove_entry_from_fstab(self):
        from ... import OSMountRepositoryMixin, OSMounterMixin
        with self.patch_fstab():
            entry = MountEntry("foo" , "bar", "baz", {"rw":True, "relatime":True,
                                                      "size":"501668k",
                                                      "mode":755})
            second_entry = MountEntry("foo1" , "bar1", "baz1", {"rw":True, "relatime":True,
                                                      "size":"501668k",
                                                      "mode":755})
            OSMounterMixin().add_entry_to_fstab(entry)
            OSMounterMixin().add_entry_to_fstab(second_entry)
            self.assertTrue(OSMountRepositoryMixin().is_entry_in_fstab(entry))
            OSMounterMixin().remove_entry_from_fstab(entry)
            self.assertFalse(OSMountRepositoryMixin().is_entry_in_fstab(entry))
            self.assertTrue(OSMountRepositoryMixin().is_entry_in_fstab(second_entry))
