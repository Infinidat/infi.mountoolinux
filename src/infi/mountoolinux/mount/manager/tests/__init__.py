from infi import unittest
from .. import MountManager
from mock import patch

class GetSupportedTestCase(unittest.TestCase):
    @patch.object(MountManager, "_get_proc_filesystems")
    @patch.object(MountManager, "_get_etc_filesystems")
    def test_empty_list(self, etc, proc):
        etc.return_value = ''
        proc.return_value = ''
        actual = MountManager().get_supported_file_systems()
        expected = []
        self.assertEqual(actual, expected)

    @patch.object(MountManager, "_get_proc_filesystems")
    @patch.object(MountManager, "_get_etc_filesystems")
    def test_proc_only(self, etc, proc):
        from os.path import dirname, join
        etc.return_value = ''
        with open(join(dirname(__file__), "proc")) as fd:
            proc.return_value = fd.read()
        actual = MountManager().get_supported_file_systems()
        expected = ["ext3", "iso9660"]
        self.assertEqual(actual, expected)

    @patch.object(MountManager, "_get_proc_filesystems")
    @patch.object(MountManager, "_get_etc_filesystems")
    def test_etc_only(self, etc, proc):
        from os.path import dirname, join
        etc.return_value = ''
        with open(join(dirname(__file__), "etc")) as fd:
            etc.return_value = fd.read()
        actual = MountManager().get_supported_file_systems()
        expected = ['hfsplus', 'ext3', 'ext2', 'iso9660', 'hfs', 'vfat']
        self.assertEqual(actual, expected)

    @patch.object(MountManager, "_get_proc_filesystems")
    @patch.object(MountManager, "_get_etc_filesystems")
    def test_both__proc_is_empty(self, etc, proc):
        from os.path import dirname, join
        etc.return_value = ''
        proc.return_value = ''
        with open(join(dirname(__file__), "etc")) as fd:
            etc.return_value = fd.read() + "\n*"
        actual = MountManager().get_supported_file_systems()
        expected = ['hfsplus', 'ext3', 'ext2', 'iso9660', 'hfs', 'vfat']
        self.assertEqual(actual, expected)
        self.assertTrue(proc.called)

    @patch.object(MountManager, "_get_proc_filesystems")
    @patch.object(MountManager, "_get_etc_filesystems")
    def test_both__proc_is_same_data(self, etc, proc):
        from os.path import dirname, join
        etc.return_value = ''
        proc.return_value = "hfs\next3"
        with open(join(dirname(__file__), "etc")) as fd:
            etc.return_value = fd.read() + "\n*"
        actual = MountManager().get_supported_file_systems()
        expected = ['hfsplus', 'ext3', 'ext2', 'iso9660', 'hfs', 'vfat']
        self.assertEqual(actual, expected)

    @patch.object(MountManager, "_get_proc_filesystems")
    @patch.object(MountManager, "_get_etc_filesystems")
    def test_both__proc_is_new_data(self, etc, proc):
        from os.path import dirname, join
        etc.return_value = ''
        proc.return_value = "xxx"
        with open(join(dirname(__file__), "etc")) as fd:
            etc.return_value = fd.read() + "\n*"
        actual = MountManager().get_supported_file_systems()
        expected = ['hfsplus', 'ext3', 'ext2', 'iso9660', 'hfs', 'xxx', 'vfat']
        self.assertEqual(actual, expected)
