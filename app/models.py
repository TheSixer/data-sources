from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class TimeframeEnum(str, Enum):
    """时间周期枚举"""
    M1 = "M1"
    M5 = "M5"
    M15 = "M15"
    M30 = "M30"
    H1 = "H1"
    H4 = "H4"
    D1 = "D1"
    W1 = "W1"
    MN1 = "MN1"

class MarketDataRequest(BaseModel):
    """行情数据请求模型"""
    symbol: str = Field(..., description="交易品种", example="EURUSD")
    timeframe: TimeframeEnum = Field(..., description="时间周期", example="H1")
    start_time: datetime = Field(..., description="开始时间", example="2024-01-01T00:00:00")
    end_time: datetime = Field(..., description="结束时间", example="2024-01-02T00:00:00")

class MarketDataResponse(BaseModel):
    """行情数据响应模型"""
    symbol: str
    timeframe: str
    data: List[dict]
    count: int
    start_time: datetime
    end_time: datetime

class ErrorResponse(BaseModel):
    """错误响应模型"""
    error: str
    detail: str
    status_code: int

class HealthResponse(BaseModel):
    """健康检查响应模型"""
    status: str
    mt5_connected: bool
    timestamp: datetime

# 技术指标相关模型
class TechnicalIndicatorRequest(BaseModel):
    """技术指标请求模型"""
    symbol: str = Field(..., description="交易品种", example="XAUUSD")
    indicator: str = Field(..., description="技术指标名称", example="close_50_sma")
    start_date: str = Field(..., description="开始日期", example="2025-08-01")
    end_date: str = Field(..., description="结束日期", example="2025-08-28")
    timeframe: TimeframeEnum = Field(..., description="时间周期", example="H1")

class TechnicalIndicatorValue(BaseModel):
    """技术指标值模型"""
    date: str = Field(..., description="日期时间", example="2025-08-01 00:00:00")
    value: Optional[float] = Field(..., description="指标值", example=1973.92)
    timestamp: int = Field(..., description="时间戳", example=1735689600)

class TechnicalIndicatorResponse(BaseModel):
    """技术指标响应模型"""
    symbol: str = Field(..., description="交易品种")
    indicator: str = Field(..., description="技术指标名称")
    timeframe: str = Field(..., description="时间周期")
    values: List[TechnicalIndicatorValue] = Field(..., description="指标值列表")
    metadata: Dict[str, Any] = Field(..., description="元数据")

class BatchTechnicalIndicatorRequest(BaseModel):
    """批量技术指标请求模型"""
    symbol: str = Field(..., description="交易品种", example="XAUUSD")
    indicators: List[str] = Field(..., description="技术指标名称列表", example=["close_50_sma", "rsi", "macd"])
    start_date: str = Field(..., description="开始日期", example="2025-08-01")
    end_date: str = Field(..., description="结束日期", example="2025-08-28")
    timeframe: TimeframeEnum = Field(..., description="时间周期", example="H1")

class BatchTechnicalIndicatorResponse(BaseModel):
    """批量技术指标响应模型"""
    symbol: str = Field(..., description="交易品种")
    timeframe: str = Field(..., description="时间周期")
    indicators: Dict[str, List[TechnicalIndicatorValue]] = Field(..., description="指标值字典")

class SupportedIndicator(BaseModel):
    """支持的指标信息模型"""
    name: str = Field(..., description="指标名称")
    description: str = Field(..., description="指标描述")
    category: str = Field(..., description="指标分类")
    parameters: Dict[str, Any] = Field(..., description="指标参数")

class SupportedIndicatorsResponse(BaseModel):
    """支持的指标列表响应模型"""
    indicators: List[SupportedIndicator] = Field(..., description="支持的指标列表")
