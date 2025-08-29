import pandas as pd
import numpy as np
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import MetaTrader5 as mt5

class TechnicalIndicatorsService:
    """技术指标计算服务"""
    
    def __init__(self):
        pass
    
    def calculate_sma(self, prices: List[float], period: int) -> List[Optional[float]]:
        """计算简单移动平均线 (SMA)"""
        if len(prices) < period:
            return [None] * len(prices)
        
        sma_values = []
        for i in range(len(prices)):
            if i < period - 1:
                sma_values.append(None)
            else:
                sma = sum(prices[i-period+1:i+1]) / period
                sma_values.append(round(sma, 2))
        
        return sma_values
    
    def calculate_ema(self, prices: List[float], period: int) -> List[Optional[float]]:
        """计算指数移动平均线 (EMA)"""
        if len(prices) < period:
            return [None] * len(prices)
        
        alpha = 2 / (period + 1)
        ema_values = []
        
        # 第一个EMA值使用前period个价格的SMA
        first_ema = sum(prices[:period]) / period
        ema_values.append(round(first_ema, 2))
        
        # 计算后续的EMA值
        for i in range(period, len(prices)):
            ema = prices[i] * alpha + ema_values[i-period] * (1 - alpha)
            ema_values.append(round(ema, 2))
        
        # 填充前面的None值
        return [None] * (period - 1) + ema_values
    
    def calculate_macd(self, prices: List[float], fast_period: int = 12, slow_period: int = 26, signal_period: int = 9) -> Dict[str, List[Optional[float]]]:
        """计算MACD指标"""
        if len(prices) < slow_period:
            return {
                'macd': [None] * len(prices),
                'macds': [None] * len(prices),
                'macdh': [None] * len(prices)
            }
        
        # 计算快线和慢线的EMA
        ema_fast = self.calculate_ema(prices, fast_period)
        ema_slow = self.calculate_ema(prices, slow_period)
        
        # 计算MACD线
        macd_line = []
        for i in range(len(prices)):
            if ema_fast[i] is not None and ema_slow[i] is not None:
                macd_line.append(round(ema_fast[i] - ema_slow[i], 2))
            else:
                macd_line.append(None)
        
        # 计算信号线 (MACD的EMA)
        # 找到第一个非None的MACD值的位置
        first_macd_idx = None
        for i, val in enumerate(macd_line):
            if val is not None:
                first_macd_idx = i
                break
        
        if first_macd_idx is None:
            return {
                'macd': macd_line,
                'macds': [None] * len(prices),
                'macdh': [None] * len(prices)
            }
        
        # 提取非None的MACD值
        macd_values = [v for v in macd_line[first_macd_idx:] if v is not None]
        
        if len(macd_values) < signal_period:
            return {
                'macd': macd_line,
                'macds': [None] * len(prices),
                'macdh': [None] * len(prices)
            }
        
        # 计算信号线
        signal_values = self.calculate_ema(macd_values, signal_period)
        
        # 构建完整的信号线
        signal_line = [None] * len(prices)
        
        # 计算信号线开始的位置
        # 第一个MACD值在第first_macd_idx位置
        # 信号线需要signal_period个MACD值才能开始计算
        signal_start_idx = first_macd_idx + signal_period - 1
        
        # 确保不越界
        for i, signal_val in enumerate(signal_values):
            if signal_val is not None and (signal_start_idx + i) < len(prices):
                signal_line[signal_start_idx + i] = signal_val
        
        # 计算柱状图
        histogram = []
        for i in range(len(prices)):
            if macd_line[i] is not None and signal_line[i] is not None:
                histogram.append(round(macd_line[i] - signal_line[i], 2))
            else:
                histogram.append(None)
        
        return {
            'macd': macd_line,
            'macds': signal_line,
            'macdh': histogram
        }
    
    def calculate_rsi(self, prices: List[float], period: int = 14) -> List[Optional[float]]:
        """计算相对强弱指数 (RSI)"""
        if len(prices) < period + 1:
            return [None] * len(prices)
        
        gains = []
        losses = []
        
        # 计算价格变化
        for i in range(1, len(prices)):
            change = prices[i] - prices[i-1]
            if change > 0:
                gains.append(change)
                losses.append(0)
            else:
                gains.append(0)
                losses.append(abs(change))
        
        rsi_values = []
        
        # 计算前period个值的平均增益和损失
        for i in range(len(prices)):
            if i < period:
                rsi_values.append(None)
            else:
                # 计算平均增益和损失
                avg_gain = sum(gains[i-period:i]) / period
                avg_loss = sum(losses[i-period:i]) / period
                
                if avg_loss == 0:
                    rsi = 100
                else:
                    rs = avg_gain / avg_loss
                    rsi = 100 - (100 / (1 + rs))
                
                rsi_values.append(round(rsi, 2))
        
        return rsi_values
    
    def calculate_bollinger_bands(self, prices: List[float], period: int = 20, std_dev: float = 2) -> Dict[str, List[Optional[float]]]:
        """计算布林带"""
        if len(prices) < period:
            return {
                'boll': [None] * len(prices),
                'boll_ub': [None] * len(prices),
                'boll_lb': [None] * len(prices)
            }
        
        # 计算中轨 (SMA)
        middle_band = self.calculate_sma(prices, period)
        
        upper_band = []
        lower_band = []
        
        for i in range(len(prices)):
            if middle_band[i] is not None:
                # 计算标准差
                start_idx = i - period + 1
                window_prices = prices[start_idx:i+1]
                std = np.std(window_prices)
                
                upper = middle_band[i] + (std_dev * std)
                lower = middle_band[i] - (std_dev * std)
                
                upper_band.append(round(upper, 2))
                lower_band.append(round(lower, 2))
            else:
                upper_band.append(None)
                lower_band.append(None)
        
        return {
            'boll': middle_band,
            'boll_ub': upper_band,
            'boll_lb': lower_band
        }
    
    def calculate_atr(self, highs: List[float], lows: List[float], closes: List[float], period: int = 14) -> List[Optional[float]]:
        """计算平均真实波幅 (ATR)"""
        if len(highs) < period + 1:
            return [None] * len(highs)
        
        true_ranges = []
        
        # 计算真实波幅
        for i in range(len(highs)):
            if i == 0:
                true_ranges.append(highs[i] - lows[i])
            else:
                tr1 = highs[i] - lows[i]
                tr2 = abs(highs[i] - closes[i-1])
                tr3 = abs(lows[i] - closes[i-1])
                true_ranges.append(max(tr1, tr2, tr3))
        
        # 计算ATR (使用SMA)
        atr_values = self.calculate_sma(true_ranges, period)
        
        return atr_values
    
    def calculate_vwma(self, prices: List[float], volumes: List[int], period: int = 20) -> List[Optional[float]]:
        """计算成交量加权移动平均线 (VWMA)"""
        if len(prices) < period or len(volumes) < period:
            return [None] * len(prices)
        
        vwma_values = []
        
        for i in range(len(prices)):
            if i < period - 1:
                vwma_values.append(None)
            else:
                # 计算加权平均
                price_volume_sum = 0
                volume_sum = 0
                
                for j in range(i - period + 1, i + 1):
                    price_volume_sum += prices[j] * volumes[j]
                    volume_sum += volumes[j]
                
                if volume_sum > 0:
                    vwma = price_volume_sum / volume_sum
                    vwma_values.append(round(vwma, 2))
                else:
                    vwma_values.append(None)
        
        return vwma_values
    
    def calculate_mfi(self, highs: List[float], lows: List[float], closes: List[float], volumes: List[int], period: int = 14) -> List[Optional[float]]:
        """计算资金流量指数 (MFI)"""
        if len(highs) < period + 1:
            return [None] * len(highs)
        
        typical_prices = []
        money_flows = []
        
        # 计算典型价格和资金流量
        for i in range(len(highs)):
            typical_price = (highs[i] + lows[i] + closes[i]) / 3
            typical_prices.append(typical_price)
            
            if i > 0:
                if typical_price > typical_prices[i-1]:
                    money_flow = typical_price * volumes[i]
                else:
                    money_flow = -typical_price * volumes[i]
                money_flows.append(money_flow)
            else:
                money_flows.append(0)
        
        mfi_values = []
        
        for i in range(len(highs)):
            if i < period:
                mfi_values.append(None)
            else:
                # 计算正负资金流量
                positive_flow = sum([mf for mf in money_flows[i-period+1:i+1] if mf > 0])
                negative_flow = abs(sum([mf for mf in money_flows[i-period+1:i+1] if mf < 0]))
                
                if negative_flow == 0:
                    mfi = 100
                else:
                    money_ratio = positive_flow / negative_flow
                    mfi = 100 - (100 / (1 + money_ratio))
                
                mfi_values.append(round(mfi, 2))
        
        return mfi_values
    
    def calculate_indicator(self, indicator_name: str, market_data: List[Dict]) -> List[Dict]:
        """根据指标名称计算对应的技术指标"""
        if not market_data:
            return []
        
        # 提取数据
        prices = [float(item['close']) for item in market_data]
        highs = [float(item['high']) for item in market_data]
        lows = [float(item['low']) for item in market_data]
        volumes = [int(item.get('tick_volume', 0)) for item in market_data]
        
        result = []
        
        if indicator_name == 'close_50_sma':
            values = self.calculate_sma(prices, 50)
        elif indicator_name == 'close_200_sma':
            values = self.calculate_sma(prices, 200)
        elif indicator_name == 'close_10_ema':
            values = self.calculate_ema(prices, 10)
        elif indicator_name == 'macd':
            macd_data = self.calculate_macd(prices)
            values = macd_data['macd']
        elif indicator_name == 'macds':
            macd_data = self.calculate_macd(prices)
            values = macd_data['macds']
        elif indicator_name == 'macdh':
            macd_data = self.calculate_macd(prices)
            values = macd_data['macdh']
        elif indicator_name == 'rsi':
            values = self.calculate_rsi(prices, 14)
        elif indicator_name == 'boll':
            bb_data = self.calculate_bollinger_bands(prices, 20, 2)
            values = bb_data['boll']
        elif indicator_name == 'boll_ub':
            bb_data = self.calculate_bollinger_bands(prices, 20, 2)
            values = bb_data['boll_ub']
        elif indicator_name == 'boll_lb':
            bb_data = self.calculate_bollinger_bands(prices, 20, 2)
            values = bb_data['boll_lb']
        elif indicator_name == 'atr':
            values = self.calculate_atr(highs, lows, prices, 14)
        elif indicator_name == 'vwma':
            values = self.calculate_vwma(prices, volumes, 20)
        elif indicator_name == 'mfi':
            values = self.calculate_mfi(highs, lows, prices, volumes, 14)
        else:
            raise ValueError(f"不支持的指标: {indicator_name}")
        
        # 构建结果
        for i, item in enumerate(market_data):
            result.append({
                "date": item['time'],
                "value": values[i],
                "timestamp": int(datetime.fromisoformat(item['time']).timestamp())
            })
        
        return result

# 全局技术指标服务实例
technical_indicators_service = TechnicalIndicatorsService()
