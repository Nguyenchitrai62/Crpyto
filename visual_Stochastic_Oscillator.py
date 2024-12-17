import pandas as pd
import matplotlib.pyplot as plt

file_path = "data_with_indicators.csv"  
df = pd.read_csv(file_path)

df['Date'] = pd.to_datetime(df['Date'])

# Khởi tạo mảng đếm SOO cho đỉnh và đáy
high = [0] * 101  
reliability_high_SO = [0] * 101 
high_cout = 0

low = [0] * 101   
reliability_low_SO = [0] * 101 
low_cout = 0

# reliability table
for idx, row in df.iterrows():
    # Kiểm tra nếu SO là NaN (trống)
    if pd.isna(row['%K']):
        continue

    if row['Is_Local_High']:
        SO_rounded = round((row['%K'] + row['%D']) / 2)  
        if 0 <= SO_rounded <= 100:
            high[SO_rounded] += 1
            high_cout += 1
            
    elif row['Is_Local_Low']:
        SO_rounded = round((row['%K'] + row['%D']) / 2) 
        if 0 <= SO_rounded <= 100:
            low[SO_rounded] += 1
            low_cout += 1 

for i in range(0,101):
    tong = 0
    for j in range (i+1,101):
        tong += high[j]
    reliability_high_SO[i] = 1 - (tong/high_cout)
    print(f"{i}    {reliability_high_SO[i]}")
     
for i in range(0,101):
    tong = 0
    for j in range (0,i):
        tong += low[j]
    reliability_low_SO[i] = 1 - (tong/low_cout)
    print(f"{i}    {reliability_low_SO[i]}")

reliability_high_SO = [round(value * 100, 2) for value in reliability_high_SO]
reliability_low_SO = [round(value * 100, 2) for value in reliability_low_SO]

reliability_df = pd.DataFrame({
    'Stochastic Oscillator': list(range(101)),
    'reliability_high_SO': reliability_high_SO,
    'reliability_low_SO': reliability_low_SO
})

output_file = 'reliability_SO_1h.csv'
reliability_df.to_csv(output_file, index=False)

print(f"Đã lưu kết quả vào file: {output_file}")
    
# Vẽ biểu đồ
plt.figure(figsize=(10, 6))

plt.bar(range(101), high, alpha=0.6, label='Đỉnh Cục Bộ', color='green')

plt.bar(range(101), low, alpha=0.6, label='Đáy Cục Bộ', color='red')

plt.title('Số lượng Đỉnh và Đáy Cục Bộ theo SO')
plt.xlabel('SO')
plt.ylabel('Số Lượng')
plt.legend()

plt.show()

