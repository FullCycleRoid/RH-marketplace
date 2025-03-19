from typing import Any, Dict, Optional

from fastapi import Depends
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security import APIKeyCookie, OAuth2
from jose import JWTError, jwt
from starlette.requests import Request

from src.auth.config import auth_config
from src.user.exceptions import AuthorizationFailed, ExpiredToken, InvalidToken
from src.user.presentation.schemas import JWTData


class OAuth2Cookie(OAuth2):
    """
    Class uses OAuth2 to retrieve token for user authentication from cookies.
    """

    def __init__(
        self,
        tokenUrl: str,
        scheme_name: Optional[str] = None,
        scopes: Optional[Dict[str, str]] = None,
        description: Optional[str] = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(
            flows=flows,
            scheme_name=scheme_name,
            description=description,
            auto_error=auto_error,
        )

    async def __call__(self, request: Request) -> Optional[str]:
        """
        Retrieves token for user authentication from cookies, if exists.
        """

        token: Optional[str] = request.cookies.get(auth_config.ACCESS_TOKEN_KEY)
        if not token:
            if self.auto_error:
                raise AuthorizationFailed
            else:
                return None
        return token


oauth2_scheme = OAuth2Cookie(
    tokenUrl="/api/marketplace/user/users/tokens", auto_error=False
)
refresh_token_scheme = APIKeyCookie(
    name=auth_config.REFRESH_TOKEN_KEY, auto_error=False
)


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
