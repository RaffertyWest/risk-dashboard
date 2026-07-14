import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt

tickers = ["^GSPC", "^FTSE", "EURUSD=X", "JPY=X"] # removal of VIX from market_data variant as disrupts graph axes and was the only non financial instrument being displayed, will be stored elsewhere further down the line
data = yf.download(tickers, period="1y")["Close"] #Appended [] must contain internal speach marks 

returns = data.pct_change().dropna()
 # print(returns.columns) prints tickers in alphabetical order, with the indices last - relevant for weightings

weightings = [0.10, 0.20, 0.20, 0.50] # Equity focused with supporting FX
portfolio_returns = (returns*weightings).sum(axis=1) #axis 1 refers to running down columns where 0 is along rows 
print(portfolio_returns.head())

# historical VaR - value at risk - using 95% VaR it finds the worst 5% of days performance wise

VaR_95 = np.percentile(portfolio_returns, 5)
VaR_99 = np.percentile(portfolio_returns, 1)
print(VaR_95, VaR_99)

print((portfolio_returns < VaR_95).sum()) #broadcasts across the whole series, in line with how the multiplication of returns*weightings does. Then sum adds trues as 1

book = 10_000
print(f"1 day 95% VaR: on 95% of the days the portfolio loses no more than {-VaR_95*100:.2f}% (£{-VaR_95*book:,.2f} on a £10,000 book)")
#:.2f reports number to 2 decimal points, :,.2f reports it with thousands commas
# In this specifc scenario, the VaR has been trained on tranquil past year and thus in unprecedented times where the future doesn't reflect this
# it will struggle 