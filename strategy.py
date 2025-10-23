
import os
import sys
from datetime import datetime
from zoneinfo import ZoneInfo
from cpz.clients.sync import CPZClient
# --- Set credentials ---
os.environ["CPZ_AI_API_KEY"] = "cpz_key_306586b0e48f4955835e6229"
os.environ["CPZ_AI_SECRET_KEY"] = "cpz_secret_55376a4b4p2n3n5s1a5n62yk2y35d676a1h223w5n1e1e5w0"
os.environ["CPZ_STRATEGY_ID"] = "d5d8d00e-40c3-4e62-b053-f4f06ddd0402"
SYMBOL = "KO"
QTY = 1
TZ_ET = ZoneInfo("US/Eastern")

if not os.getenv("CPZ_AI_API_KEY") or not os.getenv("CPZ_AI_SECRET_KEY"):
    print("CPZ_AI_API_KEY and CPZ_AI_SECRET_KEY must be set in environment", file=sys.stderr)
    sys.exit(2)

strategy_id = os.getenv("CPZ_STRATEGY_ID") or "default"
broker = os.getenv("CPZ_BROKER", "alpaca")
env = os.getenv("CPZ_ENV", "paper")  # reserved for future use
account_id = os.getenv("CPZ_ACCOUNT_ID")  # optional

client = CPZClient()
if account_id:
    client.execution.use_broker(broker, account_id="PA31SNG7N5V9")
else:
    client.execution.use_broker(broker)

def place(side: str):
    order = client.execution.order(
        symbol=SYMBOL,
        qty=QTY,
        side=side,
        order_type="market",
        time_in_force="DAY",
        strategy_id=strategy_id,
    )
    print(order.model_dump_json())

def main():
    now_et = datetime.now(TZ_ET)
    ten_am = now_et.replace(hour=10, minute=0, second=0, microsecond=0).time()

    if now_et.time() < ten_am:
        print(f"[{now_et}] Before 10:00 AM ET -> BUY {QTY} {SYMBOL}")
        place("buy")
    elif now_et.time() > ten_am:
        print(f"[{now_et}] After 10:00 AM ET -> SELL {QTY} {SYMBOL}")
        place("sell")
    else:
        print(f"[{now_et}] Exactly 10:00 AM ET -> no action")

if __name__ == "__main__":
    main()