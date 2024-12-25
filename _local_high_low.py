import pandas as pd
from scipy.signal import argrelextrema
import numpy as np

# Đọc dữ liệu từ file CSV
file_path = "data_with_indicators.csv"  
df = pd.read_csv(file_path)

# Chuyển cột Date sang định dạng datetime
df['Date'] = pd.to_datetime(df['Date'])

# Tham số để xác định đỉnh và đáy
n = 10  # Số phiên xung quanh để so sánh
threshold = 0.02  # Ngưỡng biến động tối thiểu (1%)

# Tìm chỉ số của đỉnh cục bộ
local_high_indices = argrelextrema(df['High'].values, comparator=lambda x, y: x > y, order=n)[0]
# Tìm chỉ số của đáy cục bộ
local_low_indices = argrelextrema(df['Low'].values, comparator=lambda x, y: x < y, order=n)[0]

# Gán nhãn mặc định là 0
df['Label'] = 2

# Gán nhãn 1 cho các đỉnh cục bộ
df.loc[local_high_indices, 'Label'] = 1

# Gán nhãn -1 cho các đáy cục bộ
df.loc[local_low_indices, 'Label'] = 0

# Lưu lại file mới với nhãn
output_file = "data_with_indicators.csv"
df.to_csv(output_file, index=False)
print(f"Dữ liệu đã được gán nhãn và lưu vào file: {output_file}")
