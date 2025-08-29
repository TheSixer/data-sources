from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status
from app.config import settings

security = HTTPBearer()

async def get_api_key(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """验证API密钥"""
    if credentials.credentials != settings.api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的API密钥，请在请求头中添加有效的Bearer Token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials.credentials
