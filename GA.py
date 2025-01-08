import numpy as np
import pandas as pd
import random

# Đọc dữ liệu từ file CSV
data = pd.read_csv('data_with_indicators.csv')

# Hàm mô phỏng giao dịch dựa trên ngưỡng RSI, ADX, tp_percent và sl_percent
def simulate_trading(data, rsi_threshold, adx_threshold, tp_percent, sl_percent, fee_percent=0.07/100, leverage=10):
    # Khởi tạo vốn và các cột cần thiết
    capital = 100000  # Vốn ban đầu
    data['Position'] = 0
    data['Entry_Price'] = 0.0
    data['Exit_Price'] = 0.0
    data['Trade_Volume'] = 0  # Đổi tên cột khối lượng giao dịch
    data['PnL'] = 0.0

    position_open = False
    entry_price = 0.0
    tp_price = 0.0
    sl_price = 0.0
    trade_volume = 0

    for i in range(len(data)):
        if not position_open:
            # Kiểm tra điều kiện vào lệnh
            if data.loc[i, 'RSI'] > rsi_threshold and data.loc[i, 'ADX'] > adx_threshold:
                entry_price = data.loc[i, 'Close']
                trade_volume = int((capital * leverage) // entry_price)  # Tính số cổ phiếu với đòn bẩy
                
                if trade_volume > 0:  # Chỉ vào lệnh nếu khối lượng > 0
                    tp_price = entry_price * (1 + tp_percent)
                    sl_price = entry_price * (1 - sl_percent)

                    # Tính phí giao dịch khi mở lệnh
                    fee_open = entry_price * trade_volume * fee_percent
                    capital -= fee_open  # Trừ phí vào tài khoản

                    # Lưu thông tin giao dịch
                    data.loc[i, 'Position'] = 1
                    data.loc[i, 'Entry_Price'] = entry_price
                    data.loc[i, 'Trade_Volume'] = trade_volume
                    position_open = True
        else:
            # Kiểm tra điều kiện thoát lệnh
            high_price = data.loc[i, 'High']
            low_price = data.loc[i, 'Low']

            if low_price <= sl_price:
                # Dừng lỗ
                exit_price = sl_price
                pnl = (exit_price - entry_price) * trade_volume  # Lợi nhuận hoặc lỗ
                # Tính phí giao dịch khi đóng lệnh
                fee_close = exit_price * trade_volume * fee_percent
                capital += pnl - fee_close  # Cập nhật vốn sau khi trừ phí
                data.loc[i, 'Exit_Price'] = exit_price
                data.loc[i, 'PnL'] = pnl
                position_open = False

            elif high_price >= tp_price:
                # Chốt lời
                exit_price = tp_price
                pnl = (exit_price - entry_price) * trade_volume
                # Tính phí giao dịch khi đóng lệnh
                fee_close = exit_price * trade_volume * fee_percent
                capital += pnl - fee_close  # Cập nhật vốn sau khi trừ phí
                data.loc[i, 'Exit_Price'] = exit_price
                data.loc[i, 'PnL'] = pnl
                position_open = False

    total_profit = data['PnL'].sum()
    return total_profit


# Hàm khởi tạo cá thể 
def create_individual():
    rsi_threshold = random.uniform(20, 80)  # Ngưỡng RSI trong khoảng [20, 80]
    adx_threshold = random.uniform(0, 60)  # Ngưỡng ADX trong khoảng [0, 60]
    tp_percent = random.uniform(0.5/100, 3.0/100)  # Chốt lời trong khoảng [0.5%, 3%]
    sl_percent = random.uniform(0.5/100, 3.0/100)  # Dừng lỗ trong khoảng [0.5%, 3%]
    return (rsi_threshold, adx_threshold, tp_percent, sl_percent)

# Hàm đột biến
def mutate(individual):
    mutation_rsi = individual[0] + random.uniform(-6, 6)
    mutation_adx = individual[1] + random.uniform(-6, 6)
    mutation_tp = individual[2] + random.uniform(-0.25/100, 0.25/100)
    mutation_sl = individual[3] + random.uniform(-0.25/100, 0.25/100)
    return (min(max(mutation_rsi, 20), 80), min(max(mutation_adx, 0), 60), 
            min(max(mutation_tp, 0.5/100), 3.0/100), min(max(mutation_sl, 0.5/100), 3.0/100))

# Hàm lai ghép
def crossover(ind1, ind2):
    rsi_threshold = (ind1[0] + ind2[0]) / 2
    adx_threshold = (ind1[1] + ind2[1]) / 2
    tp_percent = (ind1[2] + ind2[2]) / 2
    sl_percent = (ind1[3] + ind2[3]) / 2
    return (rsi_threshold, adx_threshold, tp_percent, sl_percent)

# Hàm tối ưu hóa bằng thuật toán tiến hóa
def optimize(data, generations=50, population_size=50):
    population = [create_individual() for _ in range(population_size)]
    best_individual = None
    best_profit = -np.inf

    for generation in range(generations):
        profits = []
        detailed_logs = []  # Lưu chi tiết quá trình

        for idx, individual in enumerate(population):
            profit = simulate_trading(data.copy(), individual[0], individual[1], individual[2], individual[3])
            profits.append(profit)
            detailed_logs.append(f"Individual {idx + 1}: RSI = {individual[0]:.2f}, ADX = {individual[1]:.2f}, TP = {individual[2]:.4f}, SL = {individual[3]:.4f}, Profit = {profit:.2f}")

            if profit > best_profit:
                best_profit = profit
                best_individual = individual

        # In thông tin chi tiết
        print(f"\nGeneration {generation + 1}:")
        for log in detailed_logs:
            print(log)

        # Chọn các cá thể tốt nhất
        sorted_population = [x for _, x in sorted(zip(profits, population), reverse=True)]
        population = sorted_population[:population_size // 2]

        # Lai ghép và đột biến để tạo thế hệ mới
        new_population = []
        while len(new_population) < population_size:
            parent1 = random.choice(population)
            parent2 = random.choice(population)
            child = crossover(parent1, parent2)
            child = mutate(child)
            new_population.append(child)

        population = new_population
        print(f"Best in Generation {generation + 1}: RSI = {best_individual[0]:.2f}, ADX = {best_individual[1]:.2f}, TP = {best_individual[2]:.4f}, SL = {best_individual[3]:.4f}, Profit = {best_profit:.2f}")

    return best_individual, best_profit

# Chạy thuật toán tối ưu hóa với đòn bẩy cố định
best_individual, best_profit = optimize(data)
print("\nFinal Results:")
print("Best RSI Threshold:", best_individual[0])
print("Best ADX Threshold:", best_individual[1])
print("Best TP Percent:", best_individual[2])
print("Best SL Percent:", best_individual[3])
print("Best Total Profit:", best_profit)
