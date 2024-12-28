import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report
import joblib  # Thư viện để lưu mô hình

# Đọc dữ liệu từ file CSV
data = pd.read_csv("data_with_indicators.csv")  # Thay bằng đường dẫn file CSV của bạn

# Lựa chọn các cột đặc trưng và nhãn
features = ['RSI', '%D', 'CCI']  # Các đặc trưng đầu vào
target = 'Label'  # Nhãn đã gán

# Lọc dữ liệu: Loại bỏ các hàng có nhãn = 2
filtered_data = data[data[target] != 2]

# Tách đặc trưng và nhãn
X = filtered_data[features].values
y = filtered_data[target].values

# Chia dữ liệu thành tập huấn luyện và tập kiểm tra
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Khởi tạo và huấn luyện mô hình KNN
k = 501  # Số lượng láng giềng gần nhất
knn = KNeighborsClassifier(n_neighbors=k)
knn.fit(X_train, y_train)

# Đánh giá mô hình trên tập kiểm tra
y_pred = knn.predict(X_test)
print("Báo cáo phân loại:")
print(classification_report(y_test, y_pred))

# Lưu mô hình KNN sau khi huấn luyện
joblib.dump(knn, 'knn_model.pkl')  # Lưu mô hình vào file 'knn_model.pkl'

# ----------- Dự đoán với đầu vào từ bàn phím -----------

def get_user_input():
    print("\nNhập các chỉ số kỹ thuật hiện tại:")
    rsi = float(input("RSI: "))
    percent_d = float(input("%D: "))
    cci = float(input("CCI: "))
    return np.array([[rsi, percent_d, cci]])

# Nhập các giá trị từ bàn phím
user_input = get_user_input()

# Dự đoán nhãn và xác suất cho đầu vào
predicted_label = knn.predict(user_input)[0]
predicted_probabilities = knn.predict_proba(user_input)[0]

# In kết quả dự đoán
print(f"\nDự đoán xu hướng: {predicted_label}")
print(f"Xác suất dự đoán: {dict(zip(knn.classes_, predicted_probabilities))}")

# Tùy chỉnh in nhãn theo yêu cầu (Đỉnh cục bộ = 1, Đáy cục bộ = 0)
if predicted_label == 0:
    print("Đáy cục bộ")
elif predicted_label == 1:
    print("Đỉnh cục bộ")
else:
    print("Dữ liệu không nằm trong tập huấn luyện!")
