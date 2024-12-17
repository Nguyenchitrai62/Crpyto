import pandas as pd

# Đọc file OHLCV (BTC/USDT)
df_ohlcv = pd.read_csv('OHLCV.csv')

# Đọc file Fear and Greed
df_fng = pd.read_csv('fear_and_greed.csv')

# Chuyển đổi cột 'Date' và 'timestamp' sang định dạng datetime
df_ohlcv['Date'] = pd.to_datetime(df_ohlcv['Date'])
df_fng['timestamp'] = pd.to_datetime(df_fng['timestamp'])

# Gộp hai DataFrame theo cột 'Date' và 'timestamp'
df_merged = pd.merge(df_ohlcv, df_fng, left_on='Date', right_on='timestamp', how='inner')

# Xóa cột 'timestamp' (không cần thiết nữa sau khi đã gộp)
df_merged = df_merged.drop(columns=['timestamp'])

# Lưu dữ liệu vào file CSV mới
df_merged.to_csv('merged_data.csv', index=False)

print("Dữ liệu đã được gộp và lưu vào file merged_data.csv")
