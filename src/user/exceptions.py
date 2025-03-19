from src.core.exceptions import (
    AlreadyExist,
    BadRequest,
    NotAuthenticated,
    NotFound,
    PermissionDenied,
)
from src.user.constants import ErrorCode


class AuthRequired(NotAuthenticated):
    DETAIL = ErrorCode.AUTHENTICATION_REQUIRED


class AuthorizationFailed(PermissionDenied):
    DETAIL = ErrorCode.AUTHORIZATION_FAILED


class InvalidToken(NotAuthenticated):
    DETAIL = ErrorCode.INVALID_TOKEN


class ExpiredToken(NotAuthenticated):
    DETAIL = ErrorCode.EXPIRED_TOKEN


class InvalidCredentials(NotAuthenticated):
    DETAIL = ErrorCode.INVALID_CREDENTIALS


class EmailTaken(AlreadyExist):
    DETAIL = ErrorCode.EMAIL_TAKEN


class EmailNotValid(BadRequest):
    DETAIL = ErrorCode.EMAIL_NOT_VALID


class PhoneTaken(AlreadyExist):
    DETAIL = ErrorCode.PHONE_TAKEN


class RefreshTokenNotValid(NotAuthenticated):
    DETAIL = ErrorCode.REFRESH_TOKEN_NOT_VALID


class UserNotFound(NotFound):
    DETAIL = ErrorCode.USER_NOT_FOUND


class InvalidConfirmationCode(BadRequest):
    DETAIL = ErrorCode.INVALID_CONFIRMATION_CODE


class ConfirmationCodeExpired(NotFound):
    DETAIL = ErrorCode.CONFIRMATION_CODE_EXPIRED


class EmailNotConfirmed(PermissionDenied):
    DETAIL = ErrorCode.EMAIL_NOT_CONFIRMED


class EmailAlreadyConfirmed(BadRequest):
    DETAIL = ErrorCode.EMAIL_ALREADY_CONFIRMED


class IncorrectOldPassword(BadRequest):
    DETAIL = ErrorCode.INCORRECT_OLD_PASSWORD


class RefreshTokenNotFound(NotFound):
    DETAIL = ErrorCode.REFRESH_TOKEN_NOT_FOUND


class UserPhoneAlreadyVerified(AlreadyExist):
    DETAIL = ErrorCode.USER_PHONE_ALREADY_VERIFIED


class AdminRoleNotFound(NotFound):
    DETAIL = ErrorCode.ADMIN_ROLE_NOT_FOUND
