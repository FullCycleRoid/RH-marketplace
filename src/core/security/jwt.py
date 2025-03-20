from datetime import datetime
from typing import Any, Dict, Optional

from fastapi import Depends
from jose import JWTError, jwt
from pydantic import ConfigDict, Field

from src.auth.config import auth_config
from src.auth.exceptions import ExpiredToken, InvalidToken
from src.core.interfaces.dto import BaseDTO
from src.core.security.oauth import oauth2_scheme


class JWTData(BaseDTO):
    user_id: int = Field(alias="sub")
    expires: datetime = Field(alias="exp")

    model_config = ConfigDict(populate_by_name=True)


def create_jwt_token(
    jwt_data: Dict[str, Any],
    key: str = auth_config.JWT_SECRET,
    algorithm: str = auth_config.JWT_ALG,
) -> str:
    return jwt.encode(claims=jwt_data, key=key, algorithm=algorithm)


async def parse_jwt_data_from_token(token: str) -> JWTData:
    if not token:
        raise InvalidToken

    try:
        payload = jwt.decode(
            token, auth_config.JWT_SECRET, algorithms=[auth_config.JWT_ALG]
        )

    except jwt.ExpiredSignatureError:
        raise ExpiredToken

    except JWTError:
        raise InvalidToken

    return JWTData(**payload)


async def parse_jwt_data_from_oauth2(
    token: Optional[str] = Depends(oauth2_scheme),
) -> JWTData:
    return await parse_jwt_data_from_token(token=token)
