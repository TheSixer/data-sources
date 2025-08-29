# MT5 Data Source API

基于FastAPI框架的MT5交易数据源API服务，提供标准化的RESTful接口获取MT5行情数据。

## 功能特性

- 🔐 API密钥认证
- 📊 多时间周期行情数据获取
- 🏗️ 模块化企业级架构
- ⚡ 高性能异步处理
- 🛡️ 完善的异常处理机制
- 📚 自动生成API文档

## 项目结构

```
data-source/
├── app/
│   ├── __init__.py
│   ├── main.py              # 主应用入口
│   ├── config.py            # 配置管理
│   ├── models.py            # 数据模型
│   ├── exceptions.py        # 自定义异常
│   ├── middleware.py        # 中间件
│   ├── api/
│   │   ├── __init__.py
│   │   └── endpoints.py     # API端点
│   └── services/
│       ├── __init__.py
│       └── mt5_service.py   # MT5服务
├── requirements.txt         # 依赖包
├── env.example             # 环境变量示例
└── README.md               # 项目说明
```

## 🚀 快速部署

### 方法1: 一键自动化部署 (推荐)

1. **获取GitHub Token**
   - 访问 [GitHub Settings > Developer settings > Personal access tokens](https://github.com/settings/tokens)
   - 生成新的token，选择权限: `repo`, `workflow`

2. **运行一键部署脚本**
   ```bash
   python deploy.py YOUR_GITHUB_TOKEN
   ```

### 方法2: 手动部署

#### 1. 创建虚拟环境

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows
```

#### 2. 安装依赖

```bash
pip install -r requirements.txt
```

#### 3. 配置环境变量

复制 `env.example` 为 `.env` 并配置：

```bash
cp env.example .env
```

编辑 `.env` 文件：

```env
# API Configuration
API_KEY=your_api_key_here

# MT5 Configuration
MT5_LOGIN=your_mt5_login
MT5_PASSWORD=your_mt5_password
MT5_SERVER=your_mt5_server
MT5_TIMEOUT=60000
```

#### 4. 启动服务

```bash
python -m app.main
```

或使用uvicorn：

```bash
uvicorn app.main:app --host 0.0.0.0 --port 3020 --reload
```

## 🌐 生产环境部署

### 自动化部署到Windows Server

本项目支持自动化部署到Windows Server (47.116.221.184)：

1. **设置GitHub Secrets**
   ```bash
   python scripts/setup_github_secrets.py TheSixer data-source YOUR_GITHUB_TOKEN
   ```

2. **初始化服务器**
   ```bash
   python scripts/server_setup.py 47.116.221.184 root Longjia@3713
   ```

3. **推送代码触发部署**
   ```bash
   git add .
   git commit -m "feat: 添加自动化部署配置"
   git push origin main
   ```

4. **监控部署进度**
   ```bash
   python scripts/deploy_monitor.py TheSixer data-source
   ```

5. **测试部署结果**
   ```bash
   python scripts/test_deployment.py
   ```

### 部署信息

- **生产环境**: http://47.116.221.184:3020
- **API文档**: http://47.116.221.184:3020/docs
- **监控页面**: https://github.com/TheSixer/data-source/actions

📖 **详细部署指南**: 请查看 [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

## API接口

### 基础信息

- **服务地址**: http://localhost:3020
- **API文档**: http://localhost:3020/docs
- **ReDoc文档**: http://localhost:3020/redoc

### 接口列表

#### 1. 健康检查

```http
GET /api/v1/health
```

**响应示例**:
```json
{
  "status": "healthy",
  "mt5_connected": true,
  "timestamp": "2024-01-01T12:00:00"
}
```

#### 2. 获取行情数据

```http
POST /api/v1/market-data
X-API-Key: your_api_key_here
Content-Type: application/json

{
  "symbol": "EURUSD",
  "timeframe": "H1",
  "start_time": "2024-01-01T00:00:00",
  "end_time": "2024-01-02T00:00:00"
}
```

**响应示例**:
```json
{
  "symbol": "EURUSD",
  "timeframe": "H1",
  "data": [
    {
      "time": "2024-01-01T00:00:00",
      "open": 1.1234,
      "high": 1.1250,
      "low": 1.1220,
      "close": 1.1240,
      "tick_volume": 1000,
      "spread": 10,
      "real_volume": 100
    }
  ],
  "count": 1,
  "start_time": "2024-01-01T00:00:00",
  "end_time": "2024-01-02T00:00:00"
}
```

#### 3. 获取交易品种列表

```http
GET /api/v1/symbols
X-API-Key: your_api_key_here
```

#### 4. 获取支持的时间周期

```http
GET /api/v1/timeframes
X-API-Key: your_api_key_here
```

#### 5. 获取技术指标数据

```http
POST /api/v1/technical-indicators
X-API-Key: your_api_key_here
Content-Type: application/json

{
  "symbol": "XAUUSD",
  "indicator": "close_50_sma",
  "start_date": "2025-08-01",
  "end_date": "2025-08-28",
  "timeframe": "H1"
}
```

**响应示例**:
```json
{
  "symbol": "XAUUSD",
  "indicator": "close_50_sma",
  "timeframe": "H1",
  "values": [
    {
      "date": "2025-08-01 00:00:00",
      "value": 1973.92,
      "timestamp": 1735689600
    }
  ],
  "metadata": {
    "calculation_period": 50,
    "total_points": 671,
    "start_date": "2025-08-01",
    "end_date": "2025-08-28"
  }
}
```

#### 6. 批量获取技术指标数据

```http
POST /api/v1/technical-indicators/batch
X-API-Key: your_api_key_here
Content-Type: application/json

{
  "symbol": "XAUUSD",
  "indicators": ["close_50_sma", "rsi", "macd"],
  "start_date": "2025-08-01",
  "end_date": "2025-08-28",
  "timeframe": "H1"
}
```

#### 7. 获取支持的指标列表

```http
GET /api/v1/technical-indicators/supported
X-API-Key: your_api_key_here
```

## 支持的时间周期

- M1: 1分钟
- M5: 5分钟
- M15: 15分钟
- M30: 30分钟
- H1: 1小时
- H4: 4小时
- D1: 1天
- W1: 1周
- MN1: 1月

## 支持的技术指标

### 移动平均线指标
- `close_50_sma` - 50日简单移动平均线
- `close_200_sma` - 200日简单移动平均线
- `close_10_ema` - 10日指数移动平均线

### MACD指标
- `macd` - MACD主线 (12,26,9)
- `macds` - MACD信号线 (12,26,9)
- `macdh` - MACD柱状图 (12,26,9)

### 动量指标
- `rsi` - 相对强弱指数 (14周期)

### 波动率指标
- `boll` - 布林带中轨 (20周期)
- `boll_ub` - 布林带上轨 (20周期, 2标准差)
- `boll_lb` - 布林带下轨 (20周期, 2标准差)
- `atr` - 平均真实波幅 (14周期)

### 成交量指标
- `vwma` - 成交量加权移动平均线 (20周期)
- `mfi` - 资金流量指数 (14周期)

## 错误处理

API使用标准HTTP状态码和统一的错误响应格式：

```json
{
  "error": "错误描述",
  "detail": "详细错误信息",
  "status_code": 400
}
```

常见错误码：
- `401`: API密钥无效
- `400`: 请求参数错误
- `503`: MT5连接失败
- `500`: 服务器内部错误

## 开发说明

### 代码规范

- 遵循PEP 8 Python代码规范
- 使用类型注解
- 完善的文档字符串
- 模块化设计

### 扩展开发

1. 在 `app/services/` 中添加新的服务类
2. 在 `app/api/endpoints.py` 中添加新的接口
3. 在 `app/models.py` 中定义新的数据模型
4. 在 `app/exceptions.py` 中添加新的异常类

## 许可证

MIT License
