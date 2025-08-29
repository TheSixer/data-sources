import os
from dotenv import load_dotenv

# 加载环境变量
try:
    load_dotenv()
except Exception:
    pass

def get_env_value(key: str, default: str) -> str:
    """安全获取环境变量值，处理占位符"""
    value = os.getenv(key, default)
    if value.startswith("your_") or value == default:
        return default
    return value

class Settings:
    """应用配置类"""
    
    def __init__(self):
        # API配置
        self.api_key = get_env_value("API_KEY", "test_api_key_123")
        
        # MT5配置
        self.mt5_login = int(get_env_value("MT5_LOGIN", "0"))
        self.mt5_password = get_env_value("MT5_PASSWORD", "")
        self.mt5_server = get_env_value("MT5_SERVER", "")
        self.mt5_timeout = int(get_env_value("MT5_TIMEOUT", "60000"))

# 全局配置实例
settings = Settings()
