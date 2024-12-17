import pandas as pd
import matplotlib.pyplot as plt

# Đọc dữ liệu từ file CSV
file_path = "local_highs_lows.csv"  # Đường dẫn tới file CSV của bạn
df = pd.read_csv(file_path)

# Chuyển cột 'Date' thành kiểu datetime
df['Date'] = pd.to_datetime(df['Date'])

# Chỉ lấy 200 bản ghi thời gian gần nhất
df = df.tail(200)

# Lọc các điểm là đỉnh và đáy cục bộ
local_highs = df[df['Is_Local_High'] == True]
local_lows = df[df['Is_Local_Low'] == True]

# Tạo biểu đồ trực quan hóa
plt.figure(figsize=(14, 8))

# Vẽ biểu đồ giá đóng cửa
plt.plot(df['Date'], df['Close'], label='Close Price', color='blue', linewidth=1.5)

# Đánh dấu các đỉnh cục bộ (màu xanh)
plt.scatter(
    local_highs['Date'], 
    local_highs['Local_High'], 
    label='Local Highs', 
    color='green', 
    marker='^', 
    s=100, 
    edgecolors='black'
)

# Đánh dấu các đáy cục bộ (màu đỏ)
plt.scatter(
    local_lows['Date'], 
    local_lows['Local_Low'], 
    label='Local Lows', 
    color='red', 
    marker='v', 
    s=100, 
    edgecolors='black'
)

# Thiết lập tiêu đề và các nhãn
plt.title("Biểu đồ OHLCV với các Đỉnh và Đáy Cục Bộ", fontsize=16)
plt.xlabel("Ngày", fontsize=12)
plt.ylabel("Giá", fontsize=12)
plt.legend(fontsize=12)
plt.grid(alpha=0.3)

# Hiển thị biểu đồ
plt.show()
