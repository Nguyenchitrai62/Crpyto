import pandas as pd
from scipy.signal import argrelextrema
import numpy as np

file_path = "OHLCV.csv"  
df = pd.read_csv(file_path)


df['Date'] = pd.to_datetime(df['Date'])

n = 10  # Số ngày xung quanh để so sánh
threshold = 0.01  # Ngưỡng biến động tối thiểu (2%)

# Xác định đỉnh cục bộ (Local High)
df['Local_High'] = df['High'][argrelextrema(df['High'].values, comparator=lambda x, y: x > y, order=n)[0]]
df['Is_Local_High'] = (df['High'] == df['Local_High']) & (df['High'] > (1 + threshold) * df['High'].rolling(n).mean())

# Xác định đáy cục bộ (Local Low)
df['Local_Low'] = df['Low'][argrelextrema(df['Low'].values, comparator=lambda x, y: x < y, order=n)[0]]
df['Is_Local_Low'] = (df['Low'] == df['Local_Low']) & (df['Low'] < (1 - threshold) * df['Low'].rolling(n).mean())

# Lọc kết quả
local_highs = df[df['Is_Local_High']]
local_lows = df[df['Is_Local_Low']]

print("Các đỉnh cục bộ:")
print(local_highs[['Date', 'High']])

print("\nCác đáy cục bộ:")
print(local_lows[['Date', 'Low']])

output_file = "local_highs_lows.csv"
df.to_csv(output_file, index=False)
print(f"Dữ liệu đã được lưu vào file: {output_file}")
