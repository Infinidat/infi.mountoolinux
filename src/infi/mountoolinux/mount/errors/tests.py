
from infi import unittest
from . import MountExceptionFactory

class ExceptionFactoryTestCase(unittest.TestCase):
    def test_single_exception(self):
        error = MountExceptionFactory(1)

