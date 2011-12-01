from infi import unittest
from contextlib import nested, contextmanager
from .. import MounterMixin
from ...show_mounts import MountEntry
from mock import patch

class MounterTestCase(unittest.TestCase):
    @contextmanager
    def patch_execute(self):
        from ... import mounter
        with patch.object(mounter, "execute") as execute:
            yield execute

    def test_mount__without_options(self):
        with self.patch_execute() as execute:
            entry = MountEntry("foo" , "bar", "baz")
            MounterMixin().mount_entry(entry)
        execute.assert_called_once_with("mount", "-t baz foo bar".split())

    def test_umount(self):
        with self.patch_execute() as execute:
            entry = MountEntry("foo" , "bar", "baz")
            MounterMixin().umount_entry(entry)
        execute.assert_called_once_with("umount", "bar".split())

    def test_mount__with_options(self):
        with self.patch_execute() as execute:
            entry = MountEntry("foo" , "bar", "baz", {"rw":True, "relatime":True,
                                                      "size":"501668k",
                                                      "mode":755})
            MounterMixin().mount_entry(entry)
        execute.assert_called_once_with("mount", "-t baz foo bar -o relatime,rw,mode=755,size=501668k".split())

class MaintainingFSTabTestCase(unittest.TestCase):
    def setUp(self):
        self._fstab = ''

    @contextmanager
    def patch_fstab(self):
        from ...show_mounts import MountRepositoryMixin
        with nested(patch.object(MountRepositoryMixin, "_read_fstab"),
                    patch.object(MounterMixin, "_read_fstab"),
                    patch.object(MounterMixin, "_get_fstab_context")) as (mock1, mock2, mock3):
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
        from ...show_mounts import MountRepositoryMixin
        with self.patch_fstab():
            entry = MountEntry("foo" , "bar", "baz", {"rw":True, "relatime":True,
                                                      "size":"501668k",
                                                      "mode":755})
            self.assertFalse(MountRepositoryMixin().is_entry_in_fstab(entry))
            MounterMixin().add_entry_to_fstab(entry)
            self.assertTrue(MountRepositoryMixin().is_entry_in_fstab(entry))

    def test_remove_entry_from_fstab(self):
        from ...show_mounts import MountRepositoryMixin
        with self.patch_fstab():
            entry = MountEntry("foo" , "bar", "baz", {"rw":True, "relatime":True,
                                                      "size":"501668k",
                                                      "mode":755})
            MounterMixin().add_entry_to_fstab(entry)
            self.assertTrue(MountRepositoryMixin().is_entry_in_fstab(entry))
            MounterMixin().remove_entry_from_fstab(entry)
            self.assertFalse(MountRepositoryMixin().is_entry_in_fstab(entry))
