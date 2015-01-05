class SupportedFileSystemsMixin(object):
    def get_supported_file_systems(self):
        """:returns: a list of mountable filesystems on this host
        :rtype: a list of strings"""
        raise NotImplemented()

    def get_creatable_file_systems(self):
        raise NotImplemented()
