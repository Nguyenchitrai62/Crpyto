import requests
import ccxt
import time
import pandas as pd
import numpy as np
import socket
import joblib
from ta.momentum import RSIIndicator, StochasticOscillator
from ta.trend import CCIIndicator

# Khởi tạo sàn giao dịch Binance
binance = ccxt.binance({
    'apiKey': '',
    'secret': '',
})

# Kiểm tra kết nối internet
def is_connected(host="8.8.8.8", port=53, timeout=2):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error:
        return False

# Gửi tin nhắn cảnh báo qua Telegram
def send_telegram_message(message):
    token = '8049293214:AAGtjjMNfP3Rivzceh2lAQ5RyoSSSNxdFCU'  # Token của Bot Telegram
    chat_id = '6403928939'  # ID của người nhận tin nhắn
    
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': message
    }

    with requests.Session() as session:
        response = session.post(url, json=payload)
        return response.json()

# Load mô hình KNN đã huấn luyện
knn_model = joblib.load('knn_model.pkl')  # Đảm bảo rằng mô hình KNN đã được lưu trước đó

# Hàm tính các chỉ báo RSI, Stochastic và CCI
def get_indicators_for_timeframe(symbol, timeframe, window=14):
    # Lấy dữ liệu giá cho khung thời gian cụ thể
    ohlcv = binance.fetch_ohlcv(symbol, timeframe=timeframe, limit=100)
    
    # Chuyển dữ liệu thành DataFrame
    df = pd.DataFrame(ohlcv, columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])
    df['Close'] = df['Close'].astype(float)
    df['High'] = df['High'].astype(float)
    df['Low'] = df['Low'].astype(float)
    
    # Tính các chỉ báo
    rsi = RSIIndicator(df['Close'], window=window).rsi().iloc[-1]
    stoch = StochasticOscillator(high=df['High'], low=df['Low'], close=df['Close'], window=14, smooth_window=3)
    stoch_k = stoch.stoch().iloc[-1]
    stoch_d = stoch.stoch_signal().iloc[-1]
    cci = CCIIndicator(df['High'], df['Low'], df['Close'], window=window).cci().iloc[-1]
    print(f"RSI:{rsi}        %D:{stoch_d}        CCI:{cci}")
    # Trả về các chỉ báo đã chuẩn hóa
    return rsi/100, stoch_d/100, (cci+500)/1000  # Chuyển các chỉ báo về phạm vi [0, 1]

# Hàm dự đoán và gửi cảnh báo
def make_prediction(rsi, stoch_d, cci):
    # Chuyển các giá trị chỉ báo thành mảng numpy
    indicators = np.array([[rsi, stoch_d, cci]])  # Cần sử dụng các chỉ báo phù hợp với mô hình của bạn

    # Dự đoán với mô hình KNN
    prediction = knn_model.predict(indicators)
    prediction_proba = knn_model.predict_proba(indicators)

    # Nếu tỷ lệ xác suất cho nhãn 1 (đỉnh cục bộ) > 90%, gửi cảnh báo
    if prediction_proba[0][1] > 0.9:
        send_telegram_message(f"Khả năng dự đoán đỉnh cục bộ (tỉ lệ > 90%): RSI={rsi:.2f}, %D={stoch_d:.2f}, CCI={cci:.2f}")
        print("Cảnh báo: Đỉnh cục bộ được dự đoán với xác suất > 90%")
        time.sleep(300)  # Ngừng một lúc để tránh gửi quá nhiều tin nhắn
    # Nếu tỷ lệ xác suất cho nhãn 0 (đáy cục bộ) > 90%, gửi cảnh báo
    elif prediction_proba[0][0] > 0.9:
        send_telegram_message(f"Khả năng dự đoán đáy cục bộ (tỉ lệ > 90%): RSI={rsi:.2f}, %D={stoch_d:.2f}, CCI={cci:.2f}")
        print("Cảnh báo: Đáy cục bộ được dự đoán với xác suất > 90%")
        time.sleep(300)  # Ngừng một lúc để tránh gửi quá nhiều tin nhắn
    else:
        print(f"Xác suất đỉnh cục bộ: {prediction_proba[0][1]:.2f}")
        print(f"Xác suất đáy cục bộ: {prediction_proba[0][0]:.2f}")

# Chạy vòng lặp để liên tục kiểm tra và dự đoán
while True:
    if is_connected():
        rsi, stoch_d, cci = get_indicators_for_timeframe("BTC/USDT", "1h")  # Thay "BTC/USDT" và "1h" theo nhu cầu

        make_prediction(rsi, stoch_d, cci)

        time.sleep(1)  # Ngừng 1 giây để tránh quá tải API của Binance
    else:
        print("Mất kết nối mạng.")
