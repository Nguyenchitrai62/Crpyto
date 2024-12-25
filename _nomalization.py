import pandas as pd

# Đọc dữ liệu từ file CSV
file_path = "data_with_indicators.csv"  # Đường dẫn file CSV của bạn
df = pd.read_csv(file_path)

# Chuẩn hóa dữ liệud:\Download\lstm_model.h5
df['RSI'] = df['RSI'] / 100  # Chia RSI cho 100
df['%K'] = df['%K'] / 100  # Chia %K cho 100
df['%D'] = df['%D'] / 100  # Chia %D cho 100
df['ADX'] = df['ADX'] / 100  # Chia ADX cho 100

# Chuẩn hóa CCI về khoảng [0, 1] với CCI max = 500 và CCI min = -500
cci_max = 500
cci_min = -500
df['CCI'] = (df['CCI'] - cci_min) / (cci_max - cci_min)

# Loại bỏ các dòng có ADX = 0
df = df[df['ADX'] != 0]

df = df.round({
    'RSI': 4,
    '%K': 4,
    '%D': 4,
    'CCI': 4,
    'ADX': 4
})

# Lưu lại dữ liệu đã chuẩn hóa vào file CSV mới
output_file = "data_with_indicators.csv"
df.to_csv(output_file, index=False)

print(f"File đã được lưu vào {output_file}")
