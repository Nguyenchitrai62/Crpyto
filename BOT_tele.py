import requests
import ccxt
import time
import pandas as pd
import ta
import time
import socket
from ta.momentum import RSIIndicator, StochasticOscillator

# Khởi tạo sàn giao dịch Binance
binance = ccxt.binance({
    'apiKey': '',
    'secret': '',
})

def is_connected(host="8.8.8.8", port=53, timeout=2):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error:
        return False
    
def send_telegram_message(message):
    # Thông tin Bot
    token = '8049293214:AAGtjjMNfP3Rivzceh2lAQ5RyoSSSNxdFCU'  
    chat_id = '6403928939'    
        
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': message
    }

    with requests.Session() as session:
        # Gửi yêu cầu với timeout để tránh bị chờ quá lâu
        response = session.post(url, json=payload)
        return response.json()

def get_rsi_for_timeframe(symbol, timeframe, window=14):
    # Lấy dữ liệu giá cho khung thời gian cụ thể
    ohlcv = binance.fetch_ohlcv(symbol, timeframe=timeframe, limit=100)
    
    # Chuyển dữ liệu thành DataFrame
    df = pd.DataFrame(ohlcv, columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])
    df['Close'] = df['Close'].astype(float)
    
    # Tính RSI cho khung thời gian này
    rsi = ta.momentum.RSIIndicator(df['Close'], window=window).rsi()
    
    stoch = StochasticOscillator(high=df['High'], low=df['Low'], close=df['Close'], window=14, smooth_window=3)
    print(f"{stoch.stoch().iloc[-1]}         {stoch.stoch_signal().iloc[-1]}")
    if (abs(stoch.stoch().iloc[-1] - stoch.stoch_signal().iloc[-1]) / stoch.stoch().iloc[-1] < 0.01):
        send_telegram_message(f"Stochastic Oscillator {timeframe}\n{stoch.stoch().iloc[-1]:.2f}")
        time.sleep(60)
    
    return round(rsi.iloc[-1])  # Trả về giá trị RSI mới nhất

def alert_symbol(symbol):
    rsi_5m = get_rsi_for_timeframe(symbol, '5m', 14)
    rsi_15m = get_rsi_for_timeframe(symbol, '15m', 14)
    rsi_1h = get_rsi_for_timeframe(symbol, '1h', 14)
    
    reliability_high_RSI_5m = reliability_RSI_5m_df.loc[rsi_5m, 'reliability_high_RSI']
    reliability_high_RSI_15m = reliability_RSI_15m_df.loc[rsi_15m, 'reliability_high_RSI']
    reliability_high_RSI_1h = reliability_RSI_1h_df.loc[rsi_1h, 'reliability_high_RSI']
    
    reliability_low_RSI_5m = reliability_RSI_5m_df.loc[rsi_5m, 'reliability_low_RSI']
    reliability_low_RSI_15m = reliability_RSI_15m_df.loc[rsi_15m, 'reliability_low_RSI']
    reliability_low_RSI_1h = reliability_RSI_1h_df.loc[rsi_1h, 'reliability_low_RSI']
    
    # hiển thị độ tin cậy đỉnh cục bộ
    print(f"{symbol}     HIGH")
    print(f"RSI14 (5m):  {rsi_5m}     {reliability_high_RSI_5m}%")
    print(f"RSI14 (15m): {rsi_15m}     {reliability_high_RSI_15m}%")
    print(f"RSI14 (1h):  {rsi_1h}     {reliability_high_RSI_1h}%")
    
    signal = 0.2 * reliability_high_RSI_5m + 0.3 * reliability_high_RSI_15m + 0.5 * reliability_high_RSI_1h
    print(f"Signal: {signal:.2f}\n")
    
    if signal > 65:
        MESSAGE = (f"{symbol} : {signal:.2f}% 🟥\n"
                   f"RSI14 (5m) : {rsi_5m} ({reliability_high_RSI_5m}%)\n"
                   f"RSI14 (15m) : {rsi_15m} ({reliability_high_RSI_15m}%)\n"
                   f"RSI14 (1h) :  {rsi_1h} ({reliability_high_RSI_1h}%)\n")
        result = send_telegram_message(MESSAGE)
        print(f"Message sent: {result}")
        time.sleep(300)

    # hiển thị độ tin cậy đáy cục bộ
    print(f"{symbol}     LOW")
    print(f"RSI14 (5m):  {rsi_5m}     {reliability_low_RSI_5m}%")
    print(f"RSI14 (15m): {rsi_15m}     {reliability_low_RSI_15m}%")
    print(f"RSI14 (1h):  {rsi_1h}     {reliability_low_RSI_1h}%")
    
    signal = 0.2 * reliability_low_RSI_5m + 0.3 * reliability_low_RSI_15m + 0.5 * reliability_low_RSI_1h
    print(f"Signal: {signal:.2f}\n")
    
    if signal > 65:
        MESSAGE = (f"{symbol} : {signal:.2f}% 🟩\n"
                   f"RSI14 (5m) : {rsi_5m} ({reliability_low_RSI_5m}%)\n"
                   f"RSI14 (15m) : {rsi_15m} ({reliability_low_RSI_15m}%)\n"
                   f"RSI14 (1h) :  {rsi_1h} ({reliability_low_RSI_1h}%)\n")
        result = send_telegram_message(MESSAGE)
        print(f"Message sent: {result}")
        time.sleep(300)
    

reliability_RSI_5m_df = pd.read_csv('reliability_RSI_5m.csv')
reliability_RSI_15m_df = pd.read_csv('reliability_RSI_15m.csv')
reliability_RSI_1h_df = pd.read_csv('reliability_RSI_1h.csv')

while True:
    if is_connected():
        alert_symbol("BTC/USDT")
        time.sleep(1)
    else:
        print("mat mang")