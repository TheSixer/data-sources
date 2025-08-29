# 技术指标API使用示例

## 📊 概述

本文档提供了MT5数据源技术指标API的详细使用示例，包括单个指标查询、批量指标查询和指标列表获取。

## 🔧 API端点

### 基础URL
```
http://localhost:3020/api/v1
```

### 认证
所有技术指标API都需要API密钥认证，请在请求头中添加：
```
Authorization: Bearer your_api_key_here
```

## 📈 使用示例

### 1. 获取单个技术指标

#### 请求示例

```bash
curl -X POST "http://localhost:3020/api/v1/technical-indicators" \
  -H "Authorization: Bearer your_api_key_here" \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "XAUUSD",
    "indicator": "close_50_sma",
    "start_date": "2025-08-01",
    "end_date": "2025-08-28",
    "timeframe": "H1"
  }'
```

#### Python示例

```python
import requests
import json

url = "http://localhost:3020/api/v1/technical-indicators"
headers = {
    "Authorization": "Bearer your_api_key_here",
    "Content-Type": "application/json"
}
data = {
    "symbol": "XAUUSD",
    "indicator": "close_50_sma",
    "start_date": "2025-08-01",
    "end_date": "2025-08-28",
    "timeframe": "H1"
}

response = requests.post(url, headers=headers, json=data)
result = response.json()
print(json.dumps(result, indent=2))
```

#### 响应示例

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
    },
    {
      "date": "2025-08-01 01:00:00",
      "value": 1975.45,
      "timestamp": 1735693200
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

### 2. 批量获取技术指标

#### 请求示例

```bash
curl -X POST "http://localhost:3020/api/v1/technical-indicators/batch" \
  -H "Authorization: Bearer your_api_key_here" \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "XAUUSD",
    "indicators": ["close_50_sma", "rsi", "macd"],
    "start_date": "2025-08-01",
    "end_date": "2025-08-28",
    "timeframe": "H1"
  }'
```

#### Python示例

```python
import requests
import json

url = "http://localhost:3020/api/v1/technical-indicators/batch"
headers = {
    "Authorization": "Bearer your_api_key_here",
    "Content-Type": "application/json"
}
data = {
    "symbol": "XAUUSD",
    "indicators": ["close_50_sma", "rsi", "macd"],
    "start_date": "2025-08-01",
    "end_date": "2025-08-28",
    "timeframe": "H1"
}

response = requests.post(url, headers=headers, json=data)
result = response.json()
print(json.dumps(result, indent=2))
```

#### 响应示例

```json
{
  "symbol": "XAUUSD",
  "timeframe": "H1",
  "indicators": {
    "close_50_sma": [
      {
        "date": "2025-08-01 00:00:00",
        "value": 1973.92,
        "timestamp": 1735689600
      }
    ],
    "rsi": [
      {
        "date": "2025-08-01 00:00:00",
        "value": 65.43,
        "timestamp": 1735689600
      }
    ],
    "macd": [
      {
        "date": "2025-08-01 00:00:00",
        "value": 12.34,
        "timestamp": 1735689600
      }
    ]
  }
}
```

### 3. 获取支持的指标列表

#### 请求示例

```bash
curl -X GET "http://localhost:3020/api/v1/technical-indicators/supported" \
  -H "Authorization: Bearer your_api_key_here"
```

#### Python示例

```python
import requests
import json

url = "http://localhost:3020/api/v1/technical-indicators/supported"
headers = {
    "Authorization": "Bearer your_api_key_here"
}

response = requests.get(url, headers=headers)
result = response.json()
print(json.dumps(result, indent=2))
```

#### 响应示例

```json
{
  "indicators": [
    {
      "name": "close_50_sma",
      "description": "50日简单移动平均线",
      "category": "moving_averages",
      "parameters": {
        "period": 50,
        "type": "sma"
      }
    },
    {
      "name": "rsi",
      "description": "相对强弱指数",
      "category": "momentum_indicators",
      "parameters": {
        "period": 14
      }
    }
  ]
}
```

## 📊 指标分类

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

## ⚠️ 注意事项

### 1. 数据要求
- 确保有足够的历史数据来计算指标
- 对于需要预热期的指标（如SMA、EMA），确保有足够的数据点
- 处理缺失数据时，返回null或跳过该时间点

### 2. 时间格式
- 日期格式：`YYYY-MM-DD`
- 时间格式：`YYYY-MM-DD HH:mm:ss`
- 时区：北京时间

### 3. 错误处理
```json
{
  "code": 4001,
  "message": "Insufficient data for calculation",
  "data": {
    "required_periods": 50,
    "available_periods": 30,
    "indicator": "close_50_sma"
  }
}
```

### 4. 性能优化
- 对于大量数据，建议使用批量查询接口
- 实现数据缓存机制以提高性能
- 支持增量计算

## 🔍 常见问题

### Q: 为什么某些指标返回null值？
A: 这是因为数据不足或处于指标计算的预热期。例如，50日SMA需要至少50个数据点才能开始计算。

### Q: 如何处理时区问题？
A: 所有时间都使用北京时间，API会自动处理时区转换。

### Q: 批量查询失败怎么办？
A: 批量查询中如果某个指标计算失败，会返回空数组，其他指标正常返回。

### Q: 如何获取最新的指标值？
A: 使用当前日期作为end_date，API会返回最新的指标值。

---

**文档版本**: v1.0  
**更新日期**: 2025-08-28  
**维护者**: HyperEcho
