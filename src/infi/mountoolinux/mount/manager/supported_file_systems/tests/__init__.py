from infi import unittest
from contextlib import nested, contextmanager
from .. import SupportedFileSystemsMixin
from mock import patch
from os.path import dirname, join
import glob

#pylint: disable-msg=W0621

class GetSupportedTestCase(unittest.TestCase):
    @contextmanager
    def patch_getters(self):
        with nested(patch.object(SupportedFileSystemsMixin, "_get_proc_filesystems"),
                    patch.object(SupportedFileSystemsMixin, "_get_etc_filesystems"),
                    patch("glob.glob")) as \
                    (proc, etc, glob):
            etc.return_value = ''
            proc.return_value = ''
            glob.return_value = []
            yield (proc, etc)

    def test_empty_list(self):
        with self.patch_getters() as (proc, etc):
            actual = SupportedFileSystemsMixin().get_supported_file_systems()
            expected = []
            self.assertEqual(actual, expected)

    def test_proc_only(self):
        with self.patch_getters() as (proc, etc):
            with open(join(dirname(__file__), "proc")) as fd:
                proc.return_value = fd.read()
            actual = SupportedFileSystemsMixin().get_supported_file_systems()
            expected = ["ext3", "iso9660"]
            self.assertEqual(actual, expected)

    def test_etc_only(self):
        with self.patch_getters() as (proc, etc):
            with open(join(dirname(__file__), "etc")) as fd:
                etc.return_value = fd.read()
            actual = SupportedFileSystemsMixin().get_supported_file_systems()
            expected = ['hfsplus', 'ext3', 'ext2', 'iso9660', 'hfs', 'vfat']
            self.assertEqual(actual, expected)

    def test_both__proc_is_empty(self):
        with self.patch_getters() as (proc, etc):
            with open(join(dirname(__file__), "etc")) as fd:
                etc.return_value = fd.read() + "\n*"
            actual = SupportedFileSystemsMixin().get_supported_file_systems()
            expected = ['hfsplus', 'ext3', 'ext2', 'iso9660', 'hfs', 'vfat']
            self.assertEqual(actual, expected)
            self.assertTrue(proc.called)

    def test_both__proc_is_same_data(self):
        with self.patch_getters() as (proc, etc):
            proc.return_value = "hfs\next3"
            with open(join(dirname(__file__), "etc")) as fd:
                etc.return_value = fd.read() + "\n*"
            actual = SupportedFileSystemsMixin().get_supported_file_systems()
            expected = ['hfsplus', 'ext3', 'ext2', 'iso9660', 'hfs', 'vfat']
            self.assertEqual(actual, expected)

    def test_both__proc_is_new_data(self):
        with self.patch_getters() as (proc, etc):
            proc.return_value = "xxx"
            with open(join(dirname(__file__), "etc")) as fd:
                etc.return_value = fd.read() + "\n*"
            actual = SupportedFileSystemsMixin().get_supported_file_systems()
            expected = ['hfsplus', 'ext3', 'ext2', 'iso9660', 'hfs', 'xxx', 'vfat']
            self.assertEqual(actual, expected)

    def test_helpers_only(self):
        import glob
        with self.patch_getters():
            with patch.object(glob, "glob") as _glob:
                _glob.return_value = ["/sbin/mount.{}".format(name) for name in ['ntfs', 'nfs', 'cifs']]
                actual = SupportedFileSystemsMixin().get_supported_file_systems()
                expected = ['ntfs', 'nfs', 'cifs']
                self.assertEqual(actual, expected)

    def test_internal_and_helpers__different_data(self):
        import glob
        with self.patch_getters() as (proc, etc):
            with patch.object(glob, "glob") as _glob:
                _glob.return_value = ["/sbin/mount.{}".format(name) for name in ['ntfs', 'nfs', 'cifs']]
                proc.return_value = "xxx"
                with open(join(dirname(__file__), "etc")) as fd:
                    etc.return_value = fd.read() + "\n*"
                actual = SupportedFileSystemsMixin().get_supported_file_systems()
                expected = ['hfsplus', 'ntfs', 'ext3', 'ext2', 'iso9660', 'hfs', 'xxx', 'nfs', 'vfat', 'cifs']
                self.assertEqual(actual, expected)

    def test_internal_and_helpers__same_data(self):
        import glob
        with patch.object(glob, "glob") as _glob:
            _glob.return_value = ["/sbin/mount.{}".format(name) for name in ['ext3', 'hfs']]
            with self.patch_getters() as (proc, etc):
                proc.return_value = "hfs\next3"
                with open(join(dirname(__file__), "etc")) as fd:
                    etc.return_value = fd.read() + "\n*"
                actual = SupportedFileSystemsMixin().get_supported_file_systems()
                expected = ['hfsplus', 'ext3', 'ext2', 'iso9660', 'hfs', 'vfat']
                self.assertEqual(actual, expected)
