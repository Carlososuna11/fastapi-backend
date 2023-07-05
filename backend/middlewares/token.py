from fastapi import (
    Depends,
    HTTPException,
    status
)
from security import HTTPToken
from pydantic import ValidationError
from schemas import TokenSchema
from conf import settings

oauth = HTTPToken()


async def get_authentication(
        token: str = Depends(oauth),
) -> TokenSchema:
    try:
        token = token.credentials.strip()
        if token != settings.TOKEN_AUTHORIZATION:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return TokenSchema(token=token)
    except ValidationError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
