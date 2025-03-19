from fastapi import Request, status
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse


def response_contract_http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.detail,
            "data": None,
            "status": exc.status_code,
        },
    )


def response_contract_validation_exception_handler(
    request: Request, exc: RequestValidationError
):
    error_msg: str
    if exc.errors()[0]["msg"].startswith("Value"):
        error_msg: str = exc.errors()[0]["msg"].split("error, ")[1]
    else:
        error_msg: str = exc.errors()[0]["msg"]

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "error": error_msg,
            "data": None,
            "status": status.HTTP_422_UNPROCESSABLE_ENTITY,
        },
    )
