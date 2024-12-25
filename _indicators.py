import pandas as pd
from ta.momentum import RSIIndicator, StochasticOscillator
from ta.trend import EMAIndicator, MACD, ADXIndicator
from ta.volatility import AverageTrueRange
from ta.trend import CCIIndicator

# Đọc dữ liệu từ file CSV
file_path = "OHLCV.csv"  # Thay bằng đường dẫn tới file CSV của bạn
df = pd.read_csv(file_path)

# Chuyển cột 'Date' thành định dạng datetime
df['Date'] = pd.to_datetime(df['Date'])

# Tính RSI
rsi_period = 14
df['RSI'] = RSIIndicator(close=df['Close'], window=rsi_period).rsi()

# Tính Stochastic Oscillator
stoch_period = 14
stoch = StochasticOscillator(high=df['High'], low=df['Low'], close=df['Close'], window=stoch_period, smooth_window=3)
df['%K'] = stoch.stoch()  # %K dòng chính
df['%D'] = stoch.stoch_signal()  # %D dòng tín hiệu

# Tính CCI
cci_period = 14
df['CCI'] = CCIIndicator(high=df['High'], low=df['Low'], close=df['Close'], window=cci_period).cci()

# Tính ADX
adx_period = 14
df['ADX'] = ADXIndicator(high=df['High'], low=df['Low'], close=df['Close'], window=adx_period).adx()

# Tính MA7 (Moving Average 7-day)
ma7_period = 7
df['MA7'] = df['Close'].rolling(window=ma7_period).mean()

# Tính cột mới theo công thức
df['MA7_Change'] = 100 * (df['MA7'] - df['MA7'].shift(1)) / df['MA7']

# Làm tròn các chỉ báo đến 2 chữ số thập phân
df = df.round({
    'RSI': 2,
    '%K': 2,
    '%D': 2,
    'CCI': 2,
    'ADX': 2,
    'MA7': 2,
    'MA7_Change': 2
})

# Lưu kết quả vào file mới
output_file = "data_with_indicators.csv"
df.to_csv(output_file, index=False)
print(f"Đã lưu dữ liệu kèm chỉ báo vào {output_file}")
