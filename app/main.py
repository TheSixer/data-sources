from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from app.api.endpoints import router
from app.middleware import api_key_middleware, exception_handler
from app.exceptions import (
    MT5ConnectionError, 
    InvalidAPIKeyError, 
    InvalidSymbolError, 
    InvalidTimeframeError, 
    DataRetrievalError,
    InsufficientDataError,
    UnsupportedIndicatorError,
    IndicatorCalculationError
)

# 创建FastAPI应用
app = FastAPI(
    title="MT5 Data Source API",
    description="MT5交易数据源API服务",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# API密钥认证已移至app.auth模块

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注释掉旧的中间件，使用新的Bearer Token认证
# app.middleware("http")(api_key_middleware)

# 注册异常处理器
app.add_exception_handler(MT5ConnectionError, exception_handler)
app.add_exception_handler(InvalidAPIKeyError, exception_handler)
app.add_exception_handler(InvalidSymbolError, exception_handler)
app.add_exception_handler(InvalidTimeframeError, exception_handler)
app.add_exception_handler(DataRetrievalError, exception_handler)
app.add_exception_handler(InsufficientDataError, exception_handler)
app.add_exception_handler(UnsupportedIndicatorError, exception_handler)
app.add_exception_handler(IndicatorCalculationError, exception_handler)

# 注册路由
app.include_router(router, prefix="/api/v1", tags=["MT5 Data"])

@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "MT5 Data Source API",
        "version": "1.0.0",
        "docs": "/docs"
    }

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=3020,
        reload=True
    )
