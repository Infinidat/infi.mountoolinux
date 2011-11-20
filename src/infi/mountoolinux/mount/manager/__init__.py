class MountManager(object):
    def get_supported_file_systems(self):
        """:returns: a list of mountable filesystems on this host
        :rtype: a list of strings"""
        return self._get_list_of_internally_supported_file_systems() + \
            self._get_list_of_supprted_file_systems_by_helpers()

    def _get_list_of_internally_supported_file_systems(self):
        raise NotImplementedError()

    def _get_list_of_supprted_file_systems_by_helpers(self):
        raise NotImplementedError()



