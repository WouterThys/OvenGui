
class InvalidPointsException(Exception):
    """
    Errors for creating graph
    """
    def __init__(self, message):
        super(InvalidPointsException, self).__init__(message)


class InterpolateFailedException(Exception):
    """
    Errors for creating graph
    """
    def __init__(self, message):
        super(InterpolateFailedException, self).__init__(message)