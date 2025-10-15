from domain.exceptions import DomainException


class InvalidResourceCopyTarget(DomainException):
    code = 10409
    message = "Invalid resource copy target."


class UserNotFound(DomainException):
    code = 10404
    message = "User not found."


class CategoryDoesNotExist(DomainException):
    code = 10407
    message = "Category not found."


class CategoryAlreadyExists(DomainException):
    code = 10411
    message = "Categoty already exists."


class UserDoesNotExistError(DomainException):
    code = 10403
    message = "User with the email does not exist."


class UserWithEmailAlreadyExistsError(DomainException):
    code = 10404
    message = "User with the email already exists."


class WrongPasswordError(DomainException):
    code = 10405
    message = "Wrong password has been entered"


class PostTitleAlreadyExists(DomainException):
    code = 10410
    message = "Post with that title already exists."
