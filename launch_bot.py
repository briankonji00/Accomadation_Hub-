"""
Quick Start Launcher for MT5 Trading Bot
Simple interface to run the bot with different configurations
"""

import MetaTrader5 as mt5
from mt5_trading_bot import MT5TradingBot
import sys


def print_menu():
    """Display main menu"""
    print("\n" + "="*60)
    print("      MT5 Trading Bot - Quick Start Launcher")
    print("="*60)
    print("\nChoose an option:")
    print("\n1. Run bot in TEST MODE (recommended for beginners)")
    print("2. Run bot in LIVE TRADING MODE (⚠️  WARNING: Real money!)")
    print("3. Run single analysis (no trading)")
    print("4. View current market status")
    print("5. Exit")
    print("\n" + "="*60)


def get_user_input(prompt, default=None):
    """Get user input with default value"""
    if default:
        user_input = input(f"{prompt} (default: {default}): ").strip()
        return user_input if user_input else default
    return input(f"{prompt}: ").strip()


def validate_positive_float(value, name, min_val=0.01, max_val=100.0):
    """Validate that a value is a positive float within range"""
    try:
        num = float(value)
        if num <= 0:
            print(f"❌ {name} must be positive")
            return None
        if num < min_val or num > max_val:
            print(f"❌ {name} must be between {min_val} and {max_val}")
            return None
        return num
    except ValueError:
        print(f"❌ Invalid number for {name}")
        return None


def validate_positive_int(value, name, min_val=1, max_val=3600):
    """Validate that a value is a positive integer within range"""
    try:
        num = int(value)
        if num <= 0:
            print(f"❌ {name} must be positive")
            return None
        if num < min_val or num > max_val:
            print(f"❌ {name} must be between {min_val} and {max_val}")
            return None
        return num
    except ValueError:
        print(f"❌ Invalid number for {name}")
        return None


def run_test_mode():
    """Run bot in test mode"""
    print("\n" + "="*60)
    print("Running in TEST MODE")
    print("="*60)
    
    symbol = get_user_input("Enter symbol", "EURUSD")
    
    # Get and validate lot size
    while True:
        lot_input = get_user_input("Enter lot size", "0.1")
        lot_size = validate_positive_float(lot_input, "Lot size", 0.01, 10.0)
        if lot_size is not None:
            break
    
    # Get and validate interval
    while True:
        interval_input = get_user_input("Check interval (seconds)", "60")
        interval = validate_positive_int(interval_input, "Interval", 10, 3600)
        if interval is not None:
            break
    
    print(f"\nStarting bot with:")
    print(f"  Symbol: {symbol}")
    print(f"  Lot Size: {lot_size}")
    print(f"  Check Interval: {interval}s")
    print(f"  Mode: TEST (no real trades)")
    
    confirm = input("\nProceed? (y/n): ").strip().lower()
    
    if confirm == 'y':
        bot = MT5TradingBot(
            symbol=symbol,
            timeframe=mt5.TIMEFRAME_M5,
            lot_size=lot_size
        )
        bot.run(test_mode=True, interval=interval)
    else:
        print("Cancelled.")


def run_live_mode():
    """Run bot in live trading mode"""
    print("\n" + "="*60)
    print("⚠️  WARNING: LIVE TRADING MODE")
    print("="*60)
    print("\nThis will place REAL trades with REAL money!")
    print("Make sure you understand the risks involved.")
    
    confirm1 = input("\nDo you understand the risks? (yes/no): ").strip().lower()
    
    if confirm1 != 'yes':
        print("Cancelled. Please use test mode first.")
        return
    
    symbol = get_user_input("Enter symbol", "EURUSD")
    
    # Get and validate lot size
    while True:
        lot_input = get_user_input("Enter lot size", "0.1")
        lot_size = validate_positive_float(lot_input, "Lot size", 0.01, 10.0)
        if lot_size is not None:
            break
    
    # Get and validate interval
    while True:
        interval_input = get_user_input("Check interval (seconds)", "60")
        interval = validate_positive_int(interval_input, "Interval", 10, 3600)
        if interval is not None:
            break
    
    print(f"\nStarting LIVE bot with:")
    print(f"  Symbol: {symbol}")
    print(f"  Lot Size: {lot_size}")
    print(f"  Check Interval: {interval}s")
    print(f"  Mode: LIVE (REAL TRADES)")
    
    confirm2 = input("\nFinal confirmation - Start live trading? (yes/no): ").strip().lower()
    
    if confirm2 == 'yes':
        bot = MT5TradingBot(
            symbol=symbol,
            timeframe=mt5.TIMEFRAME_M5,
            lot_size=lot_size
        )
        bot.run(test_mode=False, interval=interval)
    else:
        print("Cancelled.")


def run_single_analysis():
    """Run a single market analysis"""
    print("\n" + "="*60)
    print("Single Market Analysis")
    print("="*60)
    
    symbol = get_user_input("Enter symbol", "EURUSD")
    
    bot = MT5TradingBot(symbol=symbol, timeframe=mt5.TIMEFRAME_M5)
    
    if not bot.initialize_mt5():
        print("Failed to connect to MT5")
        return
    
    try:
        df = bot.get_rates(count=300)
        if df is None:
            print("Failed to get market data")
            return
        
        df = bot.calculate_moving_averages(df)
        signal = bot.generate_signals(df)
        bot.print_analysis(df, signal)
        
        print(f"\n✅ Analysis complete")
        print(f"   Recommendation: {signal.upper()}")
        
    finally:
        bot.shutdown_mt5()


def view_market_status():
    """View current market status"""
    print("\n" + "="*60)
    print("Current Market Status")
    print("="*60)
    
    if not mt5.initialize():
        print(f"❌ Failed to connect to MT5: {mt5.last_error()}")
        return
    
    try:
        # Get account info
        account = mt5.account_info()
        if account:
            print(f"\nAccount Information:")
            print(f"  Login: {account.login}")
            print(f"  Server: {account.server}")
            print(f"  Balance: ${account.balance:.2f}")
            print(f"  Equity: ${account.equity:.2f}")
            print(f"  Margin: ${account.margin:.2f}")
            print(f"  Free Margin: ${account.margin_free:.2f}")
        
        # Get positions
        positions = mt5.positions_get()
        print(f"\nOpen Positions: {len(positions) if positions else 0}")
        
        if positions:
            for pos in positions:
                print(f"\n  Symbol: {pos.symbol}")
                print(f"  Type: {'BUY' if pos.type == 0 else 'SELL'}")
                print(f"  Volume: {pos.volume}")
                print(f"  Price: {pos.price_open}")
                print(f"  Current: {pos.price_current}")
                print(f"  Profit: ${pos.profit:.2f}")
        
        # Get popular symbols
        symbols = ["EURUSD", "GBPUSD", "USDJPY", "AUDUSD"]
        print(f"\nCurrent Prices:")
        
        for symbol in symbols:
            tick = mt5.symbol_info_tick(symbol)
            if tick:
                print(f"  {symbol}: Bid {tick.bid:.5f} / Ask {tick.ask:.5f}")
        
    finally:
        mt5.shutdown()


def main():
    """Main launcher function"""
    while True:
        print_menu()
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == '1':
            run_test_mode()
        elif choice == '2':
            run_live_mode()
        elif choice == '3':
            run_single_analysis()
        elif choice == '4':
            view_market_status()
        elif choice == '5':
            print("\nThank you for using MT5 Trading Bot!")
            print("Happy trading! 📈")
            sys.exit(0)
        else:
            print("\n❌ Invalid choice. Please enter 1-5.")
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nBot stopped by user. Goodbye!")
        sys.exit(0)
