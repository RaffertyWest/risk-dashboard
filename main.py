import yfinance as yf

sp500 = yf.Ticker("^GSPC")  #Allows date pull from markets 
data = sp500.history(period="1d")
print(data["Close"])