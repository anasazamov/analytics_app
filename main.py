import websocket
import time
import json
import csv
import os
import threading

# --- Fayl nomlari ---
FILES = {
    "OnRegistration": "registration.csv",
    "OnBets":         "bets.csv",
    "OnCashouts":     "cashouts.csv",
    "OnCrash":        "crash.csv",
    "summary":        "summary.csv"
}

# --- Headerlarni tayyorlash ---
HEADERS = {
    "OnRegistration": ["timestamp","round_id","id","user","bet"],
    "OnBets":         ["timestamp","round_id","id","user","bet"],
    "OnCashouts":     ["timestamp","round_id","id","win","k"],
    "OnCrash":        ["timestamp","round_id","crash_point"],
    "summary":        ["round_id","crash_point","total_bet","total_win","net_profit","avg_odds","num_bets","num_cashouts"]
}

writers = {}
files   = {}
first_run = {}

# --- Thread-safe lock ---
lock = threading.Lock()

# --- Raund bo‘yicha analytics saqlovchi ---
round_stats = {}  # { round_id: { total_bet, total_win, num_bets, num_cashouts, sum_odds } }

def init_file(event):
    """Agar birinchi marta ochilsa, fayl va writer tayyorlaydi."""
    fname = FILES[event]
    is_new = not os.path.exists(fname) or os.path.getsize(fname)==0
    f = open(fname, 'a', newline='', encoding='utf-8')
    w = csv.writer(f)
    if is_new:
        w.writerow(HEADERS[event])
        f.flush()
    files[event] = f
    writers[event] = w

for ev in FILES:
    init_file(ev)

def record(event, row):
    """Qatorni tegishli CSV ga yozadi."""
    with lock:
        writers[event].writerow(row)
        files[event].flush()

def on_message(ws, message):
    raw = message.rstrip('\x1e').strip()
    try:
        obj = json.loads(raw)
    except json.JSONDecodeError:
        return

    ts = time.time()
    # Ba’zi xabarlar type:6 yoki type:3 bo‘lishi mumkin, e’tibor bermaymiz
    if "target" not in obj or not obj.get("arguments"):
        return

    tgt = obj["target"]
    args = obj["arguments"][0]
    rid = args.get("l")  # round_id

    # --- Registration ---
    if tgt == "OnRegistration" and "q" in args:
        for bet in args["q"]:
            record("OnRegistration", [
                ts, rid,
                bet.get("id"), bet.get("u"), bet.get("bet")
            ])
            # analytics
            st = round_stats.setdefault(rid, {"total_bet":0,"total_win":0,"num_bets":0,"num_cashouts":0,"sum_odds":0})
            st["total_bet"] += float(bet.get("bet",0))
            st["num_bets"] += 1

    # --- Bets ---
    elif tgt == "OnBets" and "q" in args:
        for bet in args["q"]:
            record("OnBets", [
                ts, rid,
                bet.get("id"), bet.get("u"), bet.get("bet")
            ])
            st = round_stats.setdefault(rid, {"total_bet":0,"total_win":0,"num_bets":0,"num_cashouts":0,"sum_odds":0})
            st["total_bet"] += float(bet.get("bet",0))
            st["num_bets"] += 1

    # --- Cashouts ---
    elif tgt == "OnCashouts" and "q" in args:
        for win in args["q"]:
            record("OnCashouts", [
                ts, rid,
                win.get("id"), win.get("win"), win.get("k")
            ])
            st = round_stats.setdefault(rid, {"total_bet":0,"total_win":0,"num_bets":0,"num_cashouts":0,"sum_odds":0})
            st["total_win"] += float(win.get("win",0))
            st["num_cashouts"] += 1
            st["sum_odds"] += float(win.get("k",0))

    # --- Crash: raund tugadi, summary yozamiz ---
    elif tgt == "OnCrash" and "f" in args:
        crash_pt = args["f"]
        record("OnCrash", [
            ts, rid, crash_pt
        ])
        # summary
        st = round_stats.pop(rid, {"total_bet":0,"total_win":0,"num_bets":0,"num_cashouts":0,"sum_odds":0})
        total_bet     = st["total_bet"]
        total_win     = st["total_win"]
        num_bets      = st["num_bets"]
        num_cashouts  = st["num_cashouts"]
        avg_odds      = (st["sum_odds"]/num_cashouts) if num_cashouts>0 else 0
        net_profit    = total_win - total_bet
        record("summary", [
            rid, crash_pt,
            total_bet, total_win,
            net_profit, avg_odds,
            num_bets, num_cashouts
        ])
        print(f"Round {rid} → crash {crash_pt}, bets={num_bets}, cashouts={num_cashouts}, total_bet={total_bet:.2f}, total_win={total_win:.2f}, net={net_profit:.2f}, avg_k={avg_odds:.2f}")

def on_error(ws, error):
    print("Error:", error)

def on_close(ws, code, msg):
    print(f"### closed ### code={code}, msg={msg}")
    for f in files.values():
        f.close()

def on_open(ws):
    print("### opened ###")
    # handshake
    ws.send(json.dumps({"protocol":"json","version":1}) + '\x1e')
    ws.send(json.dumps({
        "arguments":[{"activity":30,"currency":87}],
        "invocationId":"0","target":"Guest","type":1
    }) + '\x1e')

def run_ws():
    url = ("wss://melbet-uz-1.com/games-frame/sockets/crash"
           "?whence=55&fcountry=192&ref=8&gr=1521&appGuid=games-web-app-unknown&lng=ru")
    ws = websocket.WebSocketApp(
        url,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    ws.run_forever(ping_interval=10, ping_timeout=5)

if __name__ == "__main__":
    try:
        run_ws()
    except KeyboardInterrupt:
        print("Interrupted, exiting.")
