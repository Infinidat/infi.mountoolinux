from unittest import SkipTest
from infi import unittest
from infi.pyutils.contexts import contextmanager
from infi.execute import execute

#pylint: disable-msg=C0103

class MountManagerTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from platform import platform
        if not platform().startswith("Linux"):
            raise SkipTest("This TestCase runs only on Linux")

    @contextmanager
    def tempfile_context(self, filesystem="ext3"):
        from tempfile import mkstemp
        fd, name = mkstemp()
        from os import write, close
        ZERO_MB = '\x00' * 1024 * 1024
        write(fd, ZERO_MB * 10)
        close(fd)
        execute("mkfs.ext3 -F {}".format(name).split())
        yield name

    def test__tempfile_loop_device(self):
        filesystem = "ext3"
        with self.tempfile_context(filesystem) as block_path:
            from os import makedirs
            mount_path = "{}.mount".format(block_path)
            makedirs(mount_path)
            from .. import MountManager, MountEntry
            manager = MountManager()
            self.assertFalse(manager.is_path_mounted(mount_path))
            entry = MountEntry(block_path, mount_path, filesystem, opts={"loop":True})
            manager.mount_entry(entry)
            self.assertTrue(manager.is_path_mounted(mount_path))
            manager.umount_entry(entry)
            self.assertFalse(manager.is_path_mounted(mount_path))
