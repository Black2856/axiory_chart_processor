"""
チャートデータ処理の設定ファイル
"""
from pathlib import Path

# パス設定
BASE_DIR = Path(__file__).parent
RAW_DATA_DIR = BASE_DIR / "raw_data"
OUTPUT_DIR = BASE_DIR / "processed_data"

# 時間足の定義（分単位）
TIMEFRAMES = {
    "1min": "1min",     # 1分足
    "5min": "5min",     # 5分足
    "15min": "15min",   # 15分足
    "30min": "30min",   # 30分足
    "1H": "1H",         # 1時間足
    "4H": "4H",         # 4時間足
    "1D": "1D",         # 日足
    "1W": "1W",         # 週足
    "1M": "1ME",        # 月足
}

# データカラム名
COLUMNS = {
    "date": "Date",
    "time": "Time",
    "open": "Open",
    "high": "High",
    "low": "Low",
    "close": "Close",
    "volume": "Volume"
}

# CSVファイルのエンコーディング
CSV_ENCODING = "utf-8"

# 出力フォーマット
OUTPUT_FORMAT = "%Y-%m-%d %H:%M:%S"