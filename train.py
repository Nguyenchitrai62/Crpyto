import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
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

# Định nghĩa các giá trị của K cần thử
param_grid = {'n_neighbors': np.arange(1, 50)}  # Thử các giá trị K từ 1 đến 20

# Khởi tạo mô hình KNN
knn = KNeighborsClassifier()

# Sử dụng GridSearchCV để tìm kiếm giá trị K tối ưu
grid_search = GridSearchCV(knn, param_grid, cv=10)  # cv=5 là số lần phân chia dữ liệu trong K-fold cross-validation
grid_search.fit(X_train, y_train)

# In ra tham số K tối ưu và độ chính xác tương ứng
optimal_k = grid_search.best_params_['n_neighbors']
print(f"Tham số K tối ưu: {optimal_k}")
print(f"Độ chính xác trên tập kiểm tra: {grid_search.best_score_}")

# Huấn luyện mô hình KNN với tham số K tối ưu
knn_optimal = KNeighborsClassifier(n_neighbors=optimal_k)
knn_optimal.fit(X_train, y_train)

# Đánh giá mô hình với tham số K tối ưu trên tập kiểm tra
y_pred = knn_optimal.predict(X_test)
print("Báo cáo phân loại:")
print(classification_report(y_test, y_pred))

# Lưu mô hình với tham số K tối ưu
joblib.dump(knn_optimal, 'knn_model.pkl')
