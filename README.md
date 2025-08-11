# Axiory チャートデータ処理ツール

Axioryから取得したFXチャートデータ（USDJPY）を様々な時間足に変換するPythonツールです。

## 機能

- 複数のCSVファイルを時系列順に結合
- 重複データの自動削除
- 様々な時間足への変換（1分足〜月足）
- バッチ処理による効率的なデータ変換

## 対応時間足

- 1分足 (1min)
- 5分足 (5min)
- 15分足 (15min)
- 30分足 (30min)
- 1時間足 (1H)
- 4時間足 (4H)
- 日足 (1D)
- 週足 (1W)
- 月足 (1M)

## インストール

```bash
# リポジトリをクローン
git clone https://github.com/yourusername/axiory_chart_processor.git
cd axiory_chart_processor

# 依存関係をインストール（uvを使用）
uv sync
```

## 使い方

### 基本的な使用方法

```bash
# 全ての標準時間足を生成
uv run python process_charts.py

# 特定の時間足のみを生成
uv run python process_charts.py --timeframes 5min 15min 1H

# 詳細ログを表示
uv run python process_charts.py --verbose
```

### カスタムディレクトリの指定

```bash
uv run python process_charts.py \
    --input-dir /path/to/input \
    --output-dir /path/to/output \
    --timeframes 5min 1H
```

## ディレクトリ構成

```
axiory_chart_processor/
├── raw_data/           # 入力CSVファイル（Axioryからダウンロード）
│   ├── USDJPY_2023_all.csv
│   ├── USDJPY_2024_all.csv
│   └── USDJPY_2025_*.csv
├── processed_data/     # 出力ファイル（時間足別）
│   ├── USDJPY_1min_processed.csv
│   ├── USDJPY_5min_processed.csv
│   └── ...
├── chart_processor.py  # メイン処理ロジック
├── process_charts.py   # CLIインターフェース
└── config.py          # 設定ファイル
```

## データフォーマット

### 入力CSV形式（ヘッダーなし）
```
2025.01.01,00:00,150.123,150.456,150.100,150.400,1234
```

カラム順：
1. 日付 (YYYY.MM.DD)
2. 時刻 (HH:MM)
3. 始値 (Open)
4. 高値 (High)
5. 安値 (Low)
6. 終値 (Close)
7. 出来高 (Volume)

### 出力CSV形式（ヘッダーあり）
```csv
date,time,open,high,low,close,volume
2025.01.01,00:00,150.123,150.456,150.100,150.400,1234
```

## リサンプリングルール

各時間足へのデータ集約方法：

| 項目 | 集約方法 |
|------|----------|
| 始値 (Open) | 期間内の最初の値 |
| 高値 (High) | 期間内の最大値 |
| 安値 (Low) | 期間内の最小値 |
| 終値 (Close) | 期間内の最後の値 |
| 出来高 (Volume) | 期間内の合計値 |

## 必要環境

- Python 3.11以上
- pandas 2.3.1以上
- numpy 2.3.2以上

## ライセンス

MIT License

## 貢献

バグ報告や機能リクエストは、GitHubのIssuesまでお願いします。