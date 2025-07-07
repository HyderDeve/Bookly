

class BooklyException(Exception):
    pass

class InvalidToken(BooklyException):
    """User has provided an Invalid Token"""
    pass

class RevokedToken(BooklyException):
    """User has provided a Revoked Token"""
    pass

class AccessTokenRequired(BooklyException):
    """User has not provided an Access Token"""
    pass

class RefreshTokenRequired(BooklyException):
    """User has not provided a Refresh Token"""
    pass

class UserAlreadyExists(BooklyException):
    """User with the provided email already exists"""
    pass

class InsufficientPermission(BooklyException):
    """User does not have sufficient permissions to perform this action"""
    pass

class BookNotFound(BooklyException):
    """Book with provided ID does not exist"""
    pass

class UserNotFound(BooklyException):
    """User with provided ID does not exist"""
    pass

class TagNotFound(BooklyException):
    """Tag with provided ID does not exist"""
    pass