#!/usr/bin/env python
"""
簡単な実行スクリプト - チャートデータの処理

使用例:
    # 全時間足を処理
    uv run process_charts.py
    
    # 特定の時間足のみ処理
    uv run process_charts.py --timeframes 5min 15min 1H
    
    # 1分、5分、15分足のみ処理
    uv run process_charts.py --timeframes 1min 5min 15min
"""

from chart_processor import ChartDataProcessor
import argparse
import config
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description='チャートデータを結合し、指定された時間足に変換します',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
時間足の例:
  1min   - 1分足
  5min   - 5分足
  15min  - 15分足
  30min  - 30分足
  1H     - 1時間足
  4H     - 4時間足
  1D     - 日足
  1W     - 週足
  1M     - 月足

カスタム時間足も指定可能:
  3min   - 3分足
  10min  - 10分足
  2H     - 2時間足
        """
    )
    
    parser.add_argument(
        '--timeframes',
        nargs='+',
        default=None,
        help='処理する時間足（省略時は全ての標準時間足を処理）'
    )
    
    parser.add_argument(
        '--input-dir',
        type=Path,
        default=config.RAW_DATA_DIR,
        help='入力CSVファイルのディレクトリ（デフォルト: raw_data）'
    )
    
    parser.add_argument(
        '--output-dir',
        type=Path,
        default=config.OUTPUT_DIR,
        help='出力先ディレクトリ（デフォルト: processed_data）'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='詳細なログを表示'
    )
    
    args = parser.parse_args()
    
    # ログレベル設定
    import logging
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    
    print("=" * 60)
    print("チャートデータ処理を開始します")
    print("=" * 60)
    print(f"入力ディレクトリ: {args.input_dir}")
    print(f"出力ディレクトリ: {args.output_dir}")
    
    if args.timeframes:
        print(f"処理する時間足: {', '.join(args.timeframes)}")
    else:
        print("処理する時間足: 全ての標準時間足")
    
    print("=" * 60)
    
    # 処理実行
    processor = ChartDataProcessor(
        input_dir=args.input_dir,
        output_dir=args.output_dir
    )
    
    try:
        processor.process(timeframes=args.timeframes)
        print("\n処理が正常に完了しました！")
        print(f"結果は {args.output_dir} に保存されています。")
    except Exception as e:
        print(f"\nエラーが発生しました: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())