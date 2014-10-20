from infi.exceptools import InfinException

class MountException(InfinException):
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
