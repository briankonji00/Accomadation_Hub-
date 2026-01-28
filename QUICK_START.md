# MT5 Trading Bot - Quick Reference Guide

## 📋 What You Got

A fully functional MT5 trading bot with:
- ✅ 8 Moving Average indicators (5, 10, 20, 50, 100, 150, 200, 250 periods)
- ✅ Automatic buy/sell signal generation
- ✅ Built-in risk management (Stop Loss & Take Profit)
- ✅ Test mode for safe strategy validation
- ✅ Comprehensive logging and analysis

## 🚀 Quick Start (3 Steps)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Ensure MT5 is Running
- Open MetaTrader 5
- Login to your account
- Enable automated trading: Tools → Options → Expert Advisors → Check "Allow automated trading"

### Step 3: Run the Bot
```bash
# Option A: Use the launcher (recommended for beginners)
python launch_bot.py

# Option B: Run directly in test mode
python mt5_trading_bot.py

# Option C: Run the test suite
python test_mt5_bot.py
```

## 🎯 How the Bot Works

### Trading Logic
1. **Calculates 8 Moving Averages** with different periods
2. **Compares current price** against all MAs
3. **Generates signals**:
   - **BUY** → Price above 60% of MAs (bullish trend)
   - **SELL** → Price below 60% of MAs (bearish trend)
   - **HOLD** → Price between MAs (unclear trend)

### Example Signal Generation
```
Price: 1.08450
MA 5:   1.08420 ✅ (price ABOVE)
MA 10:  1.08390 ✅ (price ABOVE)
MA 20:  1.08350 ✅ (price ABOVE)
MA 50:  1.08280 ✅ (price ABOVE)
MA 100: 1.08200 ✅ (price ABOVE)
MA 150: 1.08150 ✅ (price ABOVE)
MA 200: 1.08100 ✅ (price ABOVE)
MA 250: 1.08050 ✅ (price ABOVE)

Result: 8/8 (100%) above → STRONG BUY SIGNAL
```

## ⚙️ Configuration

Edit `config.py` to customize:

```python
SYMBOL = "EURUSD"           # Trading pair
TIMEFRAME = "M5"            # 5-minute candles
LOT_SIZE = 0.1              # Position size
MA_PERIODS = [5, 10, 20, 50, 100, 150, 200, 250]  # 8 MAs
TEST_MODE = True            # Safe mode (no real trades)
```

## 📊 Understanding the Output

When running, you'll see:
```
============================================================
Market Analysis for EURUSD
Time: 2026-01-28 10:30:00
Current Price: 1.08450
------------------------------------------------------------
MA   5: 1.08420 - Price is ABOVE
MA  10: 1.08390 - Price is ABOVE
[... more MAs ...]
------------------------------------------------------------
SIGNAL: BUY
Current Position: None
============================================================
```

## 🔒 Safety Features

1. **Test Mode** (DEFAULT): Analyzes and shows signals WITHOUT placing trades
2. **Stop Loss**: Automatic 100-point stop loss on each trade
3. **Take Profit**: Automatic 150-point take profit target
4. **Logging**: All activity saved to `mt5_trading_bot.log`
5. **Error Handling**: Comprehensive error checking and recovery

## 📁 File Overview

| File | Purpose |
|------|---------|
| `mt5_trading_bot.py` | Main bot implementation |
| `launch_bot.py` | User-friendly launcher |
| `test_mt5_bot.py` | Test suite to validate setup |
| `config.py` | Configuration settings |
| `requirements.txt` | Python dependencies |
| `MT5_BOT_README.md` | Full documentation |
| `.gitignore` | Excludes logs and cache files |

## 🎮 Usage Modes

### 1. Test Mode (Recommended First)
```bash
python mt5_trading_bot.py
```
- Shows signals
- No real trades
- Perfect for learning

### 2. Single Analysis
```bash
python launch_bot.py
# Select option 3
```
- One-time market analysis
- View current signals
- No continuous monitoring

### 3. Live Trading (⚠️ Use with Caution!)
```python
# Edit mt5_trading_bot.py
TEST_MODE = False  # Change this line

# Then run
python mt5_trading_bot.py
```

## 🔧 Customization Examples

### Change MA Periods to Fibonacci Numbers
```python
# In mt5_trading_bot.py
self.ma_periods = [8, 13, 21, 34, 55, 89, 144, 233]
```

### Use Different Timeframes
```python
# In mt5_trading_bot.py
TIMEFRAME = mt5.TIMEFRAME_M15  # 15-minute candles
TIMEFRAME = mt5.TIMEFRAME_H1   # 1-hour candles
TIMEFRAME = mt5.TIMEFRAME_H4   # 4-hour candles
```

### Adjust Signal Threshold
```python
# In generate_signals method
if above_ma_count / total_valid_mas >= 0.7:  # Change to 70%
    return 'buy'
```

## ❓ Common Questions

**Q: Do I need a live account?**
A: No! Start with a demo account from any MT5 broker.

**Q: Will this make me money?**
A: No guarantee! This is a tool, not a magic money printer. Always test thoroughly.

**Q: Can I run multiple symbols?**
A: Yes, but run separate bot instances for each symbol.

**Q: What if MT5 closes?**
A: The bot will stop. Keep MT5 running while trading.

**Q: How do I stop the bot?**
A: Press `Ctrl+C` in the terminal.

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| "MT5 initialization failed" | Ensure MT5 is open and logged in |
| "Symbol not found" | Check symbol name in Market Watch |
| "Failed to get rates" | Verify symbol has historical data |
| "Order failed" | Check account balance and connection |

## ⚠️ Important Reminders

1. **Always test first** with TEST_MODE = True
2. **Use demo account** before live trading
3. **Never risk** more than you can afford to lose
4. **Monitor the bot** - don't leave it unattended
5. **Understand the strategy** before using it
6. **Check logs** regularly in `mt5_trading_bot.log`

## 📚 Next Steps

1. ✅ Install dependencies
2. ✅ Run test suite: `python test_mt5_bot.py`
3. ✅ Try launcher: `python launch_bot.py`
4. ✅ Observe in test mode
5. ✅ Backtest your strategy
6. ✅ Paper trade on demo
7. ⚠️ Go live (only if confident)

## 📞 Need Help?

1. Check `mt5_trading_bot.log` for detailed errors
2. Review MT5 terminal journal
3. Read the full documentation in `MT5_BOT_README.md`

---

**Remember**: This bot is a tool for education and automation. Success depends on market conditions, proper configuration, and risk management. Trade responsibly! 📈
