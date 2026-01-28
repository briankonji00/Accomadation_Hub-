# Accommodation Hub & MT5 Trading Bot

This repository contains two distinct projects:

## 1. 🏠 Accommodation Hub Website

A web platform designed to help university students find off-campus accommodation.

### Features
- Modern, responsive design
- Image carousel showcasing properties
- Login system for users
- Easy navigation and user-friendly interface

### Files
- `index.html` - Main landing page
- `login_page.html` - User login page
- `styles.css` - Styling
- `script.js` - Interactive features

## 2. 📈 MT5 Trading Bot

An automated trading bot for MetaTrader 5 that uses multiple moving averages to generate trading signals.

### Key Features
- ✅ **8 Moving Average Indicators** (5, 10, 20, 50, 100, 150, 200, 250 periods)
- ✅ **Automated Buy/Sell Signals** based on price position relative to MAs
- ✅ **Risk Management** with Stop Loss and Take Profit
- ✅ **Test Mode** for safe strategy validation
- ✅ **Comprehensive Logging** and market analysis
- ✅ **User-Friendly Interface** with multiple execution modes

### Trading Strategy
- **BUY Signal**: When price is above 60% or more of the moving averages
- **SELL Signal**: When price is below 60% or more of the moving averages
- **HOLD**: When price is between moving averages without clear trend

### Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Ensure MT5 is Running**
   - Open MetaTrader 5 terminal
   - Login to your account (demo or live)
   - Enable automated trading in settings

3. **Run the Bot**
   ```bash
   # Easy launcher with menu
   python launch_bot.py
   
   # Or run directly in test mode
   python mt5_trading_bot.py
   
   # Or run tests
   python test_mt5_bot.py
   ```

### Documentation

- **[QUICK_START.md](QUICK_START.md)** - Fast setup guide and quick reference
- **[MT5_BOT_README.md](MT5_BOT_README.md)** - Complete documentation with examples
- **[config.py](config.py)** - Configuration settings

### Bot Files
- `mt5_trading_bot.py` - Main bot implementation
- `launch_bot.py` - Interactive launcher
- `test_mt5_bot.py` - Test suite
- `config.py` - Configuration
- `requirements.txt` - Python dependencies

### Safety First! ⚠️

The bot runs in **TEST MODE** by default, which means:
- It analyzes the market and shows signals
- It does **NOT** place real trades
- Perfect for learning and strategy validation

**Important**: Always test thoroughly on a demo account before considering live trading!

### Example Output

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

### Customization

You can easily customize:
- Trading symbols (EURUSD, GBPUSD, etc.)
- Moving average periods
- Timeframes (M5, M15, H1, H4, D1)
- Signal thresholds
- Risk parameters (Stop Loss, Take Profit)

See [MT5_BOT_README.md](MT5_BOT_README.md) for detailed customization examples.

## 📄 License

Open source - Educational purposes

## ⚠️ Disclaimer

**For the MT5 Trading Bot**: Trading forex and CFDs involves significant risk of loss. This bot is provided for educational purposes only. Always use a demo account for testing, understand the risks, and never trade with money you cannot afford to lose. The authors are not responsible for any financial losses.

---

© 2024-2026 Accommodation Hub. All rights reserved.
