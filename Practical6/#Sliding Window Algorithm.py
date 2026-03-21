#Sliding Window Algorithm
def rolling_avg_7days(arr):
    n = len(arr)
    if n < 7:
        return []

    buf = [0.0] * 7     # 7个槽
    idx = 0             # 插入位置（循环）
    window_sum = 0.0
    result = []

    # 先把前7天塞入
    for i in range(7):
        buf[i] = arr[i]
        window_sum += arr[i]
    result.append(window_sum / 7)

    # 从第8天开始，覆盖最早的槽
    for i in range(7, n):
        old = buf[idx]      # 即最老的数据
        window_sum -= old
        buf[idx] = arr[i]
        window_sum += arr[i]

        idx = (idx + 1) % 7
        result.append(window_sum / 7)

    return result

# 测试
sleep_hours = [7.0, 6.8, 7.5, 8.2, 6.9, 9.0, 8.0, 7.2, 7.4, 6.8, 8.1, 7.0]
weekly_avg = rolling_avg_7days(sleep_hours)
print('7-day rolling average:', weekly_avg)

# 绘图（需要 matplotlib）
import matplotlib.pyplot as plt

days = list(range(1, len(sleep_hours) + 1))
rolling_days = list(range(7, len(sleep_hours) + 1))

plt.figure(figsize=(10, 5))
plt.plot(days, sleep_hours, label='Daily Sleep Hours', marker='o', alpha=0.7)
plt.plot(rolling_days, weekly_avg, label='7-Day Rolling Avg', color='red', linewidth=2)
plt.title('Sleep Hours and 7-Day Rolling Average')
plt.xlabel('Day')
plt.ylabel('Hours')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('sleep_rolling_avg.png')
plt.show()

