"""
チャートデータ処理の実行例
"""
from chart_processor import ChartDataProcessor
import config
import logging

logging.basicConfig(level=logging.INFO)


def example_1_process_all_timeframes():
    """例1: 全ての時間足でデータを処理"""
    print("=" * 50)
    print("例1: 全ての時間足でデータを処理")
    print("=" * 50)
    
    processor = ChartDataProcessor()
    processor.process()  # 全時間足を処理


def example_2_process_specific_timeframes():
    """例2: 特定の時間足のみ処理"""
    print("=" * 50)
    print("例2: 5分足と1時間足のみ処理")
    print("=" * 50)
    
    processor = ChartDataProcessor()
    processor.process(timeframes=["5min", "1H"])


def example_3_custom_directories():
    """例3: カスタムディレクトリを使用"""
    print("=" * 50)
    print("例3: カスタム入出力ディレクトリ")
    print("=" * 50)
    
    from pathlib import Path
    
    # カスタムディレクトリを指定
    custom_input = Path("./raw_data")
    custom_output = Path("./custom_output")
    
    processor = ChartDataProcessor(
        input_dir=custom_input,
        output_dir=custom_output
    )
    processor.process(timeframes=["15min", "30min", "4H"])


def example_4_minute_based_processing():
    """例4: 分単位での細かい時間足指定"""
    print("=" * 50)
    print("例4: 3分足、10分足、20分足など、カスタム時間足の処理")
    print("=" * 50)
    
    processor = ChartDataProcessor()
    
    # カスタム時間足（分単位）
    custom_timeframes = ["3min", "10min", "20min", "45min"]
    
    for timeframe in custom_timeframes:
        print(f"Processing {timeframe}...")
        processor.process(timeframes=[timeframe])


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        example_num = sys.argv[1]
        
        examples = {
            "1": example_1_process_all_timeframes,
            "2": example_2_process_specific_timeframes,
            "3": example_3_custom_directories,
            "4": example_4_minute_based_processing,
        }
        
        if example_num in examples:
            examples[example_num]()
        else:
            print(f"例 {example_num} は存在しません")
            print("利用可能な例: 1, 2, 3, 4")
    else:
        print("使用方法:")
        print("  uv run run_examples.py <例番号>")
        print("")
        print("例:")
        print("  uv run run_examples.py 1  # 全時間足を処理")
        print("  uv run run_examples.py 2  # 特定の時間足のみ")
        print("  uv run run_examples.py 3  # カスタムディレクトリ")
        print("  uv run run_examples.py 4  # カスタム分足")
        print("")
        print("デフォルトで例1を実行します...")
        print("")
        example_1_process_all_timeframes()