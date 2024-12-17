import requests
import pandas as pd

# URL API
url = "https://api.alternative.me/fng/?limit=1999"

# Gửi yêu cầu GET
response = requests.get(url)

# Kiểm tra nếu yêu cầu thành công
if response.status_code == 200:
    data = response.json()['data']
    
    # Tạo DataFrame từ dữ liệu và đổi tên cột ngay lập tức
    df = pd.DataFrame(data)
    
    # Đổi tên cột 'value' thành 'Fear and Greed' ngay khi tạo DataFrame
    df = df.rename(columns={'value': 'Fear and Greed'})
    
    # Chuyển đổi timestamp thành ngày tháng
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    
    # Đổi kiểu dữ liệu cần thiết (chỉ số Fear and Greed)
    df['Fear and Greed'] = pd.to_numeric(df['Fear and Greed'])
    
    # Đặt cột 'timestamp' lên đầu và chỉ giữ lại cột 'timestamp' và 'Fear and Greed'
    df = df[['timestamp', 'Fear and Greed']]
    
    # Sắp xếp dữ liệu từ quá khứ đến tương lai (tăng dần theo 'timestamp')
    df = df.sort_values(by='timestamp', ascending=True)
    
    # Lưu dữ liệu vào file CSV
    output_file = "fear_and_greed.csv"
    df.to_csv(output_file, index=False)
    print(f"Dữ liệu đã được lưu vào file: {output_file}")
else:
    print("Lỗi khi truy cập API:", response.status_code)
