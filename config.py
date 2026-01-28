# MT5 Trading Bot Configuration

# Trading Symbol
SYMBOL = "EURUSD"

# Timeframe options:
# mt5.TIMEFRAME_M1  - 1 minute
# mt5.TIMEFRAME_M5  - 5 minutes
# mt5.TIMEFRAME_M15 - 15 minutes
# mt5.TIMEFRAME_M30 - 30 minutes
# mt5.TIMEFRAME_H1  - 1 hour
# mt5.TIMEFRAME_H4  - 4 hours
# mt5.TIMEFRAME_D1  - Daily
TIMEFRAME = "M5"  # 5-minute candles

# Position size (lot size)
LOT_SIZE = 0.1

# Moving Average Periods (8 different periods)
MA_PERIODS = [5, 10, 20, 50, 100, 150, 200, 250]

# Signal threshold (percentage of MAs that price must be above/below)
SIGNAL_THRESHOLD = 0.6  # 60%

# Risk Management
STOP_LOSS_POINTS = 100  # Stop loss in points
TAKE_PROFIT_POINTS = 150  # Take profit in points

# Bot Settings
TEST_MODE = True  # Set to False for live trading (WARNING: Use with caution!)
CHECK_INTERVAL = 60  # Time between checks in seconds

# Logging
LOG_FILE = "mt5_trading_bot.log"
LOG_LEVEL = "INFO"  # Options: DEBUG, INFO, WARNING, ERROR
