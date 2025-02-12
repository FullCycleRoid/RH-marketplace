from typing import Any

from fastapi import HTTPException, status

from src.core.constants import ErrorCode


class DetailedHTTPException(HTTPException):
    STATUS_CODE = status.HTTP_500_INTERNAL_SERVER_ERROR
    DETAIL = "Внутренняя ошибка сервера"

    def __init__(self, **kwargs: dict[str, Any]) -> None:
        super().__init__(status_code=self.STATUS_CODE, detail=self.DETAIL, **kwargs)


class PermissionDenied(DetailedHTTPException):
    STATUS_CODE = status.HTTP_403_FORBIDDEN
    DETAIL = "Доступ запрещен"


class NotFound(DetailedHTTPException):
    STATUS_CODE = status.HTTP_404_NOT_FOUND


class AlreadyExist(DetailedHTTPException):
    STATUS_CODE = status.HTTP_409_CONFLICT


class BadRequest(DetailedHTTPException):
    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    DETAIL = "Некорректный запрос"


class PydanticValidationError(DetailedHTTPException):
    STATUS_CODE = status.HTTP_422_UNPROCESSABLE_ENTITY
    DETAIL = "Ошибка валидации данных"


class NotAuthenticated(DetailedHTTPException):
    STATUS_CODE = status.HTTP_401_UNAUTHORIZED
    DETAIL = "Пользователь не аутентифицирован"

    def __init__(self) -> None:
        super().__init__(headers={"WWW-Authenticate": "Bearer"})


class AcceptCodeNotFound(NotFound):
    DETAIL = ErrorCode.ACCEPT_CODE_NOT_FOUND


class RedisKeyNotFound(NotFound):
    DETAIL = ErrorCode.REDIS_KEY_NOT_FOUND


class WrongAcceptCode(BadRequest):
    DETAIL = ErrorCode.WRONG_ACCEPT_CODE
