import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Optional
from app.config import settings
from app.exceptions import MT5ConnectionError, DataRetrievalError, InvalidSymbolError, InvalidTimeframeError
from app.utils import to_mt5_time, format_mt5_time_to_beijing

class MT5Service:
    """MT5服务类"""
    
    def __init__(self):
        self.connected = False
        # 初始化时不强制连接，允许服务启动
        try:
            self._connect()
        except Exception:
            # 连接失败不影响服务启动
            pass
    
    def _connect(self) -> bool:
        """连接MT5"""
        try:
            # 初始化MT5
            if not mt5.initialize():
                raise MT5ConnectionError("MT5初始化失败")
            
            # 登录MT5
            if not mt5.login(
                login=settings.mt5_login,
                password=settings.mt5_password,
                server=settings.mt5_server,
                timeout=settings.mt5_timeout
            ):
                raise MT5ConnectionError("MT5登录失败")
            
            self.connected = True
            return True
            
        except Exception as e:
            self.connected = False
            raise MT5ConnectionError(f"MT5连接失败: {str(e)}")
    
    def _get_timeframe_enum(self, timeframe: str) -> int:
        """将时间周期字符串转换为MT5枚举值"""
        timeframe_map = {
            "M1": mt5.TIMEFRAME_M1,
            "M5": mt5.TIMEFRAME_M5,
            "M15": mt5.TIMEFRAME_M15,
            "M30": mt5.TIMEFRAME_M30,
            "H1": mt5.TIMEFRAME_H1,
            "H4": mt5.TIMEFRAME_H4,
            "D1": mt5.TIMEFRAME_D1,
            "W1": mt5.TIMEFRAME_W1,
            "MN1": mt5.TIMEFRAME_MN1
        }
        
        if timeframe not in timeframe_map:
            raise InvalidTimeframeError(f"不支持的时间周期: {timeframe}")
        
        return timeframe_map[timeframe]
    
    def get_market_data(
        self, 
        symbol: str, 
        timeframe: str, 
        start_time: datetime, 
        end_time: datetime
    ) -> List[Dict]:
        """获取行情数据"""
        try:
            # 检查连接状态
            if not self.connected:
                self._connect()
            
            # 验证交易品种
            symbol_info = mt5.symbol_info(symbol)
            if symbol_info is None:
                raise InvalidSymbolError(f"无效的交易品种: {symbol}")
            
            # 获取时间周期枚举
            tf_enum = self._get_timeframe_enum(timeframe)
            
            # 时区转换：将北京时间转换为UTC时间（特殊处理）
            mt5_start_time = to_mt5_time(start_time)
            mt5_end_time = to_mt5_time(end_time)
            
            # 获取历史数据
            rates = mt5.copy_rates_range(symbol, tf_enum, mt5_start_time, mt5_end_time)
            
            if rates is None or len(rates) == 0:
                return []
            
            # 转换为DataFrame
            df = pd.DataFrame(rates)
            # MT5返回的是UTC时间戳，转换为北京时间（加5小时）
            df['time'] = pd.to_datetime(df['time'], unit='s', utc=True) + pd.Timedelta(hours=5)
            
            # 转换为字典列表
            data = []
            for _, row in df.iterrows():
                data.append({
                    "time": row['time'].strftime('%Y-%m-%dT%H:%M:%S'),
                    "open": float(row['open']),
                    "high": float(row['high']),
                    "low": float(row['low']),
                    "close": float(row['close']),
                    "tick_volume": int(row['tick_volume']),
                    "spread": int(row['spread']),
                    "real_volume": int(row['real_volume'])
                })
            
            return data
            
        except (InvalidSymbolError, InvalidTimeframeError):
            raise
        except Exception as e:
            raise DataRetrievalError(f"获取行情数据失败: {str(e)}")
    
    def is_connected(self) -> bool:
        """检查MT5连接状态"""
        return self.connected and mt5.terminal_info() is not None
    
    def disconnect(self):
        """断开MT5连接"""
        if self.connected:
            mt5.shutdown()
            self.connected = False

# 全局MT5服务实例
mt5_service = MT5Service()
