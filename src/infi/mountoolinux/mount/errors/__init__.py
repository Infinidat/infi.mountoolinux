
class BaseMountException(Exception):
    pass

class IncorrectInvocationOrPermissions(BaseMountException):
    pass

class SystemErrorExeption(BaseMountException):
    pass

class MountInternalBugException(BaseMountException):
    pass

class UserInterruptException(BaseMountException):
    pass

class ProblemWithWritingOrLockingException(BaseMountException):
    pass

class MountFailureException(BaseMountException):
    pass

class SomeMountSucceededException(BaseMountException):
    pass


ERRORCODES_DICT = {1:IncorrectInvocationOrPermissions,
                   2:SystemErrorExeption,
                   4:MountInternalBugException,
                   8:UserInterruptException,
                   16:ProblemWithWritingOrLockingException,
                   32:MountFailureException,
                   64:SomeMountSucceededException}

class MountExceptionFactory(object):
    @classmethod
    def create(cls, error_code, *args, **kwargs):
        """mount's return codes are bitwise ORed on some contants.
        This factory method creates a multiple-inherited exception class based on the error code
        """
        bases = map(lambda bit: ERRORCODES_DICT[bit],
                    filter(lambda bit: bit & error_code, ERRORCODES_DICT.keys()))
        return type("MountException", tuple(bases), {})(*args, **kwargs)
