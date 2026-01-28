# MT5 Trading Bot - Moving Average Strategy

An automated trading bot for MetaTrader 5 that uses multiple moving averages to generate buy and sell signals.

## Overview

This trading bot implements a multi-moving average strategy using 8 different moving average periods to predict market movements. The bot analyzes price action against these moving averages and generates trading signals accordingly.

### Strategy Logic

- **BUY Signal**: Triggered when the current price is above at least 60% of the moving averages
- **SELL Signal**: Triggered when the current price is below at least 60% of the moving averages
- **HOLD Signal**: When the price is between moving averages without a clear trend

### Moving Average Periods

The bot uses 8 different moving average periods by default:
- MA 5 (Very short-term)
- MA 10 (Short-term)
- MA 20 (Short-term)
- MA 50 (Medium-term)
- MA 100 (Medium-term)
- MA 150 (Long-term)
- MA 200 (Long-term)
- MA 250 (Very long-term)

## Features

✅ Multiple moving average analysis (8 different periods)
✅ Automated buy/sell signal generation
✅ Position management (open/close)
✅ Risk management (Stop Loss & Take Profit)
✅ Test mode for strategy validation
✅ Comprehensive logging
✅ Configurable parameters
✅ Real-time market analysis

## Requirements

- Python 3.8 or higher
- MetaTrader 5 terminal installed
- Active MT5 trading account (demo or live)

## Installation

### Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Install and Setup MetaTrader 5

1. Download and install MetaTrader 5 from [MetaQuotes website](https://www.metatrader5.com/)
2. Open MT5 and login to your trading account
3. Enable automated trading in MT5:
   - Go to Tools → Options → Expert Advisors
   - Check "Allow automated trading"
   - Check "Allow DLL imports"

## Configuration

Edit `config.py` to customize the bot settings:

```python
# Trading Symbol
SYMBOL = "EURUSD"  # Change to your preferred symbol

# Timeframe
TIMEFRAME = "M5"  # 5-minute candles

# Position Size
LOT_SIZE = 0.1  # Adjust based on your account size

# Moving Average Periods
MA_PERIODS = [5, 10, 20, 50, 100, 150, 200, 250]

# Test Mode (IMPORTANT!)
TEST_MODE = True  # Set to False for live trading
```

## Usage

### Running in Test Mode (Recommended for beginners)

Test mode analyzes the market and generates signals without placing actual orders:

```bash
python mt5_trading_bot.py
```

The bot will:
1. Connect to MT5
2. Analyze the market every 60 seconds (configurable)
3. Display current price and moving average analysis
4. Show BUY/SELL/HOLD signals
5. Log all activity to console and `mt5_trading_bot.log`

### Running in Live Trading Mode

⚠️ **WARNING**: Live trading involves real money. Only use this mode if you understand the risks!

1. Edit `mt5_trading_bot.py` and set `TEST_MODE = False`
2. Start with a demo account to validate the strategy
3. Run the bot:

```bash
python mt5_trading_bot.py
```

## How It Works

### 1. Data Collection
The bot retrieves historical price data (OHLC) from MT5 for the specified symbol and timeframe.

### 2. Moving Average Calculation
It calculates 8 different moving averages using the closing prices.

### 3. Signal Generation
The bot compares the current price against all moving averages:
- Counts how many MAs the price is above
- Counts how many MAs the price is below
- Generates a signal based on the majority (60% threshold)

### 4. Trade Execution
Based on the signal:
- **BUY**: Opens a long position if price is above 60% of MAs
- **SELL**: Opens a short position if price is below 60% of MAs
- **HOLD**: No action if the signal is unclear

### 5. Risk Management
Each trade includes:
- Stop Loss: 100 points (configurable)
- Take Profit: 150 points (configurable)

## Example Output

```
============================================================
Market Analysis for EURUSD
Time: 2026-01-28 10:30:00
Current Price: 1.08450
------------------------------------------------------------
MA   5: 1.08420 - Price is ABOVE
MA  10: 1.08390 - Price is ABOVE
MA  20: 1.08350 - Price is ABOVE
MA  50: 1.08280 - Price is ABOVE
MA 100: 1.08200 - Price is ABOVE
MA 150: 1.08150 - Price is ABOVE
MA 200: 1.08100 - Price is ABOVE
MA 250: 1.08050 - Price is ABOVE
------------------------------------------------------------
SIGNAL: BUY
Current Position: None
============================================================
```

## Customization

### Changing Moving Average Periods

Edit the `ma_periods` list in `mt5_trading_bot.py`:

```python
self.ma_periods = [5, 10, 20, 50, 100, 150, 200, 250]
# Change to your preferred periods, e.g.:
# self.ma_periods = [8, 13, 21, 34, 55, 89, 144, 233]  # Fibonacci numbers
```

### Adjusting Signal Threshold

Modify the signal generation logic in the `generate_signals` method:

```python
# Current: 60% threshold
if above_ma_count / total_valid_mas >= 0.6:  # Change 0.6 to your preference
    return 'buy'
```

### Changing Risk Parameters

Edit the Stop Loss and Take Profit in `place_buy_order` and `place_sell_order` methods:

```python
"sl": price - 100 * point,  # Increase/decrease stop loss
"tp": price + 150 * point,  # Increase/decrease take profit
```

## Logging

All activity is logged to:
- Console output (real-time)
- `mt5_trading_bot.log` file

Log includes:
- Connection status
- Market analysis
- Signal generation
- Trade execution
- Errors and warnings

## Safety Features

1. **Test Mode**: Analyze without trading
2. **Error Handling**: Comprehensive error checking
3. **Position Management**: Automatic position tracking
4. **Stop Loss & Take Profit**: Built-in risk management
5. **Logging**: Complete audit trail

## Common Issues

### Bot won't connect to MT5
- Ensure MT5 terminal is running
- Check that you're logged into your MT5 account
- Verify "Allow automated trading" is enabled in MT5 settings

### No data received
- Check that the symbol exists in your MT5 Market Watch
- Verify the symbol name (e.g., "EURUSD" vs "EUR/USD")
- Ensure there's sufficient historical data

### Orders not executing
- Check account balance
- Verify lot size is appropriate for your account
- Ensure symbol is available for trading
- Check MT5 terminal for error messages

## Disclaimer

⚠️ **IMPORTANT DISCLAIMER**

This trading bot is provided for educational purposes only. Trading forex and CFDs involves significant risk of loss and is not suitable for all investors. Past performance is not indicative of future results.

- Never trade with money you cannot afford to lose
- Always test strategies on a demo account first
- Understand the risks before trading live
- The authors are not responsible for any financial losses

## Support

For issues or questions:
1. Check the log file for detailed error messages
2. Review the MT5 terminal journal
3. Ensure all dependencies are installed correctly

## License

This project is open source and available for educational purposes.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.
