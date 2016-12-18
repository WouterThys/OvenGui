

class InvalidPointsException(Exception):
    def __init__(self, message):
        super(InvalidPointsException, self).__init__(message)