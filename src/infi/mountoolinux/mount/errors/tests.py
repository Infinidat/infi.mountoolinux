
from infi import unittest
from . import MountExceptionFactory
from . import ERRORCODES_DICT

class ExceptionFactoryTestCase(unittest.TestCase):
    def test_single_exception(self):
        error = MountExceptionFactory.create(1)
        self.assertIsInstance(error, ERRORCODES_DICT[1])

    def test_two_exceptions(self):
        error = MountExceptionFactory.create(3)
        self.assertIsInstance(error, ERRORCODES_DICT[1])
        self.assertIsInstance(error, ERRORCODES_DICT[2])

    def test_all(self):
        error_mask = 1 + 2 + 4 + 8 + 16 + 32 + 64
        error = MountExceptionFactory.create(error_mask)
        for key, value in ERRORCODES_DICT.items():
            self.assertIsInstance(error, value)

