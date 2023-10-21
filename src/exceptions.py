class UserAlreadyExist(Exception):
    pass


class UserNotExist(Exception):
    pass


class TokenNotExist(Exception):
    pass


class InvalidExistingToken(Exception):
    pass


class InvalidCredentials(Exception):
    pass


class PyJWTError(Exception):
    pass