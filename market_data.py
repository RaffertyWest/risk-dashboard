import yfinance as yf
import matplotlib.pyplot as plt 
tickers = ["^GSPC", "^FTSE", "EURUSD=X", "JPY=X", "^VIX"]
data = yf.download(tickers, period="1y")["Close"]

returns = data.pct_change().dropna()

def plot_ticker(ticker):
    data[ticker].plot(title=f"{ticker} - 1 Year Closing Prices") #f string - f prior to string allows for variable insertion. No longer quotation marks around ticker as now not a string being handed to yf but a variable to be defined 
    plt.show()

# plot_ticker("^FTSE") plots prices 

# returns.plot()
# plt.show()  together these plot the percentage changes 

def plot_normalised(prices):
    normalised1 = prices / prices.iloc[0]
    normalised2 = normalised1*100
    normalised2.plot()
    plt.show()

plot_normalised(data)