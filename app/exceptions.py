from fastapi import HTTPException, status

class MT5ConnectionError(HTTPException):
    """MT5连接异常"""
    def __init__(self, detail: str = "MT5连接失败"):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=detail
        )

class InvalidAPIKeyError(HTTPException):
    """无效API密钥异常"""
    def __init__(self, detail: str = "无效的API密钥"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail
        )

class InvalidSymbolError(HTTPException):
    """无效交易品种异常"""
    def __init__(self, detail: str = "无效的交易品种"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )

class InvalidTimeframeError(HTTPException):
    """无效时间周期异常"""
    def __init__(self, detail: str = "无效的时间周期"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )

class DataRetrievalError(HTTPException):
    """数据获取异常"""
    def __init__(self, detail: str = "数据获取失败"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail
        )

# 技术指标相关异常
class InsufficientDataError(HTTPException):
    """数据不足异常"""
    def __init__(self, detail: str = "数据不足，无法计算指标"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )

class UnsupportedIndicatorError(HTTPException):
    """不支持的指标异常"""
    def __init__(self, detail: str = "不支持的指标"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )

class IndicatorCalculationError(HTTPException):
    """指标计算异常"""
    def __init__(self, detail: str = "指标计算失败"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail
        )
