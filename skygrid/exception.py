class SkygridException(Exception):
    pass


# indicates the login has failed
class AuthenticationError(SkygridException):
    pass


class ProjectError(SkygridException):
    pass
