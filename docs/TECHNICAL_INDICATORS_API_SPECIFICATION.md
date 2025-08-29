# 技术指标API规范文档

## 📊 概述

本文档定义了自定义数据源需要支持的技术指标接口规范，以确保与技术分析工具的完全兼容。

## 🎯 支持的指标列表

### 1. 移动平均线指标 (Moving Averages)

| 指标名称 | 描述 | 参数 | 计算公式 |
|---------|------|------|----------|
| `close_50_sma` | 50日简单移动平均线 | 周期: 50 | SMA = Σ(Close) / 50 |
| `close_200_sma` | 200日简单移动平均线 | 周期: 200 | SMA = Σ(Close) / 200 |
| `close_10_ema` | 10日指数移动平均线 | 周期: 10 | EMA = Close × α + EMA(prev) × (1-α), α=2/(10+1) |

### 2. MACD指标 (MACD Indicators)

| 指标名称 | 描述 | 参数 | 计算公式 |
|---------|------|------|----------|
| `macd` | MACD主线 | 快线: 12, 慢线: 26, 信号线: 9 | MACD = EMA(12) - EMA(26) |
| `macds` | MACD信号线 | 快线: 12, 慢线: 26, 信号线: 9 | Signal = EMA(9) of MACD |
| `macdh` | MACD柱状图 | 快线: 12, 慢线: 26, 信号线: 9 | Histogram = MACD - Signal |

### 3. 动量指标 (Momentum Indicators)

| 指标名称 | 描述 | 参数 | 计算公式 |
|---------|------|------|----------|
| `rsi` | 相对强弱指数 | 周期: 14 | RSI = 100 - (100 / (1 + RS)), RS = Avg Gain / Avg Loss |

### 4. 波动率指标 (Volatility Indicators)

| 指标名称 | 描述 | 参数 | 计算公式 |
|---------|------|------|----------|
| `boll` | 布林带中轨 | 周期: 20, 标准差: 2 | Middle = SMA(20) |
| `boll_ub` | 布林带上轨 | 周期: 20, 标准差: 2 | Upper = Middle + (2 × StdDev) |
| `boll_lb` | 布林带下轨 | 周期: 20, 标准差: 2 | Lower = Middle - (2 × StdDev) |
| `atr` | 平均真实波幅 | 周期: 14 | ATR = SMA(True Range), True Range = max(High-Low, |High-PrevClose|, |Low-PrevClose|) |

### 5. 成交量指标 (Volume-Based Indicators)

| 指标名称 | 描述 | 参数 | 计算公式 |
|---------|------|------|----------|
| `vwma` | 成交量加权移动平均线 | 周期: 20 | VWMA = Σ(Close × Volume) / Σ(Volume) |
| `mfi` | 资金流量指数 | 周期: 14 | MFI = 100 - (100 / (1 + Money Flow Ratio)) |

## 📋 数据格式要求

### 输入数据格式

```json
{
  "symbol": "XAUUSD",
  "start_date": "2025-08-01",
  "end_date": "2025-08-28",
  "timeframe": "H1",
  "indicator": "close_50_sma"
}
```

### 输出数据格式

```json
{
  "symbol": "XAUUSD",
  "indicator": "close_50_sma",
  "timeframe": "H1",
  "data": [
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

## 🔧 API接口规范

### 1. 单个指标查询接口

**端点**: `POST /api/v1/technical-indicators`

**请求体**:
```json
{
  "symbol": "XAUUSD",
  "indicator": "close_50_sma",
  "start_date": "2025-08-01",
  "end_date": "2025-08-28",
  "timeframe": "H1"
}
```

**响应**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "symbol": "XAUUSD",
    "indicator": "close_50_sma",
    "timeframe": "H1",
    "values": [
      {
        "date": "2025-08-01 00:00:00",
        "value": 1973.92
      }
    ]
  }
}
```

### 2. 批量指标查询接口

**端点**: `POST /api/v1/technical-indicators/batch`

**请求体**:
```json
{
  "symbol": "XAUUSD",
  "indicators": ["close_50_sma", "rsi", "macd"],
  "start_date": "2025-08-01",
  "end_date": "2025-08-28",
  "timeframe": "H1"
}
```

**响应**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "symbol": "XAUUSD",
    "timeframe": "H1",
    "indicators": {
      "close_50_sma": [
        {
          "date": "2025-08-01 00:00:00",
          "value": 1973.92
        }
      ],
      "rsi": [
        {
          "date": "2025-08-01 00:00:00",
          "value": 65.43
        }
      ],
      "macd": [
        {
          "date": "2025-08-01 00:00:00",
          "value": 12.34
        }
      ]
    }
  }
}
```

### 3. 指标列表查询接口

**端点**: `GET /api/v1/technical-indicators/supported`

**响应**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "indicators": [
      {
        "name": "close_50_sma",
        "description": "50日简单移动平均线",
        "category": "moving_averages",
        "parameters": {
          "period": 50,
          "type": "sma"
        }
      }
    ]
  }
}
```

## 📊 数据要求

### 基础数据字段

每个K线数据必须包含以下字段：

```json
{
  "date": "2025-08-01 00:00:00",
  "open": 1973.92,
  "high": 1987.04,
  "low": 1970.23,
  "close": 1982.40,
  "volume": 4239
}
```

### 时间格式

- **日期格式**: `YYYY-MM-DD HH:mm:ss`
- **时区**: UTC
- **时间戳**: Unix timestamp (秒)

### 数值精度

- **价格数据**: 保留5位小数
- **指标值**: 保留2位小数
- **成交量**: 整数

## 🔄 计算规则

### 1. 移动平均线计算

```python
# 简单移动平均线 (SMA)
def calculate_sma(prices, period):
    return sum(prices[-period:]) / period

# 指数移动平均线 (EMA)
def calculate_ema(prices, period):
    alpha = 2 / (period + 1)
    ema = prices[0]
    for price in prices[1:]:
        ema = price * alpha + ema * (1 - alpha)
    return ema
```

### 2. MACD计算

```python
def calculate_macd(prices):
    ema12 = calculate_ema(prices, 12)
    ema26 = calculate_ema(prices, 26)
    macd_line = ema12 - ema26
    signal_line = calculate_ema([macd_line], 9)
    histogram = macd_line - signal_line
    return macd_line, signal_line, histogram
```

### 3. RSI计算

```python
def calculate_rsi(prices, period=14):
    gains = []
    losses = []
    
    for i in range(1, len(prices)):
        change = prices[i] - prices[i-1]
        if change > 0:
            gains.append(change)
            losses.append(0)
        else:
            gains.append(0)
            losses.append(abs(change))
    
    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period
    
    rs = avg_gain / avg_loss if avg_loss != 0 else 0
    rsi = 100 - (100 / (1 + rs))
    return rsi
```

## ⚠️ 注意事项

### 1. 数据完整性

- 确保有足够的历史数据来计算指标
- 对于需要预热期的指标（如SMA、EMA），确保有足够的数据点
- 处理缺失数据时，返回null或跳过该时间点

### 2. 性能优化

- 实现数据缓存机制
- 支持增量计算
- 优化大数据量的处理

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

### 4. 支持的错误码

| 错误码 | 描述 |
|--------|------|
| 4001 | 数据不足 |
| 4002 | 不支持的指标 |
| 4003 | 无效的时间范围 |
| 4004 | 无效的symbol |
| 4005 | 计算错误 |

## 🧪 测试用例

### 测试数据

```json
{
  "test_cases": [
    {
      "symbol": "XAUUSD",
      "indicator": "close_50_sma",
      "start_date": "2025-08-01",
      "end_date": "2025-08-28",
      "expected_count": 671
    },
    {
      "symbol": "XAUUSD", 
      "indicator": "rsi",
      "start_date": "2025-08-01",
      "end_date": "2025-08-28",
      "expected_range": [0, 100]
    }
  ]
}
```

## 📝 实现建议

1. **模块化设计**: 将每个指标的计算逻辑独立封装
2. **缓存策略**: 实现多级缓存（内存、Redis、数据库）
3. **异步处理**: 对于大量数据，使用异步计算
4. **监控告警**: 添加计算时间、错误率等监控指标
5. **文档完善**: 提供详细的API文档和示例代码

---

**文档版本**: v1.0  
**最后更新**: 2025-08-28  
**维护者**: HyperEcho
