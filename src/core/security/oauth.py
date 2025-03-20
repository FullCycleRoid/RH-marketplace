from typing import Dict, Optional

from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security import APIKeyCookie, OAuth2
from jose import JWTError, jwt
from starlette.requests import Request

from src.auth.config import auth_config
from src.auth.exceptions import AuthorizationFailed


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
