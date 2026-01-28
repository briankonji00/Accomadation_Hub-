"""
MT5 Trading Bot with Multiple Moving Average Strategy
This bot uses 8 different moving averages to generate buy/sell signals
"""

import MetaTrader5 as mt5
import pandas as pd
import numpy as np
from datetime import datetime
import time
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('mt5_trading_bot.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class MT5TradingBot:
    """
    MT5 Trading Bot that uses multiple moving averages for trading signals
    """
    
    def __init__(self, symbol="EURUSD", timeframe=mt5.TIMEFRAME_M5, lot_size=0.1):
        """
        Initialize the trading bot
        
        Args:
            symbol: Trading symbol (default: EURUSD)
            timeframe: Timeframe for analysis (default: M5)
            lot_size: Position size (default: 0.1)
        """
        self.symbol = symbol
        self.timeframe = timeframe
        self.lot_size = lot_size
        
        # 8 different moving average periods
        self.ma_periods = [5, 10, 20, 50, 100, 150, 200, 250]
        
        # Trading state
        self.current_position = None  # None, 'buy', or 'sell'
        
    def initialize_mt5(self):
        """Initialize connection to MetaTrader 5"""
        if not mt5.initialize():
            logger.error(f"MT5 initialization failed: {mt5.last_error()}")
            return False
        
        logger.info("MT5 initialized successfully")
        logger.info(f"MT5 version: {mt5.version()}")
        return True
    
    def shutdown_mt5(self):
        """Shutdown MT5 connection"""
        mt5.shutdown()
        logger.info("MT5 connection closed")
    
    def get_rates(self, count=500):
        """
        Get historical price data
        
        Args:
            count: Number of candles to retrieve
            
        Returns:
            pandas DataFrame with OHLC data
        """
        rates = mt5.copy_rates_from_pos(self.symbol, self.timeframe, 0, count)
        
        if rates is None or len(rates) == 0:
            logger.error(f"Failed to get rates: {mt5.last_error()}")
            return None
        
        # Convert to DataFrame
        df = pd.DataFrame(rates)
        df['time'] = pd.to_datetime(df['time'], unit='s')
        
        return df
    
    def calculate_moving_averages(self, df):
        """
        Calculate 8 different moving averages
        
        Args:
            df: DataFrame with price data
            
        Returns:
            DataFrame with added MA columns
        """
        for period in self.ma_periods:
            df[f'MA_{period}'] = df['close'].rolling(window=period).mean()
        
        return df
    
    def generate_signals(self, df):
        """
        Generate buy/sell signals based on moving averages
        
        Strategy:
        - BUY: When price crosses above the majority of MAs
        - SELL: When price crosses below the majority of MAs
        
        Args:
            df: DataFrame with price and MA data
            
        Returns:
            Signal: 'buy', 'sell', or 'hold'
        """
        if df is None or len(df) < max(self.ma_periods):
            return 'hold'
        
        latest_price = df['close'].iloc[-1]
        
        # Count how many MAs the price is above
        above_ma_count = 0
        below_ma_count = 0
        
        for period in self.ma_periods:
            ma_value = df[f'MA_{period}'].iloc[-1]
            
            if pd.notna(ma_value):
                if latest_price > ma_value:
                    above_ma_count += 1
                elif latest_price < ma_value:
                    below_ma_count += 1
        
        # Generate signals based on majority
        total_valid_mas = above_ma_count + below_ma_count
        
        if total_valid_mas == 0:
            return 'hold'
        
        # Buy signal: price above at least 60% of MAs
        if above_ma_count / total_valid_mas >= 0.6:
            return 'buy'
        # Sell signal: price below at least 60% of MAs
        elif below_ma_count / total_valid_mas >= 0.6:
            return 'sell'
        else:
            return 'hold'
    
    def get_symbol_info(self):
        """Get symbol information"""
        symbol_info = mt5.symbol_info(self.symbol)
        
        if symbol_info is None:
            logger.error(f"Symbol {self.symbol} not found")
            return None
        
        if not symbol_info.visible:
            logger.info(f"Symbol {self.symbol} is not visible, trying to enable")
            if not mt5.symbol_select(self.symbol, True):
                logger.error(f"Failed to select {self.symbol}")
                return None
        
        return symbol_info
    
    def place_buy_order(self):
        """Place a buy order"""
        symbol_info = self.get_symbol_info()
        if symbol_info is None:
            return False
        
        price = mt5.symbol_info_tick(self.symbol).ask
        point = symbol_info.point
        
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": self.symbol,
            "volume": self.lot_size,
            "type": mt5.ORDER_TYPE_BUY,
            "price": price,
            "sl": price - 100 * point,  # Stop loss
            "tp": price + 150 * point,  # Take profit
            "deviation": 10,
            "magic": 234000,
            "comment": "MT5 Bot Buy",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        
        result = mt5.order_send(request)
        
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            logger.error(f"Buy order failed: {result.retcode}, {result.comment}")
            return False
        
        logger.info(f"Buy order executed at {price}")
        self.current_position = 'buy'
        return True
    
    def place_sell_order(self):
        """Place a sell order"""
        symbol_info = self.get_symbol_info()
        if symbol_info is None:
            return False
        
        price = mt5.symbol_info_tick(self.symbol).bid
        point = symbol_info.point
        
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": self.symbol,
            "volume": self.lot_size,
            "type": mt5.ORDER_TYPE_SELL,
            "price": price,
            "sl": price + 100 * point,  # Stop loss
            "tp": price - 150 * point,  # Take profit
            "deviation": 10,
            "magic": 234000,
            "comment": "MT5 Bot Sell",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        
        result = mt5.order_send(request)
        
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            logger.error(f"Sell order failed: {result.retcode}, {result.comment}")
            return False
        
        logger.info(f"Sell order executed at {price}")
        self.current_position = 'sell'
        return True
    
    def close_position(self):
        """Close current position"""
        positions = mt5.positions_get(symbol=self.symbol)
        
        if positions is None or len(positions) == 0:
            logger.info("No positions to close")
            self.current_position = None
            return True
        
        for position in positions:
            tick = mt5.symbol_info_tick(self.symbol)
            
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": self.symbol,
                "volume": position.volume,
                "type": mt5.ORDER_TYPE_BUY if position.type == mt5.ORDER_TYPE_SELL else mt5.ORDER_TYPE_SELL,
                "position": position.ticket,
                "price": tick.ask if position.type == mt5.ORDER_TYPE_SELL else tick.bid,
                "deviation": 10,
                "magic": 234000,
                "comment": "MT5 Bot Close",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }
            
            result = mt5.order_send(request)
            
            if result.retcode != mt5.TRADE_RETCODE_DONE:
                logger.error(f"Failed to close position: {result.retcode}")
                return False
            
            logger.info(f"Position closed: {position.ticket}")
        
        self.current_position = None
        return True
    
    def print_analysis(self, df, signal):
        """Print current market analysis"""
        latest_price = df['close'].iloc[-1]
        
        logger.info("=" * 60)
        logger.info(f"Market Analysis for {self.symbol}")
        logger.info(f"Time: {df['time'].iloc[-1]}")
        logger.info(f"Current Price: {latest_price:.5f}")
        logger.info("-" * 60)
        
        for period in self.ma_periods:
            ma_value = df[f'MA_{period}'].iloc[-1]
            if pd.notna(ma_value):
                position = "ABOVE" if latest_price > ma_value else "BELOW"
                logger.info(f"MA {period:3d}: {ma_value:.5f} - Price is {position}")
        
        logger.info("-" * 60)
        logger.info(f"SIGNAL: {signal.upper()}")
        logger.info(f"Current Position: {self.current_position}")
        logger.info("=" * 60)
    
    def run(self, test_mode=True, interval=60):
        """
        Run the trading bot
        
        Args:
            test_mode: If True, only analyze without placing orders
            interval: Time between iterations in seconds
        """
        if not self.initialize_mt5():
            return
        
        logger.info(f"Starting MT5 Trading Bot")
        logger.info(f"Symbol: {self.symbol}")
        logger.info(f"Timeframe: {self.timeframe}")
        logger.info(f"MA Periods: {self.ma_periods}")
        logger.info(f"Test Mode: {test_mode}")
        
        try:
            while True:
                # Get latest data
                df = self.get_rates()
                
                if df is None:
                    logger.warning("Failed to get rates, skipping iteration")
                    time.sleep(interval)
                    continue
                
                # Calculate moving averages
                df = self.calculate_moving_averages(df)
                
                # Generate signal
                signal = self.generate_signals(df)
                
                # Print analysis
                self.print_analysis(df, signal)
                
                # Execute trades (if not in test mode)
                if not test_mode:
                    if signal == 'buy' and self.current_position != 'buy':
                        if self.current_position == 'sell':
                            self.close_position()
                        self.place_buy_order()
                    elif signal == 'sell' and self.current_position != 'sell':
                        if self.current_position == 'buy':
                            self.close_position()
                        self.place_sell_order()
                else:
                    logger.info("Test mode: No orders placed")
                
                # Wait for next iteration
                logger.info(f"Waiting {interval} seconds for next analysis...")
                time.sleep(interval)
                
        except KeyboardInterrupt:
            logger.info("Bot stopped by user")
        except Exception as e:
            logger.error(f"Error in bot execution: {e}")
        finally:
            self.shutdown_mt5()


def main():
    """Main function to run the bot"""
    # Configuration
    SYMBOL = "EURUSD"
    TIMEFRAME = mt5.TIMEFRAME_M5  # 5-minute candles
    LOT_SIZE = 0.1
    TEST_MODE = True  # Set to False for live trading
    INTERVAL = 60  # Check every 60 seconds
    
    # Create and run bot
    bot = MT5TradingBot(
        symbol=SYMBOL,
        timeframe=TIMEFRAME,
        lot_size=LOT_SIZE
    )
    
    bot.run(test_mode=TEST_MODE, interval=INTERVAL)


if __name__ == "__main__":
    main()
