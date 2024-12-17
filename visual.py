import pandas as pd
import matplotlib.pyplot as plt

# Đọc dữ liệu từ file CSV
file_path = "OHLCV.csv"  # Đường dẫn tới file CSV của bạn
df = pd.read_csv(file_path)

# Chuyển cột 'Date' thành kiểu datetime
df['Date'] = pd.to_datetime(df['Date'])

# Chỉ lấy 200 bản ghi thời gian gần nhất
df = df.tail(200)

# Tạo biểu đồ trực quan hóa
plt.figure(figsize=(14, 8))

# Vẽ biểu đồ giá đóng cửa
plt.plot(df['Date'], df['Close'], label='Close Price', color='blue', linewidth=1.5)

# Thiết lập tiêu đề và các nhãn
plt.title("Biểu đồ OHLCV", fontsize=16)
plt.xlabel("Ngày", fontsize=12)
plt.ylabel("Giá", fontsize=12)
plt.legend(fontsize=12)
plt.grid(alpha=0.3)

# Hiển thị biểu đồ
plt.show()
