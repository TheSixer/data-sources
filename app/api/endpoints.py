from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any
from app.utils import get_beijing_now

from app.models import (
    MarketDataRequest, 
    MarketDataResponse, 
    HealthResponse,
    TimeframeEnum,
    TechnicalIndicatorRequest,
    TechnicalIndicatorResponse,
    TechnicalIndicatorValue,
    BatchTechnicalIndicatorRequest,
    BatchTechnicalIndicatorResponse,
    SupportedIndicator,
    SupportedIndicatorsResponse
)
from app.services.mt5_service import mt5_service
from app.services.technical_indicators import technical_indicators_service
from app.exceptions import (
    MT5ConnectionError, 
    DataRetrievalError, 
    InvalidSymbolError, 
    InvalidTimeframeError,
    InsufficientDataError,
    UnsupportedIndicatorError,
    IndicatorCalculationError
)
from app.auth import get_api_key

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """健康检查接口"""
    try:
        mt5_connected = mt5_service.is_connected()
        # 返回北京时间
        beijing_time = get_beijing_now()
        return HealthResponse(
            status="healthy",
            mt5_connected=mt5_connected,
            timestamp=beijing_time
        )
    except Exception as e:
        # 返回北京时间
        beijing_time = get_beijing_now()
        return HealthResponse(
            status="unhealthy",
            mt5_connected=False,
            timestamp=beijing_time
        )

@router.post("/market-data", response_model=MarketDataResponse, dependencies=[Depends(get_api_key)])
async def get_market_data(request: MarketDataRequest):
    """获取行情数据接口"""
    try:
        # 获取行情数据
        data = mt5_service.get_market_data(
            symbol=request.symbol,
            timeframe=request.timeframe.value,
            start_time=request.start_time,
            end_time=request.end_time
        )
        
        return MarketDataResponse(
            symbol=request.symbol,
            timeframe=request.timeframe.value,
            data=data,
            count=len(data),
            start_time=request.start_time,
            end_time=request.end_time
        )
        
    except (InvalidSymbolError, InvalidTimeframeError, DataRetrievalError) as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"获取行情数据失败: {str(e)}"
        )

@router.get("/symbols", dependencies=[Depends(get_api_key)])
async def get_symbols():
    """获取可用交易品种列表"""
    try:
        if not mt5_service.is_connected():
            raise MT5ConnectionError()
        
        import MetaTrader5 as mt5
        symbols = mt5.symbols_get()
        
        if symbols is None:
            return {"symbols": []}
        
        symbol_list = [symbol.name for symbol in symbols]
        return {"symbols": symbol_list}
        
    except MT5ConnectionError as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"获取交易品种列表失败: {str(e)}"
        )

@router.get("/timeframes", dependencies=[Depends(get_api_key)])
async def get_timeframes():
    """获取支持的时间周期列表"""
    timeframes = [tf.value for tf in TimeframeEnum]
    return {"timeframes": timeframes}

# 技术指标相关接口
@router.post("/technical-indicators", response_model=TechnicalIndicatorResponse, dependencies=[Depends(get_api_key)])
async def get_technical_indicator(request: TechnicalIndicatorRequest):
    """获取单个技术指标数据"""
    try:
        # 转换日期格式
        start_time = datetime.fromisoformat(f"{request.start_date}T00:00:00")
        end_time = datetime.fromisoformat(f"{request.end_date}T23:59:59")
        
        # 获取行情数据
        market_data = mt5_service.get_market_data(
            symbol=request.symbol,
            timeframe=request.timeframe.value,
            start_time=start_time,
            end_time=end_time
        )
        
        if not market_data:
            raise InsufficientDataError("没有获取到行情数据")
        
        # 验证数据量是否足够计算指标
        required_period = _get_indicator_period(request.indicator)
        if len(market_data) < required_period:
            raise InsufficientDataError(f"数据不足，需要至少{required_period}个数据点，当前只有{len(market_data)}个")
        
        # 计算技术指标
        indicator_values = technical_indicators_service.calculate_indicator(
            request.indicator, 
            market_data
        )
        
        # 过滤掉None值
        filtered_values = [
            TechnicalIndicatorValue(
                date=item["date"],
                value=item["value"],
                timestamp=item["timestamp"]
            )
            for item in indicator_values
            if item["value"] is not None
        ]
        
        # 构建元数据
        metadata = {
            "calculation_period": _get_indicator_period(request.indicator),
            "total_points": len(filtered_values),
            "start_date": request.start_date,
            "end_date": request.end_date
        }
        
        return TechnicalIndicatorResponse(
            symbol=request.symbol,
            indicator=request.indicator,
            timeframe=request.timeframe.value,
            values=filtered_values,
            metadata=metadata
        )
        
    except (InsufficientDataError, UnsupportedIndicatorError, IndicatorCalculationError) as e:
        raise e
    except ValueError as e:
        raise UnsupportedIndicatorError(str(e))
    except Exception as e:
        # 添加更详细的错误日志
        import logging
        logging.error(f"技术指标计算失败 - 品种: {request.symbol}, 指标: {request.indicator}, 错误: {str(e)}")
        raise IndicatorCalculationError(f"计算技术指标失败: {str(e)}")

@router.post("/technical-indicators/batch", response_model=BatchTechnicalIndicatorResponse, dependencies=[Depends(get_api_key)])
async def get_batch_technical_indicators(request: BatchTechnicalIndicatorRequest):
    """批量获取技术指标数据"""
    try:
        # 转换日期格式
        start_time = datetime.fromisoformat(f"{request.start_date}T00:00:00")
        end_time = datetime.fromisoformat(f"{request.end_date}T23:59:59")
        
        # 获取行情数据
        market_data = mt5_service.get_market_data(
            symbol=request.symbol,
            timeframe=request.timeframe.value,
            start_time=start_time,
            end_time=end_time
        )
        
        if not market_data:
            raise InsufficientDataError("没有获取到行情数据")
        
        # 计算所有指标
        indicators_data = {}
        for indicator in request.indicators:
            try:
                indicator_values = technical_indicators_service.calculate_indicator(
                    indicator, 
                    market_data
                )
                
                # 过滤掉None值
                filtered_values = [
                    TechnicalIndicatorValue(
                        date=item["date"],
                        value=item["value"],
                        timestamp=item["timestamp"]
                    )
                    for item in indicator_values
                    if item["value"] is not None
                ]
                
                indicators_data[indicator] = filtered_values
                
            except Exception as e:
                # 如果某个指标计算失败，记录错误但继续处理其他指标
                indicators_data[indicator] = []
        
        return BatchTechnicalIndicatorResponse(
            symbol=request.symbol,
            timeframe=request.timeframe.value,
            indicators=indicators_data
        )
        
    except InsufficientDataError as e:
        raise e
    except Exception as e:
        raise IndicatorCalculationError(f"批量计算技术指标失败: {str(e)}")

@router.get("/technical-indicators/supported", response_model=SupportedIndicatorsResponse, dependencies=[Depends(get_api_key)])
async def get_supported_indicators():
    """获取支持的指标列表"""
    supported_indicators = [
        SupportedIndicator(
            name="close_50_sma",
            description="50日简单移动平均线",
            category="moving_averages",
            parameters={"period": 50, "type": "sma"}
        ),
        SupportedIndicator(
            name="close_200_sma",
            description="200日简单移动平均线",
            category="moving_averages",
            parameters={"period": 200, "type": "sma"}
        ),
        SupportedIndicator(
            name="close_10_ema",
            description="10日指数移动平均线",
            category="moving_averages",
            parameters={"period": 10, "type": "ema"}
        ),
        SupportedIndicator(
            name="macd",
            description="MACD主线",
            category="macd_indicators",
            parameters={"fast_period": 12, "slow_period": 26, "signal_period": 9}
        ),
        SupportedIndicator(
            name="macds",
            description="MACD信号线",
            category="macd_indicators",
            parameters={"fast_period": 12, "slow_period": 26, "signal_period": 9}
        ),
        SupportedIndicator(
            name="macdh",
            description="MACD柱状图",
            category="macd_indicators",
            parameters={"fast_period": 12, "slow_period": 26, "signal_period": 9}
        ),
        SupportedIndicator(
            name="rsi",
            description="相对强弱指数",
            category="momentum_indicators",
            parameters={"period": 14}
        ),
        SupportedIndicator(
            name="boll",
            description="布林带中轨",
            category="volatility_indicators",
            parameters={"period": 20, "std_dev": 2}
        ),
        SupportedIndicator(
            name="boll_ub",
            description="布林带上轨",
            category="volatility_indicators",
            parameters={"period": 20, "std_dev": 2}
        ),
        SupportedIndicator(
            name="boll_lb",
            description="布林带下轨",
            category="volatility_indicators",
            parameters={"period": 20, "std_dev": 2}
        ),
        SupportedIndicator(
            name="atr",
            description="平均真实波幅",
            category="volatility_indicators",
            parameters={"period": 14}
        ),
        SupportedIndicator(
            name="vwma",
            description="成交量加权移动平均线",
            category="volume_indicators",
            parameters={"period": 20}
        ),
        SupportedIndicator(
            name="mfi",
            description="资金流量指数",
            category="volume_indicators",
            parameters={"period": 14}
        )
    ]
    
    return SupportedIndicatorsResponse(indicators=supported_indicators)

def _get_indicator_period(indicator_name: str) -> int:
    """获取指标的周期参数"""
    period_map = {
        "close_50_sma": 50,
        "close_200_sma": 200,
        "close_10_ema": 10,
        "macd": 26,
        "macds": 26,
        "macdh": 26,
        "rsi": 14,
        "boll": 20,
        "boll_ub": 20,
        "boll_lb": 20,
        "atr": 14,
        "vwma": 20,
        "mfi": 14
    }
    return period_map.get(indicator_name, 0)
