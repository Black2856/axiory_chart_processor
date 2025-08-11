# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a financial chart data processing tool that reads raw CSV files containing USDJPY tick/minute data and converts them into various timeframes (1min, 5min, 15min, 30min, 1H, 4H, 1D, 1W, 1M).

## Common Commands

### Run the chart processor
```bash
# Process specific timeframes
uv run python process_charts.py --timeframes 5min 15min 1H

# Process all standard timeframes
uv run python process_charts.py
```

### Development environment
```bash
# Install dependencies
uv sync

# Run with custom directories
uv run python process_charts.py --input-dir raw_data --output-dir processed_data
```

## Architecture

The system follows a simple ETL pipeline:

1. **Input**: Raw CSV files in `raw_data/` directory containing minute-level OHLCV data
2. **Processing**: `ChartDataProcessor` class handles:
   - Loading and merging multiple CSV files chronologically
   - Removing duplicates based on datetime
   - Resampling to different timeframes using pandas
3. **Output**: Processed files saved to `processed_data/` directory

### Key Components

- `chart_processor.py`: Core processing logic with `ChartDataProcessor` class
- `process_charts.py`: CLI interface for running the processor
- `config.py`: Configuration for timeframes, paths, and data formats

### Data Processing Rules

When resampling to higher timeframes:
- **Open**: First value in the period
- **High**: Maximum value in the period  
- **Low**: Minimum value in the period
- **Close**: Last value in the period
- **Volume**: Sum of all volumes in the period

### Input Data Format

Raw CSV files have no headers and columns are:
1. Date (YYYY.MM.DD format)
2. Time (HH:MM format)
3. Open price
4. High price
5. Low price
6. Close price
7. Volume

## Dependencies

- Python 3.11+
- pandas for data manipulation
- numpy for numerical operations
- Uses `uv` for package management