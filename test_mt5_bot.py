"""
Example script to test the MT5 Trading Bot
This script demonstrates how to use the bot and test its functionality
"""

import MetaTrader5 as mt5
from mt5_trading_bot import MT5TradingBot
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def test_connection():
    """Test MT5 connection"""
    print("\n" + "="*60)
    print("Testing MT5 Connection")
    print("="*60)
    
    if not mt5.initialize():
        print(f"❌ MT5 initialization failed: {mt5.last_error()}")
        return False
    
    print("✅ MT5 initialized successfully")
    print(f"   Version: {mt5.version()}")
    
    account_info = mt5.account_info()
    if account_info:
        print(f"   Account: {account_info.login}")
        print(f"   Server: {account_info.server}")
        print(f"   Balance: ${account_info.balance}")
        print(f"   Currency: {account_info.currency}")
    
    mt5.shutdown()
    return True


def test_data_retrieval(symbol="EURUSD"):
    """Test data retrieval from MT5"""
    print("\n" + "="*60)
    print(f"Testing Data Retrieval for {symbol}")
    print("="*60)
    
    bot = MT5TradingBot(symbol=symbol)
    
    if not bot.initialize_mt5():
        return False
    
    # Get data
    df = bot.get_rates(count=300)
    
    if df is None:
        print(f"❌ Failed to retrieve data for {symbol}")
        bot.shutdown_mt5()
        return False
    
    print(f"✅ Successfully retrieved {len(df)} candles")
    print(f"   Timeframe: M5 (5 minutes)")
    print(f"   Latest price: {df['close'].iloc[-1]:.5f}")
    print(f"   Date range: {df['time'].iloc[0]} to {df['time'].iloc[-1]}")
    
    bot.shutdown_mt5()
    return True


def test_moving_averages(symbol="EURUSD"):
    """Test moving average calculations"""
    print("\n" + "="*60)
    print("Testing Moving Average Calculations")
    print("="*60)
    
    bot = MT5TradingBot(symbol=symbol)
    
    if not bot.initialize_mt5():
        return False
    
    # Get data
    df = bot.get_rates(count=300)
    
    if df is None:
        bot.shutdown_mt5()
        return False
    
    # Calculate MAs
    df = bot.calculate_moving_averages(df)
    
    latest_price = df['close'].iloc[-1]
    print(f"Current Price: {latest_price:.5f}\n")
    
    print("Moving Averages:")
    for period in bot.ma_periods:
        ma_value = df[f'MA_{period}'].iloc[-1]
        if not pd.isna(ma_value):
            diff = latest_price - ma_value
            percentage = (diff / ma_value) * 100
            position = "ABOVE" if diff > 0 else "BELOW"
            print(f"  MA {period:3d}: {ma_value:.5f} ({position} by {abs(percentage):.2f}%)")
        else:
            print(f"  MA {period:3d}: N/A (insufficient data)")
    
    bot.shutdown_mt5()
    return True


def test_signal_generation(symbol="EURUSD"):
    """Test signal generation"""
    print("\n" + "="*60)
    print("Testing Signal Generation")
    print("="*60)
    
    bot = MT5TradingBot(symbol=symbol)
    
    if not bot.initialize_mt5():
        return False
    
    # Get and process data
    df = bot.get_rates(count=300)
    if df is None:
        bot.shutdown_mt5()
        return False
    
    df = bot.calculate_moving_averages(df)
    signal = bot.generate_signals(df)
    
    print(f"Generated Signal: {signal.upper()}")
    
    # Print analysis
    bot.print_analysis(df, signal)
    
    bot.shutdown_mt5()
    return True


def run_single_analysis(symbol="EURUSD"):
    """Run a single market analysis"""
    print("\n" + "="*60)
    print("Running Single Market Analysis")
    print("="*60)
    
    bot = MT5TradingBot(
        symbol=symbol,
        timeframe=mt5.TIMEFRAME_M5,
        lot_size=0.1
    )
    
    if not bot.initialize_mt5():
        return False
    
    try:
        # Get data
        df = bot.get_rates(count=300)
        
        if df is None:
            print("Failed to get data")
            return False
        
        # Calculate MAs
        df = bot.calculate_moving_averages(df)
        
        # Generate signal
        signal = bot.generate_signals(df)
        
        # Print analysis
        bot.print_analysis(df, signal)
        
        print("\n📊 Analysis complete!")
        print(f"   Recommendation: {signal.upper()}")
        
        return True
        
    finally:
        bot.shutdown_mt5()


def main():
    """Run all tests"""
    print("\n" + "#"*60)
    print("# MT5 Trading Bot - Test Suite")
    print("#"*60)
    
    import pandas as pd  # Import here for test functions
    
    tests = [
        ("Connection Test", test_connection),
        ("Data Retrieval Test", lambda: test_data_retrieval("EURUSD")),
        ("Moving Average Test", lambda: test_moving_averages("EURUSD")),
        ("Signal Generation Test", lambda: test_signal_generation("EURUSD")),
        ("Single Analysis", lambda: run_single_analysis("EURUSD")),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            logger.error(f"Error in {test_name}: {e}")
            results.append((test_name, False))
    
    # Print summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! The bot is ready to use.")
        print("\nNext steps:")
        print("1. Review the configuration in config.py")
        print("2. Run the bot in test mode: python mt5_trading_bot.py")
        print("3. Monitor the logs and signals")
        print("4. When confident, switch to live trading (at your own risk!)")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")


if __name__ == "__main__":
    main()
