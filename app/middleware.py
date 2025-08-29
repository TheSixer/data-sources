from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from app.config import settings
from app.exceptions import InvalidAPIKeyError

async def api_key_middleware(request: Request, call_next):
    """API密钥验证中间件"""
    
    # 跳过不需要验证的路径
    skip_paths = ["/", "/docs", "/redoc", "/openapi.json", "/health"]
    if request.url.path in skip_paths:
        response = await call_next(request)
        return response
    
    # 获取API密钥
    api_key = request.headers.get("X-API-Key")
    
    # 验证API密钥
    if not api_key or api_key != settings.api_key:
        raise InvalidAPIKeyError()
    
    response = await call_next(request)
    return response

async def exception_handler(request: Request, exc: Exception):
    """全局异常处理器"""
    if isinstance(exc, HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": exc.detail,
                "status_code": exc.status_code
            }
        )
    
    # 处理其他异常
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "内部服务器错误",
            "detail": str(exc),
            "status_code": 500
        }
    )
