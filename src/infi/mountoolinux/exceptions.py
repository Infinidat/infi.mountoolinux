from infi.exceptools import InfiException

class MountException(InfiException):
    pass

class IncorrectInvocationOrPermissions(MountException):
    pass

class SystemErrorExeption(MountException):
    pass

class MountInternalBugException(MountException):
    pass

class UserInterruptException(MountException):
    pass

class ProblemWithWritingOrLockingException(MountException):
    pass

class MountFailureException(MountException):
    pass

class SomeMountSucceededException(MountException):
    pass


ERRORCODES_DICT = {1:IncorrectInvocationOrPermissions,
                   2:SystemErrorExeption,
                   4:MountInternalBugException,
                   8:UserInterruptException,
                   16:ProblemWithWritingOrLockingException,
                   32:MountFailureException,
                   64:SomeMountSucceededException}
