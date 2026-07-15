import yfinance as yf
import numpy as np

tickers = ["^GSPC", "^FTSE", "EURUSD=X", "JPY=X"] # removal of VIX from market_data variant as disrupts graph axes and was the only non financial instrument being displayed, will be stored elsewhere further down the line
data = yf.download(tickers, period="1y")["Close"] 

returns = data.pct_change().dropna()
# print(returns.columns) prints tickers in alphabetical order, with the indices last - relevant for weightings

if len(returns.columns) != len(tickers):
    raise ValueError("Data download incomplete, run stopped prior to incorrect downstream calculations")
#Prevents runs that fail to download all data from yf


weightings = [0.10, 0.20, 0.20, 0.50] # Equity focused with supporting FX
portfolio_returns = (returns*weightings).sum(axis=1) #axis 1 refers to collapsing columns and keeping rows
print(f"Daily portfolio returns snapshot: {portfolio_returns.head()}")

VaR_95 = np.percentile(portfolio_returns, 5)
VaR_99 = np.percentile(portfolio_returns, 1)
print(f"Historical VaR 95: {VaR_95:.2%}, Historical VaR 99: {VaR_99:.2%}")

print(f"Breaches of 95% VaR: {(portfolio_returns < VaR_95).sum()}") #broadcasts across the whole series, in line with how the multiplication of returns*weightings does. Then sum adds trues as 1

book = 10_000
print(f"1 day 95% VaR: on 95% of the days the portfolio loses no more than {-VaR_95*100:.2f}% (£{-VaR_95*book:,.2f} on a £10,000 book)")
#:.2f reports number to 2 decimal points, :,.2f reports it with thousands commas

returns_mean = returns.mean()   #daily average return
cov_matrix = returns.cov() #4x4 matrix with solo variance (how much daily returns scatter around the average) on the diag and covariance on the off diags 
# print(returns_mean)
# print(cov_matrix)

np.random.seed(1) # pins the starting state so each rerun samples the same "random" distribution
simulated = np.random.multivariate_normal(returns_mean, cov_matrix, 10_000)  #raw number array, no headers (cf pandas dataframes that carry labels)
# print(simulated.shape)

simulated_portfolio_returns = (simulated*weightings).sum(axis=1)
sim_VaR_95 = np.percentile(simulated_portfolio_returns, 5)
sim_VaR_99 = np.percentile(simulated_portfolio_returns, 1)
print(f"Monte Carlo VaR 95: {sim_VaR_95:.2%}, Monte Carlo VaR 99: {sim_VaR_99:.2%}")

# Monte values less extreme. Normal distributions by construction, bell curve under predicts extreme days when compared to real markets (i.e. thin tails - therefore deviation most notable for 99% deep into the tail)

boolean_mask1 = simulated_portfolio_returns < sim_VaR_95
print(f"Expected shortfall 95% - Monte Carlo: {simulated_portfolio_returns[boolean_mask1].mean():.2%}")

boolean_mask2 = simulated_portfolio_returns < sim_VaR_99
print(f"Expected shortfall 99% - Monte Carlo: {simulated_portfolio_returns[boolean_mask2].mean():.2%}") #Format is series[mask].mean(), the mask filters for instances where it is True, keeping it in square brackets allows the values to be unaffected and then these are averaged. mask.mean() alone averages the number of Trues to total entries which just returns 0.05 or 0.01 as it should

boolean_mask3 = portfolio_returns < VaR_95
print(f"Expected shortfall 95% - Historical: {portfolio_returns[boolean_mask3].mean():.2%}")

boolean_mask4 = portfolio_returns < VaR_99
print(f"Expected shortfall 99% - Historical: {portfolio_returns[boolean_mask4].mean():.2%}")