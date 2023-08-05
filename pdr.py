import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import mplfinance as mpf
import datetime
import talib
import tkinter as tk
from tkinter import messagebox

def generate_stock_chart():
    try:
        # Get user inputs
        stock_name = stock_entry.get()
        start_input = start_entry.get()

        # Parse the start date
        start = datetime.datetime.strptime(start_input, '%Y-%m-%d')

        # Download historical stock data for the given stock from Yahoo Finance
        df_stock = yf.download(stock_name, start=start)

        # Plot a candlestick chart for the stock using mplfinance
        mpf.plot(df_stock, type='candle', style='yahoo', title=f'{stock_name} Candlestick Chart')

        # Format the date index to be in the format 'YYYY-MM-DD'
        df_stock.index = df_stock.index.strftime('%Y-%m-%d')

        # Calculate the 50-day and 200-day simple moving averages (SMA) of the 'Close' price
        sma_50 = talib.SMA(np.array(df_stock['Close']), timeperiod=50)
        sma_200 = talib.SMA(np.array(df_stock['Close']), timeperiod=200)

        # Create a new figure and subplot to plot the candlestick chart with the moving averages
        fig = plt.figure(figsize=(24, 8))
        ax = fig.add_subplot(1, 1, 1)
        ax.set_xticks(range(0, len(df_stock.index), 30))
        ax.set_xticklabels(df_stock.index[::10])
        mpf.plot(df_stock, ax=ax, type='candle', style='yahoo', title=f'{stock_name} Candlestick Chart with Moving Averages', warn_too_much_data=500)
        ax.plot(sma_50, label='50 day average')  # Plot the 50-day moving average
        ax.plot(sma_200, label='200 day average')  # Plot the 200-day moving average
        ax.legend()

        # Calculate the 10-day and 30-day simple moving averages (SMA) of the 'Close' price
        sma_10 = talib.SMA(np.array(df_stock['Close']), timeperiod=10)
        sma_30 = talib.SMA(np.array(df_stock['Close']), timeperiod=30)

        # Calculate the Stochastic Oscillator (KD) values for the 'High', 'Low', and 'Close' prices
        df_stock['k'], df_stock['d'] = talib.STOCH(df_stock['High'], df_stock['Low'], df_stock['Close'])

        # Fill any NaN (Not a Number) values in the 'k' and 'd' columns with 0
        df_stock['k'].fillna(value=0, inplace=True)
        df_stock['d'].fillna(value=0, inplace=True)

        # Create a new figure and multiple subplots to plot the candlestick chart, moving averages, and KD indicator
        fig = plt.figure(figsize=(24, 20))
        ax = fig.add_axes([0, 0.3, 1, 0.4])  # Main subplot for the candlestick chart and moving averages
        ax2 = fig.add_axes([0, 0.2, 1, 0.1])  # Subplot for the KD values
        ax3 = fig.add_axes([0, 0, 1, 0.2])  # Subplot for the volume overlay

        ax.set_xticks(range(0, len(df_stock.index), 10))
        ax.set_xticklabels(df_stock.index[::10])
        mpf.plot(df_stock, ax=ax, type='candle', style='yahoo', title=f'{stock_name} Candlestick Chart with Moving Averages and KD Indicator', warn_too_much_data=500)
        ax.plot(sma_10, label='10 day average')  # Plot the 10-day moving average
        ax.plot(sma_30, label='30 day average')  # Plot the 30-day moving average

        ax2.plot(df_stock['k'], label='K value')  # Plot the 'K' value of the Stochastic Oscillator
        ax2.plot(df_stock['d'], label='D value')  # Plot the 'D' value of the Stochastic Oscillator
        ax2.set_xticks(range(0, len(df_stock.index), 10))
        ax2.set_xticklabels(df_stock.index[::10])
        ax2.legend()

        # Create a volume overlay on the third subplot to show the volume bars corresponding to price changes
        mpf.volume_overlay(ax3, df_stock['Open'], df_stock['Close'], df_stock['Volume'], colorup='r', colordown='g', width=0.5, alpha=0.8)
        ax3.set_xticks(range(0, len(df_stock.index), 10))
        ax3.set_xticklabels(df_stock.index[::10])

        ax.legend()

        # Save the completed graph to the specified pathway
        plt.ioff()  # Disable interactive mode
        plt.savefig(f'/Users/tuckerhoneycutt/Pictures/Stock Trading Graphs/{stock_name}_Candlestick_Chart.png')
        plt.show()  # Re-enable interactive mode if needed

    except Exception as e:
        messagebox.showerror("Error", f"Error occurred while fetching data from Yahoo Finance: {e}")

# Create the main application window
app = tk.Tk()
app.title("Stock Trading Graph Generator")

# Create and place labels and entry fields for stock name and start date
stock_label = tk.Label(app, text="Enter the stock name (e.g., KO for Coca-Cola):")
stock_label.pack()
stock_entry = tk.Entry(app)
stock_entry.pack()

start_label = tk.Label(app, text="Enter the start date in the format YYYY-MM-DD (e.g., 2020-09-01):")
start_label.pack()
start_entry = tk.Entry(app)
start_entry.pack()

# Create and place the "Generate Chart" button
generate_button = tk.Button(app, text="Generate Chart", command=generate_stock_chart)
generate_button.pack()

app.mainloop()
