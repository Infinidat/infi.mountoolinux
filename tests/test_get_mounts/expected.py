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

MTAB_SOLARIS = [
    {
        "typename": "zfs",
        "dirname": "/",
        "fsname": "rpool/ROOT/solaris",
        "opts": {"dev": 4490002},
        "createtime": "0"
    },
    {
        "typename": "devfs",
        "dirname": "/devices",
        "fsname": "/devices",
        "opts": {"dev": 8540000},
        "createtime": "1419158457"
    },
    {
        "typename": "dev",
        "dirname": "/dev",
        "fsname": "/dev",
        "opts": {"dev": 8580000},
        "createtime": "1419158457"
    },
    {
        "typename": "ctfs",
        "dirname": "/system/contract",
        "fsname": "ctfs",
        "opts": {"dev": 8640001},
        "createtime": "1419158457"
    },
    {
        "typename": "proc",
        "dirname": "/proc",
        "fsname": "proc",
        "opts": {"dev": "85c0000"},
        "createtime": "1419158457"
    },
    {
        "typename": "mntfs",
        "dirname": "/etc/mnttab",
        "fsname": "mnttab",
        "opts": {"dev": 8680001},
        "createtime": "1419158457"
    },
    {
        "typename": "tmpfs",
        "dirname": "/system/volatile",
        "fsname": "swap",
        "opts": {"xattr": True,
        "dev": "86c0001"},
        "createtime": "1419158457"
    },
    {
        "typename": "objfs",
        "dirname": "/system/object",
        "fsname": "objfs",
        "opts": {"dev": 8700001},
        "createtime": "1419158457"
    },
    {
        "typename": "sharefs",
        "dirname": "/etc/dfs/sharetab",
        "fsname": "sharefs",
        "opts": {"dev": 8740001},
        "createtime": "1419158457"
    },
    {
        "typename": "lofs",
        "dirname": "/lib/libc.so.1",
        "fsname": "/usr/lib/libc/libc_hwcap1.so.1",
        "opts": {"dev": 4490002},
        "createtime": "1419158477"
    },
    {
        "typename": "fd",
        "dirname": "/dev/fd",
        "fsname": "fd",
        "opts": {"rw": True,
            "dev": 8840001},
        "createtime": "1419158480"
    },
    {
        "typename": "zfs",
        "dirname": "/var",
        "fsname": "rpool/ROOT/solaris/var",
        "opts": {"setuid": True,
            "nonbmand": True,
            "rw": True,
            "exec": True,
            "devices": True,
            "dev": 4490003,
            "atime": True,
            "xattr": True,
            "rstchown": True},
        "createtime": "1419158480"
    },
    {
        "typename": "tmpfs",
        "dirname": "/tmp",
        "fsname": "swap",
        "opts": {"xattr": True,
        "dev": "86c0002"},
        "createtime": "1419158480"
    },
    {
        "typename": "zfs",
        "dirname": "/var/share",
        "fsname": "rpool/VARSHARE",
        "opts": {"setuid": True,
            "nonbmand": True,
            "rw": True,
            "exec": True,
            "devices": True,
            "dev": 4490004,
            "atime": True,
            "xattr": True,
            "rstchown": True},
        "createtime": "1419158480"
    },
    {
        "typename": "zfs",
        "dirname": "/export",
        "fsname": "rpool/export",
        "opts": {"setuid": True,
            "nonbmand": True,
            "rw": True,
            "exec": True,
            "devices": True,
            "dev": 4490005,
            "atime": True,
            "xattr": True,
            "rstchown": True},
        "createtime": "1419158494"
    },
    {
        "typename": "zfs",
        "dirname": "/export/home",
        "fsname": "rpool/export/home",
        "opts": {"setuid": True,
            "nonbmand": True,
            "rw": True,
            "exec": True,
            "devices": True,
            "dev": 4490006,
            "atime": True,
            "xattr": True,
            "rstchown": True},
        "createtime": "1419158495"
    },
    {
        "typename": "zfs",
        "dirname": "/rpool",
        "fsname": "rpool",
        "opts": {"setuid": True,
            "nonbmand": True,
            "rw": True,
            "exec": True,
            "devices": True,
            "dev": 4490007,
            "atime": True,
            "xattr": True,
            "rstchown": True},
        "createtime": "1419158495"
    },
    {
        "typename": "autofs",
        "dirname": "/net",
        "fsname": "-hosts",
        "opts": {"ignore": True,
        "indirect": True,
        "nosuid": True,
        "dev": "88c0001",
        "nobrowse": True},
        "createtime": "1419158500"
    },
    {
        "typename": "autofs",
        "dirname": "/home",
        "fsname": "auto_home",
        "opts": {"ignore": True,
        "indirect": True,
        "dev": "88c0002",
        "nobrowse": True},
        "createtime": "1419158500"
    },
    {
        "typename": "autofs",
        "dirname": "/nfs4",
        "fsname": "-fedfs",
        "opts": {"dev": "88c0003",
            "ignore": True,
            "indirect": True,
            "ro": True,
            "nosuid": True,
            "nobrowse": True},
        "createtime": "1419158500"}
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

FSTAB_SOLARIS = [
    {"typename": "devfs", "dirname": "/devices", "passno": "-", "fsname": "/devices", "opts": {}},
    {"typename": "proc", "dirname": "/proc", "passno": "-", "fsname": "/proc", "opts": {}},
    {"typename": "ctfs", "dirname": "/system/contract", "passno": "-", "fsname": "ctfs", "opts": {}},
    {"typename": "objfs", "dirname": "/system/object", "passno": "-", "fsname": "objfs", "opts": {}},
    {"typename": "sharefs", "dirname": "/etc/dfs/sharetab", "passno": "-", "fsname": "sharefs", "opts": {}},
    {"typename": "fd", "dirname": "/dev/fd", "passno": "-", "fsname": "fd", "opts": {}},
    {"typename": "tmpfs", "dirname": "/tmp", "passno": "-", "fsname": "swap", "opts": {}},
    {"typename": "swap", "dirname": "none", "passno": "-", "fsname": "/dev/zvol/dsk/rpool/swap", "opts": {}}
]
