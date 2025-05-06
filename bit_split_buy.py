import pyupbit
import time
from datetime import datetime

# 📌 업비트 API 키 입력
access = "6Wx4gthGq1pI19kKd5gZ9RaEvZPKkcSj47ViAJmT"
secret = "Iy3hC43OhWhQes30UFNaJXwQ3r6v6Llg1xY34CFJ"
upbit = pyupbit.Upbit(access, secret)

# 📌 매매 설정값
symbol = "KRW-BTC"
base_price = pyupbit.get_current_price(symbol)  # 기준 가격 자동 설정
buy_percent = 0.02         # 2% 간격
buy_amount = 10000         # 차수당 매수 금액 (원)
interval_sec = 5           # 가격 확인 주기 (초)

# 📌 7단계 분할매수 기준 가격 설정
buy_levels = [base_price * (1 - buy_percent * i) for i in range(7)]
buy_flags = [False] * 7        # 각 차수 매수 여부 저장
buy_prices = [0] * 7           # 실제 매수가 기록

print(f"[시작] 기준가: {base_price:,.0f}원 → 2% 간격 7단계 분할매수 시작\n")

while True:
    try:
        price = pyupbit.get_current_price(symbol)
        now = datetime.now().strftime('%H:%M:%S')
        print(f"[{now}] 현재가: {price:,.0f}원")

        for i in range(7):
            if not buy_flags[i] and price <= buy_levels[i]:
                print(f">>> {i+1}차 매수! 매수가: {price:,.0f}원")
                upbit.buy_market_order(symbol, buy_amount)
                buy_flags[i] = True
                buy_prices[i] = price
                time.sleep(1)  # 주문 간격

        if all(buy_flags):
            print("\n✅ 7단계 매수 완료! 매수 내역:")
            for i in range(7):
                print(f"{i+1}차: {buy_prices[i]:,.0f}원")
            break

        time.sleep(interval_sec)

    except Exception as e:
        print("[오류 발생]", e)
        time.sleep(5)
