from infi import unittest
from contextlib import nested, contextmanager
from .. import MountRepositoryMixin, MountEntry
from mock import patch
from os.path import dirname, join
import glob

from logging import getLogger
log = getLogger()

#pylint: disable-msg=W0212

MTAB_REDHAT = [
    {
        "freq": "0",
        "dirname": "/",
        "passno": "0",
        "typename": "rootfs",
        "fsname": "rootfs",
        "opts": {
            "rw": True
        }
    },
    {
        "freq": "0",
        "dirname": "/proc",
        "passno": "0",
        "typename": "proc",
        "fsname": "/proc",
        "opts": {
            "relatime": True,
            "rw": True
        }
    },
    {
        "freq": "0",
        "dirname": "/sys",
        "passno": "0",
        "typename": "sysfs",
        "fsname": "/sys",
        "opts": {
            "relatime": True,
            "rw": True
        }
    },
    {
        "freq": "0",
        "dirname": "/dev",
        "passno": "0",
        "typename": "devtmpfs",
        "fsname": "udev",
        "opts": {
            "relatime": True,
            "nr_inodes": 125417,
            "rw": True,
            "mode": 755,
            "size": "501668k"
        }
    },
    {
        "freq": "0",
        "dirname": "/dev/pts",
        "passno": "0",
        "typename": "devpts",
        "fsname": "devpts",
        "opts": {
            "relatime": True,
            "ptmxmode": 0,
            "rw": True,
            "mode": 620,
            "gid": 5
        }
    },
    {
        "freq": "0",
        "dirname": "/dev/shm",
        "passno": "0",
        "typename": "tmpfs",
        "fsname": "tmpfs",
        "opts": {
            "relatime": True,
            "rw": True
        }
    },
    {
        "freq": "0",
        "dirname": "/",
        "passno": "0",
        "typename": "ext3",
        "fsname": "/dev/sda1",
        "opts": {
            "relatime": True,
            "rw": True,
            "barrier": 1,
            "user_xattr": True,
            "acl": True,
            "errors": "continue",
            "data": "ordered"
        }
    },
    {
        "freq": "0",
        "dirname": "/proc/bus/usb",
        "passno": "0",
        "typename": "usbfs",
        "fsname": "/proc/bus/usb",
        "opts": {
            "relatime": True,
            "rw": True
        }
    },
    {
        "freq": "0",
        "dirname": "/proc/sys/fs/binfmt_misc",
        "passno": "0",
        "typename": "binfmt_misc",
        "fsname": "none",
        "opts": {
            "relatime": True,
            "rw": True
        }
    }
]

MTAB_UBUNTU = [
    {
        "freq": "0",
        "dirname": "/",
        "passno": "0",
        "typename": "rootfs",
        "fsname": "rootfs",
        "opts": {
            "rw": True
        }
    },
    {
        "freq": "0",
        "dirname": "/sys",
        "passno": "0",
        "typename": "sysfs",
        "fsname": "none",
        "opts": {
            "noexec": True,
            "relatime": True,
            "rw": True,
            "nosuid": True,
            "nodev": True
        }
    },
    {
        "freq": "0",
        "dirname": "/proc",
        "passno": "0",
        "typename": "proc",
        "fsname": "none",
        "opts": {
            "noexec": True,
            "relatime": True,
            "rw": True,
            "nosuid": True,
            "nodev": True
        }
    },
    {
        "freq": "0",
        "dirname": "/dev",
        "passno": "0",
        "typename": "devtmpfs",
        "fsname": "none",
        "opts": {
            "relatime": True,
            "nr_inodes": 61033,
            "rw": True,
            "mode": 755,
            "size": "244132k"
        }
    },
    {
        "freq": "0",
        "dirname": "/dev/pts",
        "passno": "0",
        "typename": "devpts",
        "fsname": "none",
        "opts": {
            "noexec": True,
            "relatime": True,
            "rw": True,
            "ptmxmode": 0,
            "gid": 5,
            "mode": 620,
            "nosuid": True
        }
    },
    {
        "freq": "0",
        "dirname": "/sys/fs/fuse/connections",
        "passno": "0",
        "typename": "fusectl",
        "fsname": "fusectl",
        "opts": {
            "relatime": True,
            "rw": True
        }
    },
    {
        "freq": "0",
        "dirname": "/",
        "passno": "0",
        "typename": "ext4",
        "fsname": "/dev/mapper/guyr--ubuntu-root",
        "opts": {
            "relatime": True,
            "rw": True,
            "data": "ordered",
            "errors": "remount-ro",
            "barrier": 1
        }
    },
    {
        "freq": "0",
        "dirname": "/sys/kernel/debug",
        "passno": "0",
        "typename": "debugfs",
        "fsname": "none",
        "opts": {
            "relatime": True,
            "rw": True
        }
    },
    {
        "freq": "0",
        "dirname": "/sys/kernel/security",
        "passno": "0",
        "typename": "securityfs",
        "fsname": "none",
        "opts": {
            "relatime": True,
            "rw": True
        }
    },
    {
        "freq": "0",
        "dirname": "/dev/shm",
        "passno": "0",
        "typename": "tmpfs",
        "fsname": "none",
        "opts": {
            "relatime": True,
            "rw": True,
            "nosuid": True,
            "nodev": True
        }
    },
    {
        "freq": "0",
        "dirname": "/var/run",
        "passno": "0",
        "typename": "tmpfs",
        "fsname": "none",
        "opts": {
            "relatime": True,
            "rw": True,
            "nosuid": True,
            "mode": 755
        }
    },
    {
        "freq": "0",
        "dirname": "/var/lock",
        "passno": "0",
        "typename": "tmpfs",
        "fsname": "none",
        "opts": {
            "noexec": True,
            "relatime": True,
            "rw": True,
            "nosuid": True,
            "nodev": True
        }
    },
    {
        "freq": "0",
        "dirname": "/boot",
        "passno": "0",
        "typename": "ext2",
        "fsname": "/dev/sda1",
        "opts": {
            "relatime": True,
            "rw": True,
            "errors": "continue"
        }
    },
    {
        "freq": "0",
        "dirname": "/media/bootsrv",
        "passno": "0",
        "typename": "fuse.sshfs",
        "fsname": "root@bootsrv:/",
        "opts": {
            "relatime": True,
            "rw": True,
            "user_id": 1000,
            "max_read": 65536,
            "group_id": 1000,
            "nosuid": True,
            "nodev": True
        }
    },
    {
        "freq": "0",
        "dirname": "/media/guyr-air",
        "passno": "0",
        "typename": "fuse.sshfs",
        "fsname": "guy@192.168.11.62:/",
        "opts": {
            "relatime": True,
            "rw": True,
            "user_id": 1000,
            "max_read": 65536,
            "group_id": 1000,
            "nosuid": True,
            "nodev": True
        }
    },
    {
        "freq": "0",
        "dirname": "/tmp/bar",
        "passno": "0",
        "typename": "ext3",
        "fsname": "/dev/loop0",
        "opts": {
            "relatime": True,
            "rw": True,
            "data": "ordered",
            "errors": "continue",
            "barrier": 0
        }
    }
]

FSTAB_REDHAT = [
    {
        "freq": "1",
        "dirname": "/",
        "passno": "1",
        "typename": "ext3",
        "fsname": "UUID=c3dc6889-9901-4b67-b48d-ea12ca241213",
        "opts": {
            "defaults": True
        }
    },
    {
        "freq": "0",
        "dirname": "swap",
        "passno": "0",
        "typename": "swap",
        "fsname": "UUID=e76257f7-99ac-4e2d-bf58-12d53162a151",
        "opts": {
            "defaults": True
        }
    },
    {
        "freq": "0",
        "dirname": "/dev/shm",
        "passno": "0",
        "typename": "tmpfs",
        "fsname": "tmpfs",
        "opts": {
            "defaults": True
        }
    },
    {
        "freq": "0",
        "dirname": "/dev/pts",
        "passno": "0",
        "typename": "devpts",
        "fsname": "devpts",
        "opts": {
            "gid": 5,
            "mode": 620
        }
    },
    {
        "freq": "0",
        "dirname": "/sys",
        "passno": "0",
        "typename": "sysfs",
        "fsname": "sysfs",
        "opts": {
            "defaults": True
        }
    },
    {
        "freq": "0",
        "dirname": "/proc",
        "passno": "0",
        "typename": "proc",
        "fsname": "proc",
        "opts": {
            "defaults": True
        }
    }
]

FSTAB_UBUNTU = [
    {
        "freq": "0",
        "dirname": "/proc",
        "passno": "0",
        "typename": "proc",
        "fsname": "proc",
        "opts": {
            "noexec": True,
            "nosuid": True,
            "nodev": True
        }
    },
    {
        "freq": "0",
        "dirname": "/",
        "passno": "1",
        "typename": "ext4",
        "fsname": "/dev/mapper/guyr--ubuntu-root",
        "opts": {
            "errors": "remount-ro"
        }
    },
    {
        "freq": "0",
        "dirname": "/boot",
        "passno": "2",
        "typename": "ext2",
        "fsname": "UUID=0c54c7fd-8192-4646-96f0-1bc4d1045bc3",
        "opts": {
            "defaults": True
        }
    },
    {
        "freq": "0",
        "dirname": "none",
        "passno": "0",
        "typename": "swap",
        "fsname": "/dev/mapper/guyr--ubuntu-swap_1",
        "opts": {
            "sw": True
        }
    },
    {
        "freq": "0",
        "dirname": "/media/floppy0",
        "passno": "0",
        "typename": "auto",
        "fsname": "/dev/fd0",
        "opts": {
            "utf8": True,
            "noauto": True,
            "rw": True,
            "user": True,
            "exec": True
        }
    }
]

class ReadMountFilesTestCase(unittest.TestCase):
    @contextmanager
    def patch_getters(self, distro):
        self.assertIn(distro, ["ubuntu", "redhat"])

        with nested(patch.object(MountRepositoryMixin, "_read_fstab"),
                    patch.object(MountRepositoryMixin, "_read_mtab_from_proc")) as \
                    (fstab, mtab):
            with open(join(dirname(__file__), distro, "fstab")) as fd:
                fstab.return_value = fd.read()
            with open(join(dirname(__file__), distro, "mounts")) as fd:
                mtab.return_value = fd.read()
            yield (fstab, mtab)

    @unittest.parameters.iterate("distro", ["ubuntu", "redhat"])
    def test_read(self, distro):
        with self.patch_getters(distro):
            actual = MountRepositoryMixin()._read_fstab()
            self.assertNotEqual(actual, '')
            actual = MountRepositoryMixin()._read_mtab_from_proc()
            self.assertNotEqual(actual, '')

    @unittest.parameters.iterate("distro", ["ubuntu", "redhat"])
    def test_get_groupdicts_from_mtab(self, distro):
        with self.patch_getters(distro):
            actual = MountRepositoryMixin()._get_list_of_groupdicts_from_mtab()
            if distro == "ubuntu":
                self.assertEqual(actual, MTAB_UBUNTU)
            if distro == "redhat":
                self.assertEqual(actual, MTAB_REDHAT)

    @unittest.parameters.iterate("distro", ["ubuntu", "redhat"])
    def test_get_groupdicts_from_fstab(self, distro):
        with self.patch_getters(distro):
            actual = MountRepositoryMixin()._get_list_of_groupdicts_from_fstab()
            if distro == "ubuntu":
                self.assertEqual(actual, FSTAB_UBUNTU)
            if distro == "redhat":
                self.assertEqual(actual, FSTAB_REDHAT)

    @unittest.parameters.iterate("distro", ["ubuntu", "redhat"])
    def test_get_mounts_from_fstab(self, distro):
        with self.patch_getters(distro):
            actual = MountRepositoryMixin().get_mounts_from_fstab()
            self.assertEqual(len(actual),
                             len(MountRepositoryMixin()._get_list_of_groupdicts_from_fstab()))
            for instance in actual:
                self.assertIsInstance(instance, MountEntry)

    @unittest.parameters.iterate("distro", ["ubuntu", "redhat"])
    def test_get_mounts_from_mtab(self, distro):
        with self.patch_getters(distro):
            actual = MountRepositoryMixin().get_mounts_from_mtab()
            self.assertEqual(len(actual),
                             len(MountRepositoryMixin()._get_list_of_groupdicts_from_mtab()))
            for instance in actual:
                self.assertIsInstance(instance, MountEntry)

    def test_is_path_mounted(self):
        with self.patch_getters("redhat"):
            repo = MountRepositoryMixin()
            self.assertTrue(repo.is_path_mounted("/"))
            self.assertFalse(repo.is_path_mounted("hello world"))

    def test_is_device_mounted(self):
        with self.patch_getters("redhat"):
            repo = MountRepositoryMixin()
            self.assertTrue(repo.is_fs_mounted("/dev/sda1"))
            self.assertFalse(repo.is_fs_mounted("hello world"))

    def test_is_entry_in_fstab(self):
        with self.patch_getters("redhat"):
            repo = MountRepositoryMixin()
            entry = repo.get_mounts_from_mtab()[4]
            self.assertTrue(repo.is_entry_in_fstab(entry))
