class SupportedFileSystemsMixin(object):
    def get_supported_file_systems(self):
        """:returns: a list of mountable filesystems on this host
        :rtype: a list of strings"""
        result = set()
        for name in self._get_list_of_internally_supported_file_systems() + \
                    self._get_list_of_supported_file_systems_by_helpers():
            result.add(name)
        return [name for name in result]
        
    def get_creatable_file_systems(self):
        from os import listdir
        mountable = self.get_supported_file_systems()
        creatable = [fs[5:] for fs in listdir("/sbin") if fs.startswith("mkfs.")]
        creatable_and_mountable = [fs for fs in creatable if fs in mountable]
        return creatable_and_mountable

    def _get_list_of_internally_supported_file_systems(self):
        # mount will try to read the file /etc/filesystems,  or,
        # if  that  does  not  exist, /proc/filesystems.  All of the filesystem types listed there will be
        # tried, except for those that are labeled "nodev" (e.g., devpts, proc and nfs).  If /etc/filesys-
        # tems ends in a line with a single * only, mount will read /proc/filesystems afterwards.
        result = set()
        for name in self._get_filesystem_names_from_etc():
            result.add(name)
        if len(result) == 0 or (self._get_etc_filesystems().splitlines() and
                                self._get_etc_filesystems().splitlines()[-1] == '*'):
            for name in self._get_filesystem_names_from_proc():
                result.add(name)
        return [name for name in result]

    def _get_filesystem_names_from_etc(self):
        result = []
        for line in self._get_etc_filesystems().splitlines():
            if line == '' or line.startswith("nodev") or '*' in line:
                continue
            result.append(line)
        return result

    def _get_filesystem_names_from_proc(self):
        result = []
        for line in self._get_proc_filesystems().splitlines():
            if line == '' or line.startswith("nodev"):
                continue
            result.append(line.strip())
        return result

    def _get_proc_filesystems(self):
        from os.path import exists
        path = "/proc/filesystems"
        if not exists(path):
            return ''
        with open(path) as fd:
            return fd.read()

    def _get_etc_filesystems(self):
        from os.path import exists
        path = "/etc/filesystems"
        if not exists(path):
            return ''
        with open(path) as fd:
            return fd.read()

    def _get_list_of_supported_file_systems_by_helpers(self):
        from glob import glob
        basedir = "/sbin"
        replace_string = "{}/mount.".format(basedir)
        return map(lambda path: path.replace(replace_string, ""),
                   glob("{}*".format(replace_string)))

