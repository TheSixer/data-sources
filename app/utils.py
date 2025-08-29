from datetime import datetime, timezone, timedelta
from typing import Union

def to_beijing_time(dt: Union[datetime, str]) -> datetime:
    """将时间转换为北京时间"""
    if isinstance(dt, str):
        dt = datetime.fromisoformat(dt.replace('Z', '+00:00'))
    
    # 如果时间没有时区信息，假设为UTC
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    
    # 转换为北京时间 (UTC+8)
    beijing_tz = timezone(timedelta(hours=8))
    return dt.astimezone(beijing_tz)

def to_mt5_time(dt: Union[datetime, str]) -> datetime:
    """将北京时间转换为MT5查询时间"""
    if isinstance(dt, str):
        dt = datetime.fromisoformat(dt.replace('Z', '+00:00'))
    
    # 如果时间没有时区信息，假设为北京时间
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone(timedelta(hours=8)))
    
    # 特殊处理：北京时间15:59对应UTC时间10:59（时差5小时）
    utc_time = dt - timedelta(hours=5)
    return utc_time.replace(tzinfo=timezone.utc)

def format_beijing_time(dt: datetime) -> str:
    """格式化北京时间为字符串"""
    # 如果时间没有时区信息，假设为UTC
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    
    # 转换为北京时间
    beijing_time = dt.astimezone(timezone(timedelta(hours=8)))
    return beijing_time.strftime('%Y-%m-%dT%H:%M:%S')

def format_mt5_time_to_beijing(dt: datetime) -> str:
    """将MT5时间戳转换为北京时间字符串"""
    # MT5时间戳是UTC时间，转换为北京时间
    # 特殊处理：UTC时间需要加5小时得到北京时间
    beijing_time = dt + timedelta(hours=5)
    return beijing_time.strftime('%Y-%m-%dT%H:%M:%S')

def get_beijing_now() -> datetime:
    """获取当前北京时间"""
    return datetime.now(timezone(timedelta(hours=8)))
