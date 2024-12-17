import pandas as pd
from ta.momentum import RSIIndicator, StochasticOscillator
from ta.trend import EMAIndicator, MACD
from ta.volatility import AverageTrueRange

# Đọc dữ liệu từ file CSV
file_path = "local_highs_lows.csv"  # Thay bằng đường dẫn tới file CSV của bạn
df = pd.read_csv(file_path)

# Chuyển cột 'Date' thành định dạng datetime
df['Date'] = pd.to_datetime(df['Date'])

# Tính RSI
rsi_period = 14
df['RSI'] = RSIIndicator(close=df['Close'], window=rsi_period).rsi()

# Tính EMA (12 kỳ và 26 kỳ)
ema_short_period = 12
ema_long_period = 26
df['EMA_12'] = EMAIndicator(close=df['Close'], window=ema_short_period).ema_indicator()
df['EMA_26'] = EMAIndicator(close=df['Close'], window=ema_long_period).ema_indicator()

# Tính MACD
macd = MACD(close=df['Close'], window_slow=26, window_fast=12, window_sign=9)
df['MACD'] = macd.macd()
df['MACD_Signal'] = macd.macd_signal()
df['MACD_Hist'] = macd.macd_diff()

# Tính Stochastic Oscillator
stoch_period = 14
stoch = StochasticOscillator(high=df['High'], low=df['Low'], close=df['Close'], window=stoch_period, smooth_window=3)
df['%K'] = stoch.stoch()  # %K dòng chính
df['%D'] = stoch.stoch_signal()  # %D dòng tín hiệu

# Tính ATR
atr_period = 14
atr = AverageTrueRange(high=df['High'], low=df['Low'], close=df['Close'], window=atr_period)
df['ATR'] = atr.average_true_range()

# Làm tròn các chỉ báo đến 2 chữ số thập phân
df = df.round({
    'RSI': 2,
    'EMA_12': 2,
    'EMA_26': 2,
    'MACD': 2,
    'MACD_Signal': 2,
    'MACD_Hist': 2,
    '%K': 2,
    '%D': 2,
    'ATR': 2
})

# Lưu kết quả vào file mới
output_file = "data_with_indicators.csv"
df.to_csv(output_file, index=False)
print(f"Đã lưu dữ liệu kèm chỉ báo vào {output_file}")
