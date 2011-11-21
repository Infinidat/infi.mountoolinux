from infi import unittest
from contextlib import nested, contextmanager
from .. import MounterMixin
from ...show_mounts import MountEntry
from mock import patch
from os.path import dirname, join
import glob

from logging import getLogger
log = getLogger()

class ReadMountFilesTestCase(unittest.TestCase):
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
