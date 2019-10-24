class AuthError(BaseException):
    """ Base AuthError """
    pass


class InvalidPassword(AuthError):
    """ Password less than 6 characters or password does not match valid username """
    pass


class UserDoesNotExist(AuthError):
    """ Username does not exist - upon login """
    pass


class PermissionDoesNotExist(Exception):
    """ Entered permission that is not in Group's permission list"""
    pass


class PermissionAlreadyExist(Exception):
    """ Entered permission that is already in Group's permission list"""
    pass


class GroupDoesNotExist(Exception):
    """ Adding membership to a Group that does not exist"""
    pass


class GroupAlreadyExist(Exception):
    """ Adding Group name that already exist"""
    pass


class UserAlreadyExist(Exception):
    """ UserName already exist - upon registration or adding of users by SuperUser """
    pass


class ActionNotAuthorized(Exception):
    """ If user not authorized for an action """
    pass
