"""
チャートデータの結合と時間足変換処理
"""
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Optional, List
import logging
from datetime import datetime
import config

# ログ設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ChartDataProcessor:
    """チャートデータを処理するクラス"""
    
    def __init__(self, input_dir: Path = config.RAW_DATA_DIR, 
                 output_dir: Path = config.OUTPUT_DIR):
        """
        初期化
        
        Args:
            input_dir: 入力データのディレクトリ
            output_dir: 出力データのディレクトリ
        """
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.output_dir.mkdir(exist_ok=True)
        
    def load_csv_files(self) -> pd.DataFrame:
        """
        raw_dataフォルダ内の全CSVファイルを読み込み、時系列順に結合
        
        Returns:
            結合されたDataFrame
        """
        csv_files = sorted(self.input_dir.glob("*.csv"))
        
        if not csv_files:
            raise FileNotFoundError(f"No CSV files found in {self.input_dir}")
        
        logger.info(f"Found {len(csv_files)} CSV files")
        
        dataframes = []
        for file_path in csv_files:
            logger.info(f"Loading {file_path.name}")
            
            # CSVを読み込み（ヘッダーなし）
            df = pd.read_csv(
                file_path, 
                header=None,
                names=['date', 'time', 'open', 'high', 'low', 'close', 'volume'],
                encoding=config.CSV_ENCODING
            )
            
            dataframes.append(df)
        
        # 全データを結合
        combined_df = pd.concat(dataframes, ignore_index=True)
        
        # datetime列を作成
        combined_df['datetime'] = pd.to_datetime(
            combined_df['date'] + ' ' + combined_df['time'],
            format='%Y.%m.%d %H:%M'
        )
        
        # datetimeでソート
        combined_df = combined_df.sort_values('datetime')
        
        # 重複を削除（同じdatetimeの行を削除）
        combined_df = combined_df.drop_duplicates(subset=['datetime'], keep='first')
        
        # インデックスをdatetimeに設定
        combined_df.set_index('datetime', inplace=True)
        
        # 不要な列を削除
        combined_df = combined_df[['open', 'high', 'low', 'close', 'volume']]
        
        logger.info(f"Total rows after merging: {len(combined_df)}")
        logger.info(f"Date range: {combined_df.index.min()} to {combined_df.index.max()}")
        
        return combined_df
    
    def resample_data(self, df: pd.DataFrame, timeframe: str) -> pd.DataFrame:
        """
        データを指定された時間足にリサンプル
        
        Args:
            df: 入力DataFrame（1分足データ）
            timeframe: 時間足（例: '5min', '1H', '1D'）
        
        Returns:
            リサンプルされたDataFrame
        """
        logger.info(f"Resampling to {timeframe}")
        
        # pandasのリサンプル用の時間足フォーマットに変換
        resample_rule = timeframe
        
        # リサンプル
        resampled = df.resample(resample_rule).agg({
            'open': 'first',
            'high': 'max',
            'low': 'min',
            'close': 'last',
            'volume': 'sum'
        })
        
        # NaNを削除（データがない時間帯）
        resampled = resampled.dropna()
        
        logger.info(f"Rows after resampling: {len(resampled)}")
        
        return resampled
    
    def save_to_csv(self, df: pd.DataFrame, timeframe: str, symbol: str = "USDJPY"):
        """
        データをCSVファイルに保存
        
        Args:
            df: 保存するDataFrame
            timeframe: 時間足
            symbol: 通貨ペア名
        """
        filename = f"{symbol}_{timeframe}_processed.csv"
        output_path = self.output_dir / filename
        
        # インデックスを列に戻す
        df_to_save = df.reset_index()
        
        # datetime列を日付と時刻に分割
        df_to_save['date'] = df_to_save['datetime'].dt.strftime('%Y.%m.%d')
        df_to_save['time'] = df_to_save['datetime'].dt.strftime('%H:%M')
        
        # 必要な列のみを選択して保存
        df_to_save[['date', 'time', 'open', 'high', 'low', 'close', 'volume']].to_csv(
            output_path,
            index=False,
            encoding=config.CSV_ENCODING
        )
        
        logger.info(f"Saved to {output_path}")
        
    def process(self, timeframes: Optional[List[str]] = None):
        """
        メイン処理：データの読み込み、結合、リサンプル、保存
        
        Args:
            timeframes: 処理する時間足のリスト（Noneの場合は全て）
        """
        # データを読み込み・結合
        df_1min = self.load_csv_files()
        
        # 1分足データも保存
        self.save_to_csv(df_1min, "1min")
        
        # 指定された時間足に変換
        if timeframes is None:
            timeframes = list(config.TIMEFRAMES.values())
        
        for timeframe in timeframes:
            if timeframe == "1min":
                continue  # 1分足は既に保存済み
                
            try:
                resampled_df = self.resample_data(df_1min, timeframe)
                self.save_to_csv(resampled_df, timeframe)
            except Exception as e:
                logger.error(f"Error processing {timeframe}: {e}")


def main():
    """メイン関数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='チャートデータの処理')
    parser.add_argument(
        '--timeframes',
        nargs='+',
        choices=list(config.TIMEFRAMES.values()),
        help='処理する時間足（複数指定可）'
    )
    parser.add_argument(
        '--input-dir',
        type=Path,
        default=config.RAW_DATA_DIR,
        help='入力データディレクトリ'
    )
    parser.add_argument(
        '--output-dir',
        type=Path,
        default=config.OUTPUT_DIR,
        help='出力データディレクトリ'
    )
    
    args = parser.parse_args()
    
    # プロセッサを作成して実行
    processor = ChartDataProcessor(
        input_dir=args.input_dir,
        output_dir=args.output_dir
    )
    
    processor.process(timeframes=args.timeframes)
    
    logger.info("Processing completed successfully!")


if __name__ == "__main__":
    main()