---
layout: single
title: "Quantitative Risk Management in Python"
excerpt: "A work in progress about quantitative risk management using pandas and python."
type: post
author_profile: false
header:
    overlay_color: "#333"
classes: wide
published: false
---


# Quantitative Risk Management in Python


```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# portfolio data
portfolio = pd.read_csv('./portfolio.csv', parse_dates=['date'])
portfolio.set_index('date', inplace=True)

# mortgage delinquency data
mort_del = pd.read_csv('./mortgage_delinquency_rates.csv', parse_dates=['Date'])
mort_del.set_index('Date', inplace=True)

# port_q_data
# importing data without headers
port_q_mean = pd.read_csv('./port_q_mean.csv', header=None)
port_q_mean = pd.DataFrame(port_q_mean.values, columns = ["Date", ''])
port_q_mean.set_index('Date', inplace=True)
port_q_mean = port_q_mean.T.iloc[0].astype(float) # converting df to Series

portfolio.head() # the older should be first
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>AAPL</th>
      <th>AMZN</th>
      <th>FB</th>
      <th>GOOG</th>
      <th>NFLX</th>
    </tr>
    <tr>
      <th>date</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2015-01-02</th>
      <td>101.1385</td>
      <td>308.52</td>
      <td>78.450</td>
      <td>524.81</td>
      <td>49.8485</td>
    </tr>
    <tr>
      <th>2015-01-05</th>
      <td>98.2893</td>
      <td>302.19</td>
      <td>77.190</td>
      <td>513.87</td>
      <td>47.3114</td>
    </tr>
    <tr>
      <th>2015-01-06</th>
      <td>98.2985</td>
      <td>295.29</td>
      <td>76.150</td>
      <td>501.96</td>
      <td>46.5014</td>
    </tr>
    <tr>
      <th>2015-01-07</th>
      <td>99.6769</td>
      <td>298.42</td>
      <td>76.150</td>
      <td>501.10</td>
      <td>46.7428</td>
    </tr>
    <tr>
      <th>2015-01-08</th>
      <td>103.5067</td>
      <td>300.46</td>
      <td>78.175</td>
      <td>502.68</td>
      <td>47.7792</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Crisis prices

crisis_prices = pd.read_csv('./2008_crisis_prices.csv')
crisis_prices.set_index('Date', inplace=True)
crisis_prices.index = pd.to_datetime(crisis_prices.index, format='%Y/%m/%d')

crisis_prices.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Citibank</th>
      <th>Morgan Stanley</th>
      <th>Goldman Sachs</th>
      <th>J.P. Morgan</th>
    </tr>
    <tr>
      <th>Date</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2004-12-31</th>
      <td>481.799988</td>
      <td>55.520000</td>
      <td>104.040001</td>
      <td>39.009998</td>
    </tr>
    <tr>
      <th>2005-01-03</th>
      <td>482.700012</td>
      <td>55.900002</td>
      <td>104.949997</td>
      <td>39.150002</td>
    </tr>
    <tr>
      <th>2005-01-04</th>
      <td>478.600006</td>
      <td>55.299999</td>
      <td>104.269997</td>
      <td>38.410000</td>
    </tr>
    <tr>
      <th>2005-01-05</th>
      <td>484.600006</td>
      <td>54.980000</td>
      <td>103.800003</td>
      <td>38.490002</td>
    </tr>
    <tr>
      <th>2005-01-06</th>
      <td>489.299988</td>
      <td>56.279999</td>
      <td>105.230003</td>
      <td>38.709999</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Crisis returns data 
crisis_returns1 = pd.read_csv('./2008_crisis_returns_1.csv')
crisis_returns1.set_index('Date', inplace=True)
crisis_returns1.index = pd.to_datetime(crisis_returns1.index, format='%Y/%m/%d')

crisis_returns2 = pd.read_csv('./2008_crisis_returns_2.csv')
crisis_returns2.set_index('Date', inplace=True)
crisis_returns2.index = pd.to_datetime(crisis_returns2.index, format='%Y/%m/%d')

crisis_returns = pd.concat([crisis_returns1, crisis_returns2]) # concatenate datasets 
crisis_returns.tail()
portfolio = crisis_prices
```


```python

```

### Portfolio returns during the crisis
The first step in quantifying the effects of uncertainty on a financial portfolio is to examine the portfolio's return. You'll consider a portfolio of four investment bank stocks, which were both instigators and victims of the global financial crisis.

The banks are Citibank, Goldman Sachs, J.P. Morgan, and Morgan Stanley. Closing stock prices for the period 2005 - 2010 are in the available portfolio DataFrame. You'll use this to examine the dramatic price changes during the depths of the crisis, 2008 - 2009. You'll also see how volatile the resulting portfolio_returns were, assuming an equal-weighted portfolio with weights stored in the weights list.

In this and in all future exercises, numpy, pandas and matplotlib.pyplot are available as np, pd, and plt respectively.


```python
# Select portfolio asset prices for the middle of the crisis, 2008-2009
asset_prices = portfolio.loc['2008-01-01':'2009-12-31']

# Plot portfolio's asset prices during this time
asset_prices.plot().set_ylabel("Closing Prices, USD")
plt.show()
```


    
![png](Quantitative%20Risk%20Management%20in%20Python_files/Quantitative%20Risk%20Management%20in%20Python_6_0.png)
    


### Asset covariance and portfolio volatility
Now that you've examined the return of the portfolio of investment banks, it's time to assess the riskiness of the portfolio using the covariance matrix to determine the portfolio's volatility.

First you'll compute the covariance between the asset_returns and identify which of the banks had the highest volatility during the 2008-2009 crisis period.

Then, given the weights of an equal-weighted portfolio, you'll find the portfolio's annualized volatility for that period using portfolio_returns.

Finally, you'll use a 30-day window to create a time series of the volatility, and visualize this with a plot.


```python
asset_returns = portfolio.pct_change()
# Generate the covariance matrix from portfolio asset's returns
covariance = asset_returns.cov()

# Annualize the covariance using 252 trading days per year
covariance = covariance * 252

# Display the covariance matrix
print(covariance)
```

                    Citibank  Morgan Stanley  Goldman Sachs  J.P. Morgan
    Citibank        0.536214        0.305045       0.217993     0.269784
    Morgan Stanley  0.305045        0.491993       0.258625     0.218310
    Goldman Sachs   0.217993        0.258625       0.217686     0.170937
    J.P. Morgan     0.269784        0.218310       0.170937     0.264315


### Frequency resampling primer
Risk factor models often rely upon data that is of different frequencies. A typical example is when using quarterly macroeconomic data, such as prices, unemployment rates, etc., with financial data, which is often daily (or even intra-daily). To use both data sources in the same model, higher frequency data needs to be resampled to match the lower frequency data.

The DataFrame and Series Pandas objects have a built-in .resample() method that specifies the lower frequency. This method is chained with a method to create the lower-frequency statistic, such as .mean() for the average of the data within the new frequency period, or .min() for the minimum of the data.

In this exercise you'll practice converting daily returns data to weekly and quarterly frequency.


```python
portfolio_returns = pd.read_csv('./portfolio_returns.csv', header=0)
portfolio_returns = pd.DataFrame(portfolio_returns.values, columns = ["Date", ''])
portfolio_returns.set_index('Date', inplace=True)
portfolio_returns.index = pd.to_datetime(portfolio_returns.index)
portfolio_returns = portfolio_returns.T.iloc[0].astype(float) # Convert into series
portfolio_returns = asset_returns
# r_cov = 

# portfolio_returns
returns_q = portfolio_returns.resample('Q').mean()

# # Examine the beginning of the quarterly series
print(returns_q.head())

# # Now convert daily returns to weekly minimum returns
returns_w = portfolio_returns.resample('W').mean()

# # Examine the beginning of the weekly series
print(returns_w.head())
```

                Citibank  Morgan Stanley  Goldman Sachs  J.P. Morgan
    Date                                                            
    2004-12-31       NaN             NaN            NaN          NaN
    2005-03-31 -0.001105        0.000613       0.000955    -0.001930
    2005-06-30  0.000470       -0.001214      -0.001085     0.000366
    2005-09-30 -0.000214        0.000475       0.002796    -0.000595
    2005-12-31  0.001043        0.000863       0.000862     0.002526
                Citibank  Morgan Stanley  Goldman Sachs  J.P. Morgan
    Date                                                            
    2005-01-02       NaN             NaN            NaN          NaN
    2005-01-09  0.001977        0.002012       0.001452    -0.003104
    2005-01-16 -0.004727        0.000060      -0.001042    -0.003082
    2005-01-23  0.002231       -0.007125      -0.002122    -0.006327
    2005-01-30  0.001880       -0.000374       0.005378     0.000818



```python

```

### Visualizing risk factor correlation
Investment banks heavily invested in mortgage-backed securities (MBS) before and during the financial crisis. This makes MBS a likely risk factor for the investment bank portfolio. You'll assess this using scatterplots between portfolio returns and an MBS risk measure, the 90-day mortgage delinquency rate mort_del.

mort_del is only available as quarterly data. So portfolio_returns first needs to be transformed from daily to quarterly frequency using the DataFrame .resample() method.

Your workspace contains both portfolio_returns for an equal-weighted portfolio and the delinquency rate mort_del variable. For the scatterplots, plot_average and plot_min are plot axes in your workspace--you'll add your scatterplots to them using the .scatter() method.


```python
# Transform the daily portfolio_returns into quarterly average returns
portfolio_q_average = portfolio_returns.resample('Q').mean().dropna()

# Create a scatterplot between delinquency and quarterly average returns
# plt.scatter(mort_del, portfolio_q_average)

# Transform daily portfolio_returns returns into quarterly minimum returns
portfolio_q_min = portfolio_returns.resample('Q').min().dropna()
portfolio_q_vol = portfolio_returns.resample('Q').std().dropna()

# Create a scatterplot between delinquency and quarterly minimum returns
# plt.scatter(mort_del, portfolio_q_min)
# plt.show()
print(portfolio_q_average.shape)

```

    (24, 4)


### Least-squares factor model
As you've seen, there is a negative correlation between minimum quarterly returns and mortgage delinquency rates from 2005 - 2010. This can be made more precise with an OLS regression factor model.

You'll compare three factor models with three different quarterly dependent variables: average returns, minimum returns, and average volatility. The independent variable is the mortgage delinquency rate. In the regression summary, examine the coefficients' t-statistic for statistical significance, as well as the overall R-squared for goodness of fit.

The statsmodels.api library is available as sm.


```python
mort_del = pd.read_csv('./mortgage_delinquency_rates.csv', parse_dates=['Date'])
mort_del.set_index('Date', inplace=True)

# port_q_mean
# mort_del
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Mortgage Delinquency Rate</th>
    </tr>
    <tr>
      <th>Date</th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2005-03-31</th>
      <td>0.0155</td>
    </tr>
    <tr>
      <th>2005-06-30</th>
      <td>0.0159</td>
    </tr>
    <tr>
      <th>2005-09-30</th>
      <td>0.0163</td>
    </tr>
    <tr>
      <th>2005-12-31</th>
      <td>0.0161</td>
    </tr>
    <tr>
      <th>2006-03-31</th>
      <td>0.0162</td>
    </tr>
    <tr>
      <th>2006-06-30</th>
      <td>0.0174</td>
    </tr>
    <tr>
      <th>2006-09-30</th>
      <td>0.0192</td>
    </tr>
    <tr>
      <th>2006-12-31</th>
      <td>0.0208</td>
    </tr>
    <tr>
      <th>2007-03-31</th>
      <td>0.0231</td>
    </tr>
    <tr>
      <th>2007-06-30</th>
      <td>0.0271</td>
    </tr>
    <tr>
      <th>2007-09-30</th>
      <td>0.0309</td>
    </tr>
    <tr>
      <th>2007-12-31</th>
      <td>0.0367</td>
    </tr>
    <tr>
      <th>2008-03-31</th>
      <td>0.0438</td>
    </tr>
    <tr>
      <th>2008-06-30</th>
      <td>0.0530</td>
    </tr>
    <tr>
      <th>2008-09-30</th>
      <td>0.0659</td>
    </tr>
    <tr>
      <th>2008-12-31</th>
      <td>0.0796</td>
    </tr>
    <tr>
      <th>2009-03-31</th>
      <td>0.0858</td>
    </tr>
    <tr>
      <th>2009-06-30</th>
      <td>0.0953</td>
    </tr>
    <tr>
      <th>2009-09-30</th>
      <td>0.1034</td>
    </tr>
    <tr>
      <th>2009-12-31</th>
      <td>0.1154</td>
    </tr>
    <tr>
      <th>2010-03-31</th>
      <td>0.1106</td>
    </tr>
    <tr>
      <th>2010-06-30</th>
      <td>0.1059</td>
    </tr>
    <tr>
      <th>2010-09-30</th>
      <td>0.1036</td>
    </tr>
    <tr>
      <th>2010-12-31</th>
      <td>0.1035</td>
    </tr>
  </tbody>
</table>
</div>




```python
import statsmodels.api as sm
# Add a constant to the regression
mort_del = sm.add_constant(mort_del)

# # Create the regression factor model and fit it to the data
results = sm.OLS(port_q_mean, mort_del).fit()

# # Print a summary of the results
print(results.summary())
```

                                OLS Regression Results                            
    ==============================================================================
    Dep. Variable:                      y   R-squared:                       0.021
    Model:                            OLS   Adj. R-squared:                 -0.023
    Method:                 Least Squares   F-statistic:                    0.4801
    Date:                Sat, 14 Nov 2020   Prob (F-statistic):              0.496
    Time:                        17:52:01   Log-Likelihood:                 113.89
    No. Observations:                  24   AIC:                            -223.8
    Df Residuals:                      22   BIC:                            -221.4
    Df Model:                           1                                         
    Covariance Type:            nonrobust                                         
    =============================================================================================
                                    coef    std err          t      P>|t|      [0.025      0.975]
    ---------------------------------------------------------------------------------------------
    const                        -0.0001      0.001     -0.175      0.862      -0.002       0.002
    Mortgage Delinquency Rate     0.0083      0.012      0.693      0.496      -0.016       0.033
    ==============================================================================
    Omnibus:                        0.081   Durbin-Watson:                   1.604
    Prob(Omnibus):                  0.960   Jarque-Bera (JB):                0.293
    Skew:                          -0.071   Prob(JB):                        0.864
    Kurtosis:                       2.477   Cond. No.                         26.7
    ==============================================================================
    
    Warnings:
    [1] Standard Errors assume that the covariance matrix of the errors is correctly specified.


### Practice with PyPortfolioOpt: returns
Modern Portfolio Theory is the cornerstone of portfolio risk management, because the efficient frontier is a standard method of assessing both investor risk appetite and market risk-return tradeoffs. In this exercise you'll develop powerful tools to explore a portfolio's efficient frontier, using the PyPortfolioOpt pypfopt Python library.

To compute the efficient frontier, both expected returns and the covariance matrix of the portfolio are required.

After some practice loading the investment bank price data, you'll use pypfopt.expected_returns's mean_historical_return method to compute and visualize the annualized average returns of each bank from daily asset prices. The following exercise will then cover the covariance matrix.


```python
# Load the investment portfolio price data into the price variable.
prices = pd.read_csv("portfolio.csv")

# Convert the 'Date' column to a datetime index
prices['Date'] = pd.to_datetime(prices['date'], format='%Y/%m/%d')
prices = prices.drop('date', 1) # drop old date column because is str type
prices.set_index(['Date'], inplace = True)
prices.shape
```




    (1067, 5)




```python
# Import the mean_historical_return method
from pypfopt.expected_returns import mean_historical_return

# Compute the annualized average historical return
mean_returns = mean_historical_return(prices, frequency = 252)

# Plot the annualized average historical return
plt.plot(mean_returns, linestyle = 'None', marker = 'o')
plt.show()
```


    
![png](Quantitative%20Risk%20Management%20in%20Python_files/Quantitative%20Risk%20Management%20in%20Python_19_0.png)
    


### Practice with PyPortfolioOpt: covariance
Portfolio optimization relies upon an unbiased and efficient estimate of asset covariance. Although sample covariance is unbiased, it is not efficient--extreme events tend to be overweighted.

One approach to alleviate this is through "covariance shrinkage", where large errors are reduced ('shrunk') to improve efficiency. In this exercise, you'll use pypfopt.risk_models's CovarianceShrinkage object to transform sample covariance into an efficient estimate. The textbook error shrinkage method, .ledoit_wolf(), is a method of this object.

Asset prices are available in your workspace. Note that although the CovarianceShrinkage object takes prices as input, it actually calculates the covariance matrix of asset returns, not prices.


```python
# Import the CovarianceShrinkage object
from pypfopt.risk_models import CovarianceShrinkage

# Create the CovarianceShrinkage instance variable
cs = CovarianceShrinkage(prices)
```


```python
# Compute the sample covariance matrix of anual returns
sample_cov = prices.pct_change().cov() * 252

# Compute the efficient covariance matrix of returns
e_cov = cs.ledoit_wolf()

# Display both the sample covariance_matrix and the efficient e_cov estimate
print("Sample Covariance Matrix\n", sample_cov, "\n")
print("Efficient Covariance Matrix\n", e_cov, "\n")

```

    Sample Covariance Matrix
               AAPL      AMZN        FB      GOOG      NFLX
    AAPL  0.063118  0.037599  0.032926  0.031483  0.039957
    AMZN  0.037599  0.093749  0.049486  0.048395  0.063560
    FB    0.032926  0.049486  0.082483  0.041922  0.049808
    GOOG  0.031483  0.048395  0.041922  0.057460  0.049559
    NFLX  0.039957  0.063560  0.049808  0.049559  0.185543 
    
    Efficient Covariance Matrix
               AAPL      AMZN        FB      GOOG      NFLX
    AAPL  0.063731  0.036806  0.032231  0.030819  0.039114
    AMZN  0.036806  0.093716  0.048442  0.047374  0.062219
    FB    0.032231  0.048442  0.082688  0.041038  0.048757
    GOOG  0.030819  0.047374  0.041038  0.058192  0.048513
    NFLX  0.039114  0.062219  0.048757  0.048513  0.183573 
    



```python
type(sample_cov)
```




    pandas.core.frame.DataFrame



Excellent. Although the differences between the sample covariance and the efficient covariance (found by shrinking errors) may seem small, they have a huge impact on estimation of the optimal portfolio weights and the generation of the efficient frontier. Practitioners generally use some form of efficient covariance for Modern Portfolio Theory.

### Breaking down the financial crisis
In the video you saw the efficient frontier for the portfolio of investment banks over the entire period 2005 - 2010, which includes time before, during and after the global financial crisis.

Here you'll break down this period into three sub-periods, or epochs: 2005-2006 (before), 2007-2008 (during) and 2009-2010 (after). For each period you'll compute the efficient covariance matrix, and compare them to each other.

The portfolio's prices for 2005 - 2010 are available in your workspace, as is the CovarianceShrinkage object from PyPortfolioOpt.


```python
prices.head()
prices.tail()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>AAPL</th>
      <th>AMZN</th>
      <th>FB</th>
      <th>GOOG</th>
      <th>NFLX</th>
    </tr>
    <tr>
      <th>Date</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2019-03-25</th>
      <td>188.0160</td>
      <td>1774.26</td>
      <td>166.29</td>
      <td>1193.00</td>
      <td>366.23</td>
    </tr>
    <tr>
      <th>2019-03-26</th>
      <td>186.0735</td>
      <td>1783.76</td>
      <td>167.68</td>
      <td>1184.62</td>
      <td>359.97</td>
    </tr>
    <tr>
      <th>2019-03-27</th>
      <td>187.7470</td>
      <td>1765.70</td>
      <td>165.87</td>
      <td>1173.02</td>
      <td>353.37</td>
    </tr>
    <tr>
      <th>2019-03-28</th>
      <td>187.9961</td>
      <td>1773.42</td>
      <td>165.55</td>
      <td>1168.49</td>
      <td>354.61</td>
    </tr>
    <tr>
      <th>2019-03-29</th>
      <td>189.2214</td>
      <td>1780.75</td>
      <td>166.69</td>
      <td>1173.31</td>
      <td>356.56</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Create a dictionary of time periods (or 'epochs')
epochs = { 'before' : {'start': '1-1-2015', 'end': '31-12-2016'},
           'during' : {'start': '1-1-2017', 'end': '31-12-2018'},
           'after'  : {'start': '1-1-2019', 'end': '31-12-2020'} # its ok to pass the final df date
         }

# Compute the efficient covariance for each epoch
e_cov = {}
for x in epochs.keys():
    sub_price = prices.loc[epochs[x]['start']:epochs[x]['end']]
    e_cov[x] = CovarianceShrinkage(sub_price).ledoit_wolf()

# Display the efficient covariance matrices for all epochs
from pprint import pprint as pp
# print("Efficient Covariance Matrices\n", pp(e_cov))
e_cov
```




    {'before':           AAPL      AMZN        FB      GOOG      NFLX
     AAPL  0.065136  0.026898  0.028855  0.024455  0.031196
     AMZN  0.026898  0.100962  0.043899  0.044377  0.050276
     FB    0.028855  0.043899  0.074869  0.037591  0.041845
     GOOG  0.024455  0.044377  0.037591  0.065811  0.042719
     NFLX  0.031196  0.050276  0.041845  0.042719  0.221128,
     'during':           AAPL      AMZN        FB      GOOG      NFLX
     AAPL  0.058822  0.042577  0.031933  0.033216  0.043893
     AMZN  0.042577  0.086963  0.049817  0.047330  0.070400
     FB    0.031933  0.049817  0.086987  0.041333  0.053155
     GOOG  0.033216  0.047330  0.041333  0.052416  0.051009
     NFLX  0.043893  0.070400  0.053155  0.051009  0.144331,
     'after':           AAPL      AMZN        FB      GOOG      NFLX
     AAPL  0.107229  0.049651  0.041517  0.044252  0.042236
     AMZN  0.049651  0.093748  0.044872  0.045403  0.060373
     FB    0.041517  0.044872  0.114216  0.041364  0.041329
     GOOG  0.044252  0.045403  0.041364  0.066046  0.047108
     NFLX  0.042236  0.060373  0.041329  0.047108  0.147604}



### The efficient frontier and the financial crisis
Previously you examined the covariance matrix of the investment bank portfolio before, during and after the financial crisis. Now you will visualize the changes that took place in the efficient frontier, showing how the crisis created a much higher baseline risk for any given return.

Using the PyPortfolioOpt pypfopt library's Critical Line Algorithm (CLA) object, you will derive and visualize the efficient frontier during the crisis period, and add it to a scatterplot already displaying the efficient frontiers before and after the crisis.

Expected returns returns_during and the efficient covariance matrix ecov_during are available, as is the CLA object from pypfopt. (Remember that DataCamp plots can be expanded to their own window, which can increase readability.)


```python
returns_during = prices.loc['1-1-2017':'31-12-2018'].mean()
ecov_during =  e_cov['during']
(returns_during.shape, ecov_during.shape) #:)
```




    ((5,), (5, 5))




```python
from pypfopt import CLA
# Initialize the Crtical Line Algorithm object
efficient_portfolio_during = CLA(returns_during, ecov_during)

# Find the minimum volatility portfolio weights and display them
print(efficient_portfolio_during.min_volatility())
# Find the max sharpe ratio weights and display them
print(efficient_portfolio_during.max_sharpe())

# Compute the efficient frontier
(ret, vol, weights) = efficient_portfolio_during.efficient_frontier()

# Add the frontier to the plot showing the 'before' and 'after' frontiers
plt.scatter(vol, ret, s = 4, c = 'g', marker = '.', label = 'During')
plt.legend()
plt.show()
```

    OrderedDict([('AAPL', 0.4009328427967109), ('AMZN', 0.0), ('FB', 0.12608593792383824), ('GOOG', 0.4729812192794509), ('NFLX', 0.0)])
    OrderedDict([('AAPL', 4.1194489698176803e-17), ('AMZN', 0.43100821377007054), ('FB', 0.0), ('GOOG', 0.5689917862299295), ('NFLX', 0.0)])



    
![png](Quantitative%20Risk%20Management%20in%20Python_files/Quantitative%20Risk%20Management%20in%20Python_30_1.png)
    


### VaR for the Normal distribution
To get accustomed to the Value at Risk (VaR) measure, it helps to apply it to a known distribution. The Normal (or Gaussian) distribution is especially appealing as it 1) has an analytically simple form, and 2) represents a wide variety of empirical phenomena. For this exercise you'll assume that the loss of a portfolio is normally distributed, i.e., the higher the value drawn from the distribution, the higher the loss.

You'll learn how to apply both scipy.stats.norm's ppf() (percent point function) and numpy's quantile() function to find the VaR at the 95% and 99% confidence levels, respectively, for a standard Normal distribution. You'll also visualize the VaR as a threshold on a Normal distribution plot.


```python
from scipy.stats import norm

# Create the VaR measure at the 95% confidence level using norm.ppf()
VaR_95 = norm.ppf(0.95)

# Create the VaR meaasure at the 5% significance level using numpy.quantile()
draws = norm.rvs(size = 100000) # 100000 observations normally distributed
VaR_99 = np.quantile(draws, 0.99)

# Compare the 95% and 99% VaR
print("95% VaR: ", VaR_95, "; 99% VaR: ", VaR_99)

# Plot the normal distribution histogram and 95% VaR measure
plt.hist(draws, bins = 100)
plt.axvline(x = VaR_95, c='r', label = "VaR at 95% Confidence Level")
plt.legend(); plt.show()
```

    95% VaR:  1.6448536269514722 ; 99% VaR:  2.3301705114514633



    
![png](Quantitative%20Risk%20Management%20in%20Python_files/Quantitative%20Risk%20Management%20in%20Python_32_1.png)
    


### Comparing CVaR and VaR
The conditional value at risk (CVaR), or expected shortfall (ES), asks what the average loss will be, conditional upon losses exceeding some threshold at a certain confidence level. It uses VaR as a point of departure, but contains more information because it takes into consideration the tail of the loss distribution.

You'll first compute the 95% VaR for a Normal distribution of portfolio losses, with the same mean and standard deviation as the 2005-2010 investment bank portfolio_losses. You'll then use the VaR to compute the 95% CVaR, and plot both against the Normal distribution.

The portfolio_losses are available in your workspace, as well as the norm Normal distribution from scipy.stats.


```python
portfolio_losses = pd.read_csv('./portfolio_losses.csv', header=None)
portfolio_losses = pd.DataFrame(portfolio_losses.values, columns = ["Date", ''])
portfolio_losses.set_index('Date', inplace=True)
portfolio_losses.index = pd.to_datetime(portfolio_losses.index, format='%Y/%m/%d') # have to be converted to be shown in the plot
portfolio_losses = portfolio_losses.T.iloc[0].astype(float) # Convert in Series
portfolio_losses.head()
```




    Date
    2005-01-03   -0.005262
    2005-01-04    0.011152
    2005-01-05   -0.001081
    2005-01-06   -0.013209
    2005-01-07    0.005479
    Name: , dtype: float64




```python
# Compute the mean and variance of the portfolio returns
pm = portfolio_losses.mean()
ps = portfolio_losses.std()

# Compute the 95% VaR using the .ppf()
VaR_95 = norm.ppf(0.95, loc = pm, scale = ps)
# Compute the expected tail loss and the CVaR in the worst 5% of cases
tail_loss = norm.expect(lambda x: x, loc = pm, scale = ps, lb = VaR_95)
CVaR_95 = (1 / (1 - 0.95)) * tail_loss

# Plot the normal distribution histogram and add lines for the VaR and CVaR
plt.hist(norm.rvs(size = 100000, loc = pm, scale = ps), bins = 100)
plt.axvline(x = VaR_95, c='r', label = "VaR, 95% confidence level")
plt.axvline(x = CVaR_95, c='g', label = "CVaR, worst 5% of outcomes")
plt.legend(); plt.show()
```


    
![png](Quantitative%20Risk%20Management%20in%20Python_files/Quantitative%20Risk%20Management%20in%20Python_35_0.png)
    



```python
CVaR_95
```




    0.06776383821709393




```python
port_q_mean.shape
```




    (24,)



### VaR and risk exposure
Previously you computed the VaR and CVaR when losses were Normally distributed. Here you'll find the VaR using another common loss distribution, the Student's t-distribution (or T) contained in scipy.stats.

You'll compute an array of 99% VaR measures from the T distribution (with 30 - 1 = 29 degrees of freedom), using 30-day rolling windows from investment bank portfolio losses.

First you'll find the mean and standard deviation of each window, creating a list of rolling_parameters. You'll use these to compute the 99% VaR array of measures.

Then you'll use this array to plot the risk exposure for a portfolio initially worth $100,000. Recall that risk exposure is the probability of loss (this is 1%) multiplied by the loss amount (this is the loss given by the 99% VaR).


```python
# Import the Student's t-distribution
from scipy.stats import t

# Create rolling window parameter list
mu = portfolio_losses.rolling(30).mean()
sigma = portfolio_losses.rolling(30).std()
# 30 - 1 Degrees of freedom 
rolling_parameters = [(29, mu[i], s) for i,s in enumerate(sigma)]

# Compute the 99% VaR array using the rolling window parameters
# params = [('degree of freedom', meand, sd)]
VaR_99 = np.array( [ t.ppf(0.99, *params) 
                    for params in rolling_parameters ] )

# Plot the minimum risk exposure over the 2005-2010 time period
plt.plot(portfolio_losses.index, 0.01 * VaR_99 * 100000)
plt.show()
```


    
![png](Quantitative%20Risk%20Management%20in%20Python_files/Quantitative%20Risk%20Management%20in%20Python_39_0.png)
    


### CVaR and risk exposure
Recall that CVaR is the expected value of loss given a minimum loss threshold. So CVaR is already in the form of a risk exposure--it is the sum (or integral) of the probability of loss in the distribution tail multiplied, by the loss amount.

To derive the 99% CVaR you'll first fit a T distribution to available crisis_losses portfolio data from 2008 - 2009, using the t.fit() method. This returns the T distribution parameters p used to find the VaR with the .ppf() method.

Next you'll compute the 99% VaR, since it's used to find the CVaR.

Finally you'll compute the 99% CVaR measure using the t.expect() method, which is the same method you used to compute CVaR for the Normal distribution in an earlier exercise.

The t distribution from scipy.stats is also available.


```python
def from_csv_to_series(path):
    df = pd.read_csv(path, header=None)
    df = pd.DataFrame(df.values, columns = ["Date", ''])
    df.set_index('Date', inplace=True)
    df.index = pd.to_datetime(df.index, format='%Y/%m/%d') # have to be converted to be shown in the plot
    series = df.T.iloc[0].astype(float) # Convert in Series
    print(series.head())
    return series 

crisis_losses = from_csv_to_series('./crisis_losses.csv')
```

    Date
    2008-01-02    0.031721
    2008-01-03    0.005006
    2008-01-04    0.025675
    2008-01-07    0.008841
    2008-01-08    0.036424
    Name: , dtype: float64



```python
# Fit the Student's t distribution to crisis losses
p = t.fit(crisis_losses)

# Compute the VaR_99 for the fitted distribution
VaR_99 = t.ppf(0.99, *p)

# Use the fitted parameters and VaR_99 to compute CVaR_99
tail_loss = t.expect(lambda y: y, args = (p[0],), loc = p[1], scale = p[2], lb = VaR_99 )
CVaR_99 = (1 / (1 - 0.99)) * tail_loss
print(CVaR_99)
```

    0.3380538488604617


### VaR from a fitted distribution
Minimizing CVaR requires calculating the VaR at a confidence level, say 95%. Previously you derived the VaR as a quantile from a Normal (or Gaussian) distribution, but minimizing the CVaR more generally requires computing the quantile from a distribution that best fits the data.

In this exercise a fitted loss distribution is provided, which fits losses from an equal-weighted investment bank portfolio from 2005-2010. You'll first plot this distribution using its .evaluate() method (fitted distributions will be covered in more detail in Chapter 4).

Next you'll use the .resample() method of the fitted object to draw a random sample of 100,000 observations from the fitted distribution.

Finally, using np.quantile() on the random sample will then compute the 95% VaR.


```python
from scipy.stats import gaussian_kde

fitted = gaussian_kde(portfolio_losses)
# Visualize the fitted distribution with a plot
x = np.linspace(-0.25,0.25,1000)
plt.plot(x,fitted.evaluate(x))
plt.show()

# Create a random sample of 100,000 observations from the fitted distribution
sample = fitted.resample(100000)

# Compute and display the 95% VaR from the random sample
VaR_95 = np.quantile(sample, 0.95)
print(VaR_95)
```


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-19-58a414c3e93f> in <module>
          1 from scipy.stats import gaussian_kde
          2 
    ----> 3 fitted = gaussian_kde(portfolio_losses)
          4 # Visualize the fitted distribution with a plot
          5 x = np.linspace(-0.25,0.30,1000)


    NameError: name 'portfolio_losses' is not defined


### Minimizing CVaR
This exercise will give you practice with PyPortfolioOpt's tools for CVaR minimization as a risk management objective.

You'll load the pypfopt.efficient_frontier module and retrieve the EfficientFrontier class, creating an instance of the class using the investment bank assets over the 2005 - 2010 period. You'll also load the negative_cvar() function from the pypfopt.objective_functions module.

You'll then use the EfficientFrontier.custom_objective() method with negative_cvar() to find the optimal portfolio weights that minimize the CVaR.

Portfolio asset returns are in the returns vector, and the efficient covariance matrix is in e_cov.


```python
def negative_cvar(weights, returns, s=10000, beta=0.95, random_state=None):
    """
    Calculate the negative CVaR. Though we want the "min CVaR portfolio", we
    actually need to maximise the expected return of the worst q% cases, thus
    we need this value to be negative.

    :param weights: asset weights of the portfolio
    :type weights: np.ndarray
    :param returns: asset returns
    :type returns: pd.DataFrame or np.ndarray
    :param s: number of bootstrap draws, defaults to 10000
    :type s: int, optional
    :param beta: "significance level" (i. 1 - q), defaults to 0.95
    :type beta: float, optional
    :param random_state: seed for random sampling, defaults to None
    :type random_state: int, optional
    :return: negative CVaR
    :rtype: float
    """
    np.random.seed(seed=random_state)
    # Calcualte the returns given the weights
    portfolio_returns = (weights * returns).sum(axis=1)
    # Sample from the historical distribution
    dist = scipy.stats.gaussian_kde(portfolio_returns)
    sample = dist.resample(s)
    # Calculate the value at risk
    var = portfolio_returns.quantile(1 - beta)
    # Mean of all losses worse than the value at risk
    return -sample[sample < var].mean()

```


```python
# The following code is not gonna work negative_cvar was aailable till version 0.5.3
import pypfopt
pypfopt.__version__
```




    '1.2.6'




```python

# # Import the EfficientFrontier class
# from pypfopt.efficient_frontier import EfficientFrontier
# # Import the negative_cvar objective function
# from pypfopt.objective_functions import negative_cvar

# # Create the efficient frontier instance
# ef = EfficientFrontier(None, covariance)

# # Find the cVar-minimizing portfolio weights at the default 95% confidence level
# # v = negative_cvar(portfolio_returns)
# # optimal_weights = ef.add_objective(v)

# # # Display the optimal weights
# # print(optimal_weights)
```

### CVaR risk management and the crisis
In this exercise you'll derive the 95% CVaR-minimizing portfolio for 2005-2006, 2007-2008, and 2009-2010. These are the periods (or 'epochs') before, during and after the crisis.

To help with this, asset returns_dict and the efficient covariance matrices e_cov_dict are available as Python dictionaries, each with epoch keys 'before', 'during' and 'after'.

Minimum volatility portfolios are also saved in a dictionary called min_vol_dict, with the same keys--be sure to check them out in the console.

After deriving each epoch's CVaR-minimizing portfolios, you'll compare them to the min_vol_dict portfolios. This will show how active risk management against conditional losses changes the portfolio weights.

Both negative_cvar and EfficientFrontier are available.


```python
# from pypfopt.efficient_frontier import EfficientFrontier

# # Initialize the efficient portfolio dictionary
# ef_dict = {}

# # For each epoch, assign an efficient frontier instance to ef
# for x in ['before', 'during', 'after']: 
#     ef_dict[x] = EfficientFrontier(None, e_cov[x])

# # Initialize the dictionary of optimal weights
# optimal_weights_dict = {}

# # Find and display the CVaR-minimizing portfolio weights at the default 95% confidence level
# for x in ['before', 'during', 'after']:
#     optimal_weights_dict[x] = ef_dict[x].custom_objective(negative_cvar, returns_dict[x])

# # Compare the CVaR-minimizing weights to the minimum volatility weights for the 'before' epoch
# print("CVaR:\n", pd.DataFrame.from_dict(optimal_weights_dict['before']), "\n")
# print("Min Vol:\n", pd.DataFrame.from_dict(min_vol_dict['before']), "\n")


```

### Black-Scholes options pricing
Options are the world's most widely used derivative to help manage asset price risk. In this exercise you'll price a European call option on IBM's stock using the Black-Scholes option pricing formula. IBM_returns data has been loaded in your workspace.

First you'll compute the volatility sigma of IBM_returns, as the annualized standard deviation.

Next you'll use the function black_scholes(), created for this and the following exercises, to price options for two different volatility levels: sigma and two times sigma.

The strike price K, i.e. the price an investor has the right (but not the obligation) to buy IBM, is 80. The risk-free interest rate r is 2% and the market spot price S is 90.

You can find the source code of the black_scholes() function here.


```python
IBM_returns = pd.read_csv('./ibm_returns.csv', header=None)
# ibm_returns.reset_index()
IBM_returns = IBM_returns.T.iloc[1].astype(float)
IBM_returns
```




    0       0.036004
    1      -0.000521
    2      -0.009355
    3       0.015222
    4      -0.009524
              ...   
    1253    0.003856
    1254   -0.001561
    1255    0.001301
    1256    0.003842
    1257   -0.009528
    Name: 1, Length: 1258, dtype: float64




```python
from black_scholes import black_scholes, bs_delta
# Compute the volatility as the annualized standard deviation of IBM returns
sigma = np.sqrt(252) * IBM_returns.std()

# Compute the Black-Scholes option price for this volatility
value_s = black_scholes(S = 90, X = 80, T = 0.5, r = 0.02, 
                        sigma = sigma, option_type = "call")

# # Compute the Black-Scholes option price for twice the volatility
value_2s = black_scholes(S = 90, X = 80, T = 0.5, r = 0.02, 
                sigma = sigma*2, option_type = "call")

# # Display and compare both values
print("Option value for sigma: ", value_s, "\n",
      "Option value for 2 * sigma: ", value_2s)
```


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-24-a2273ca8bd25> in <module>
          1 from black_scholes import black_scholes, bs_delta
          2 # Compute the volatility as the annualized standard deviation of IBM returns
    ----> 3 sigma = np.sqrt(252) * IBM_returns.std()
          4 
          5 # Compute the Black-Scholes option price for this volatility


    NameError: name 'IBM_returns' is not defined


Nice job. As shown, the value of the call option increases with an increase in volatility! This is because an option only needs to be exercised when it is profitable to do so, which means that more volatility increases the chance for profit. In the next exercise, you'll examine how an option's profitability changes instead with the price of the underlying stock over time.

### Options pricing and the underlying asset
Options are essentially bets on the future evolution of the underlying asset's price.

For example, a put option is valuable when the spot (market) price falls below the option's strike price. The option holder may exercise the option to sell the underlying at the strike X, and buy it back at the spot S<X, yielding profit X−S.

In this exercise you'll value and visualize a European put option on IBM stock, again applying the Black-Scholes pricing formula, as the spot S changes.

The strike X = 140, the time to maturity T is 1/2 a year, and the risk-free interest rate is 2%.

The annualized volatility of IBM is available as sigma, and the plotting axis option_axis is available to add your plot.

You can find the source code of the black_scholes() function here.


```python
IBM = pd.read_csv('./ibm_prices.csv', header=0)
IBM = IBM.loc[:, ~IBM.columns.str.contains('^Unnamed')]
# IBM.drop('Unnamed:0', inplace=True )
IBM.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>close</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>129.57</td>
    </tr>
    <tr>
      <th>1</th>
      <td>134.32</td>
    </tr>
    <tr>
      <th>2</th>
      <td>134.25</td>
    </tr>
    <tr>
      <th>3</th>
      <td>133.00</td>
    </tr>
    <tr>
      <th>4</th>
      <td>135.04</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Select the first 100 observations of IBM data
IBM_spot = IBM[:100]

# Initialize the European put option values array
option_values = np.zeros(IBM_spot.size)

# Iterate through IBM's spot price and compute the option values
for i,S in enumerate(IBM_spot.values):
    option_values[i] = black_scholes(S = S, X = 140, T = 0.5, r = 0.02, 
                        sigma = sigma, option_type = "call")

fig, ax1 = plt.subplots()
plt.xlabel('Time')
ax2 = ax1.twinx()
ax1.plot(option_values, color = "red", label = "Put Option")
ax1.legend(loc = "upper left")
ax1.set_ylabel('Put Option')
ax2.plot(IBM_spot, color = "blue", label = "IBM stock")
ax2.legend(loc = "upper right")
ax2.set_ylabel('IBM Stock')
plt.show()
```


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-23-d2f11517f00e> in <module>
          7 # Iterate through IBM's spot price and compute the option values
          8 for i,S in enumerate(IBM_spot.values):
    ----> 9     option_values[i] = black_scholes(S = S, X = 140, T = 0.5, r = 0.02, 
         10                         sigma = sigma, option_type = "call")
         11 


    NameError: name 'black_scholes' is not defined


### Using options for hedging
Suppose that you have an investment portfolio with one asset, IBM. You'll hedge the portfolio's risk using delta hedging with a European put option on IBM.

First, value the European put option using the Black-Scholes option pricing formula, with a strike X of 80 and a time to maturity T of 1/2 a year. The risk-free interest rate is 2% and the spot S is initially 70.

Then create a delta hedge by computing the delta of the option with the bs_delta() function, and use it to hedge against a change in the stock price to 69.5. The result is a delta neutral portfolio of both the option and the stock.

Both of the functions black_scholes() and bs_delta() are available in your workspace.

You can find the source code of the black_scholes() and bs_delta() functions here.


```python
# Compute the annualized standard deviation of `IBM` returns
sigma = np.sqrt(252) * IBM_returns.std()

# Compute the Black-Scholes value at IBM spot price 70
value = black_scholes(S = 70, X = 80, T = 0.5, r = 0.02, 
                      sigma = sigma, option_type = "put")
# Find the delta of the option at IBM spot price 70
delta = bs_delta(S = 70, X = 80, T = 0.5, r = 0.02, 
                 sigma = sigma, option_type = "put")

# Find the option value change when the price of IBM falls to 69.5
value_change = black_scholes(S = 69.5, X = 80, T = 0.5, r = 0.02, 
                             sigma = sigma, option_type = "put") - value

print( (69.5 - 70) + (1/delta) * value_change )
```

    0.004594280510132442


Excellent! The price change in IBM has been offset using the option delta. You've hedged risk the way institutional risk managers do it, which is how pension funds keep their value. Important stuff!

### Parameter estimation: Normal
Parameter estimation is the strongest method of VaR estimation because it assumes that the loss distribution class is known. Parameters are estimated to fit data to this distribution, and statistical inference is then made.

In this exercise, you will estimate the 95% VaR from a Normal distribution fitted to the investment bank data from 2007 - 2009. You'll use scipy.stats's norm distribution, assuming that it's the most appropriate class of distribution.

Is a Normal distribution a good fit? You'll test this with the scipy.stats.anderson Anderson-Darling test. If the test result is statistically different from zero, this indicates the data is not Normally distributed. You'll address this in the next exercise.

Portfolio losses for the 2005 - 2010 period are available.


```python
# Import the Normal distribution and skewness test from scipy.stats
from scipy.stats import norm, anderson

# Fit portfolio losses to the Normal distribution
params = norm.fit(portfolio_losses)

# Compute the 95% VaR from the fitted distribution, using parameter estimates
VaR_95 = norm.ppf(0.95, *params)
print("VaR_95, Normal distribution: ", VaR_95)

# Test the data for Normality
print("Anderson-Darling test result: ", anderson(portfolio_losses))
```

    VaR_95, Normal distribution:  0.05395533010834023
    Anderson-Darling test result:  AndersonResult(statistic=86.43196190834169, critical_values=array([0.574, 0.654, 0.785, 0.916, 1.089]), significance_level=array([15. , 10. ,  5. ,  2.5,  1. ]))


Well done. The Anderson-Darling test value of 30.30 exceeds the 99% critical value of 1.086 by a large margin, indicating that the Normal distribution may be a poor choice to represent portfolio losses.

### Parameter estimation: Skewed Normal
In the previous exercise you found that fitting a Normal distribution to the investment bank portfolio data from 2005 - 2010 resulted in a poor fit according to the Anderson-Darling test.

You will test the data using the skewtest() function from scipy.stats. If the test result is statistically different from zero, then the data support a skewed distribution.

Now you'll parametrically estimate the 95% VaR of a loss distribution fit using scipy.stats's skewnorm skewed Normal distribution. This is a more general distribution than the Normal and allows losses to be non-symmetrically distributed. We might expect losses to be skewed during the crisis, when portfolio losses were more likely than gains.

Portfolio losses for the 2007 - 2009 period are available.


```python
# Import the skew-normal distribution and skewness test from scipy.stats
from scipy.stats import skewnorm, skewtest

# Test the data for skewness
print("Skewtest result: ", skewtest(portfolio_losses))

# Fit the portfolio loss data to the skew-normal distribution
params = skewnorm.fit(portfolio_losses)

# Compute the 95% VaR from the fitted distribution, using parameter estimates
VaR_95 = skewnorm.ppf(0.95, *params)
print("VaR_95 from skew-normal: ", VaR_95)
```

    Skewtest result:  SkewtestResult(statistic=-20.031345424766013, pvalue=2.936172905672016e-89)
    VaR_95 from skew-normal:  0.04998801227255191


### Historical Simulation
Historical simulation of VaR assumes that the distribution of historical losses is the same as the distribution of future losses. We'll test if this is true for our investment bank portfolio by comparing the 95% VaR from 2005 - 2006 to the 95% VaR from 2007 - 2009.

The list asset_returns has been created for you, which contains asset returns for each of the two periods. You'll use this list to create portfolio_returns with the available weights, and use this to derive portfolio losses.

Then you'll use the np.quantile() function to find the 95% VaR for each period. If the loss distributions are the same, then the 95% VaR estimate should be about the same for both periods. Otherwise the distribution might have changed as the global financial crisis took hold.


```python
asset_returns = [
    portfolio_returns.loc['2005-01-03':'2006-12-29'],
    portfolio_returns.loc['2007-01-03':'2009-12-31']
]

portfolio_returns
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Citibank</th>
      <th>Morgan Stanley</th>
      <th>Goldman Sachs</th>
      <th>J.P. Morgan</th>
    </tr>
    <tr>
      <th>Date</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2004-12-31</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2005-01-03</th>
      <td>0.001868</td>
      <td>0.006844</td>
      <td>0.008747</td>
      <td>0.003589</td>
    </tr>
    <tr>
      <th>2005-01-04</th>
      <td>-0.008494</td>
      <td>-0.010734</td>
      <td>-0.006479</td>
      <td>-0.018902</td>
    </tr>
    <tr>
      <th>2005-01-05</th>
      <td>0.012537</td>
      <td>-0.005787</td>
      <td>-0.004507</td>
      <td>0.002083</td>
    </tr>
    <tr>
      <th>2005-01-06</th>
      <td>0.009699</td>
      <td>0.023645</td>
      <td>0.013776</td>
      <td>0.005716</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>2010-12-23</th>
      <td>-0.010571</td>
      <td>0.000365</td>
      <td>-0.011792</td>
      <td>-0.001897</td>
    </tr>
    <tr>
      <th>2010-12-27</th>
      <td>0.019231</td>
      <td>0.003648</td>
      <td>0.013305</td>
      <td>0.014021</td>
    </tr>
    <tr>
      <th>2010-12-28</th>
      <td>0.002096</td>
      <td>0.005453</td>
      <td>-0.003768</td>
      <td>-0.001406</td>
    </tr>
    <tr>
      <th>2010-12-29</th>
      <td>-0.002092</td>
      <td>-0.013738</td>
      <td>-0.009220</td>
      <td>-0.005867</td>
    </tr>
    <tr>
      <th>2010-12-30</th>
      <td>-0.002096</td>
      <td>0.001833</td>
      <td>0.000060</td>
      <td>-0.003069</td>
    </tr>
  </tbody>
</table>
<p>1511 rows × 4 columns</p>
</div>




```python
weights = [0.25, 0.25, 0.25, 0.25]


# Create portfolio returns for the two sub-periods using the list of asset returns
portfolio_returns = np.array([ x.dot(weights) for x in asset_returns])

# Derive portfolio losses from portfolio returns
losses = - portfolio_returns

# Find the historical simulated VaR estimates
VaR_95 = [np.quantile(x, 0.95) for x in losses]

# Display the VaR estimates
print("VaR_95, 2005-2006: ", VaR_95[0], '; VaR_95, 2007-2009: ', VaR_95[1])
```

    VaR_95, 2005-2006:  0.01468718447283454 ; VaR_95, 2007-2009:  0.0579057406681419



```python
e_cov = crisis_returns.cov().values.tolist()
N = 1000
total_steps = 1440
# mean asset losses
mu = np.array([[ 0.00048534],[-0.00042112],[-0.00074171],[-0.00056848]])

# Initialize daily cumulative loss for the assets, across N runs
daily_loss = np.zeros((4,N))

# Create the Monte Carlo simulations for N runs
for n in range(N):
    # Compute simulated path of length total_steps for correlated returns
    correlated_randomness = e_cov @ norm.rvs(size = (4,total_steps))
    # Adjust simulated path by total_steps and mean of portfolio losses
    steps = 1/total_steps
    minute_losses = mu * steps + correlated_randomness * np.sqrt(steps)
    daily_loss[:, n] = minute_losses.sum(axis=1)
    
# Generate the 95% VaR estimate
losses = weights @ daily_loss
print("Monte Carlo VaR_95 estimate: ", np.quantile(losses, 0.95))
```

    Monte Carlo VaR_95 estimate:  0.003867634004813328


### Crisis structural break: I
You have already seen in Chapters 1 and 2 that the global financial crisis changed investor perception regarding market risk, and influenced investor decisions on portfolio allocations to manage risk.

Now you'll have a chance to investigate whether something "structural" changed between 2005 and 2010. In this exercise you can see if quarterly minimum portfolio values and mean return volatility time series together identify a structural break.

You'll check this first with a simple visualization of the data. Plot the quarterly minimum portfolio returns port_q_min and mean return volatility vol_q_mean to identify a date where a structural break may have occurred.


```python
portfolio_q_min = portfolio_returns['Citibank'].resample('Q').min().dropna()
portfolio_q_vol = portfolio_returns['Citibank'].resample('Q').std().dropna()
```


    ---------------------------------------------------------------------------

    IndexError                                Traceback (most recent call last)

    <ipython-input-42-78c6dd33b44f> in <module>
    ----> 1 portfolio_q_min = portfolio_returns['Citibank'].resample('Q').min().dropna()
          2 portfolio_q_vol = portfolio_returns['Citibank'].resample('Q').std().dropna()


    IndexError: only integers, slices (`:`), ellipsis (`...`), numpy.newaxis (`None`) and integer or boolean arrays are valid indices



```python
# Create a plot of quarterly minimum portfolio returns
plt.plot(portfolio_q_min, label="Quarterly minimum return")

# Create a plot of quarterly mean volatility
plt.plot(portfolio_q_vol, label="Quarterly mean volatility")

# Create legend and plot
plt.legend()
plt.show()
```

As you can see from the visualization, there appears to be a discrete change somewhere in the first half of 2008, but it's unclear if this is just a temporary 'blip' or something more structural. We'll now proceed to test this by building the Chow test statistic.

### Crisis structural break: II
The video identified a structural break for a simple relationship between population size and time in China. In this and the following exercise you'll use the richer factor model relationship between portfolio returns and mortgage delinquencies from Chapter 1 to test for a structural break around 2008, by computing the Chow test statistic for the factor model.

First, after importing the statsmodels API, you'll run an OLS regression for 2005 - 2010, with quarterly minimum returns port_q_min as the dependent variable, and mortgage delinquencies mort_del as the independent variable (plus an intercept term).

Take note of the sum of squared residuals ssr_total from the regression result (this will be provided in the next exercise to help derive the Chow test statistic).


```python
port_q_min = pd.read_csv('./port_q_min.csv', header=None)
port_q_min = pd.DataFrame(port_q_min.values, columns = ["Date", ''])
port_q_min.set_index('Date', inplace=True)
port_q_min = port_q_min.T.iloc[0].astype(float) # converting df to Series
```


```python
# Import the statsmodels API to be able to run regressions
import statsmodels.api as sm

# Add a constant to the regression
mort_del = sm.add_constant(mort_del)

# Regress quarterly minimum portfolio returns against mortgage delinquencies
result = sm.OLS(port_q_min, mort_del).fit()

# Retrieve the sum-of-squared residuals
ssr_total = result.ssr
print("Sum-of-squared residuals, 2005-2010: ", ssr_total)
```

Good. The sum-of-squared residual total you found here will be brought over into the next exercise, where it will be used to build the Chow test for the crisis period!

### Crisis structural break: III
Now you can put everything together to perform the Chow test.

The 2005 - 2010 data have been split into two available DataFrames, before and after, using June 30, 2008 as the structural break point (identified in the first exercise in this series). The columns of both DataFrames are mort_del and returns for mortgage delinquency data and returns data, respectively.

You'll run two OLS regressions on before and after, regressing the returns column against the mort_del column in each DataFrame, and derive the sum-of-squared residuals.

Then you'll compute the Chow test statistic as in the video, using ssr_total (provided from the second exercise) and the derived residuals. The critical F-value at 99% confidence is around 5.85. What value do you find for your test statistic?


```python
before = pd.read_csv('./before.csv', header=0)
before.set_index('Date', inplace=True)

after = pd.read_csv('./after.csv', header=0)
after.set_index('Date', inplace=True)
after['mort_del']
```


```python
# Add intercept constants to each sub-period 'before' and 'after'
before_with_intercept = sm.add_constant(before['mort_del'])
after_with_intercept  = sm.add_constant(after['mort_del'])

# Fit OLS regressions to each sub-period
r_b = sm.OLS(before['returns'], before_with_intercept).fit()
r_a = sm.OLS(after['returns'],  after_with_intercept).fit()

# Get sum-of-squared residuals for both regressions
ssr_before = r_b.ssr
ssr_after = r_a.ssr
# Compute and display the Chow test statistic
numerator = ((ssr_total - (ssr_before + ssr_after)) / 2)
denominator = ((ssr_before + ssr_after) / (24 - 4))
print("Chow test statistic: ", numerator / denominator)
```

Excellent! Your test statistic was well above the critical F-value, indicating that a structural break in the data occurred in the summer of 2008. We'll investigate the consequences of such a structural break for risk management in Chapter 4.

### Volatility and structural breaks
Visualizing volatility changes helps reveal possible structural break points in time series. By identifying when volatility appears to change, an informed choice of break point can be made that can, in turn, be used for further statistical analysis (such as the Chow test).

You'll examine two visualizations of volatility for the investment bank portfolio from 2008 - 2009, for two available portfolio weights: weights_with_citi and weights_without_citi. These correspond, respectively, to equal-weighted portfolios with and without Citibank, which exhibited (as you saw in Chapter 1) the highest volatility of the four assets over the period.

The portfolio prices for 2008 - 2009 with Citibank are available as prices_with_citi, and without Citibank as prices_without_citi


```python
weights_with_citi = [0.25, 0.25, 0.25, 0.25]
weights_without_citi = [0.3333333333333333, 0.3333333333333333, 0.3333333333333333]
prices_with_citi = pd.read_csv('./prices_with_city.csv', header=0)
prices_with_citi.set_index('Date', inplace=True)

prices_without_citi = pd.read_csv('./prices_without_city.csv', header=0)
prices_without_citi.set_index('Date', inplace=True)
```


```python
# Find the time series of returns with and without Citibank
ret_with_citi = prices_with_citi.pct_change().dot(weights_with_citi)
ret_without_citi = prices_without_citi.pct_change().dot(weights_without_citi)

# Find the average 30-day rolling window volatility as the standard deviation
vol_with_citi = ret_with_citi.rolling(30).std().dropna().rename("With Citi")
vol_without_citi = ret_without_citi.rolling(30).std().dropna().rename("Without Citi")

# Combine two volatilities into one Pandas DataFrame
vol = pd.concat([vol_with_citi, vol_without_citi], axis=1)

# Plot volatilities over time
vol.plot().set_ylabel("Losses")
plt.show()
```


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    /var/folders/g4/6dd139k115j_s9grl9d6l56h0000gq/T/ipykernel_27838/3652006667.py in <module>
          1 # Find the time series of returns with and without Citibank
    ----> 2 ret_with_citi = prices_with_citi.pct_change().dot(weights_with_citi)
          3 ret_without_citi = prices_without_citi.pct_change().dot(weights_without_citi)
          4 
          5 # Find the average 30-day rolling window volatility as the standard deviation


    NameError: name 'prices_with_citi' is not defined


Nice job. The visualizations show that Citibank's volatility alone was not responsible for the increase in portfolio volatility during the crisis. This lends futher support to a structural break sometime around the summer/fall of 2008.

### Extreme values and backtesting
Extreme values are those which exceed a threshold and are used to determine if risk measures such as VaR are accurately reflecting the risk of loss.

You'll explore extreme values by computing the 95% VaR of the equally-weighted investment bank portfolio for 2009-2010 (recall that this is equivalent to historical simulation from 2010 onwards), and then backtesting on data from 2007-2008.

2009-2010 portfolio losses are available in estimate_data, from which you'll compute the 95% VaR estimate. Then find extreme values exceeding the VaR estimate, from the 2007-2008 portfolio losses in the available backtest_data.

Compare the relative frequency of extreme values to the 95% VaR, and finally visualize the extreme values with a stem plot.


```python
estimate_data = pd.read_csv('2009-2010_losses.csv', header=None)
estimate_data = pd.DataFrame(estimate_data.values, columns = ["Date", ''])
estimate_data.set_index('Date', inplace=True)

backtest_data = pd.read_csv('backtest_data_losses_2007_2008_daily.csv', header=None)
backtest_data = pd.DataFrame(backtest_data.values, columns = ['Date', ''])
backtest_data.set_index('Date', inplace=True)
backtest_data.index = pd.to_datetime(backtest_data.index, format='%Y/%m/%d')
backtest_data.head()
```


```python
# Compute the 95% VaR on 2009-2010 losses
VaR_95 = np.quantile(estimate_data, 0.95)

# Find backtest_data exceeding the 95% VaR
extreme_values = backtest_data[backtest_data > VaR_95]

# Compare the fraction of extreme values for 2007-2008 to the Var_95 estimate
print("VaR_95: ", VaR_95, "; Backtest: ", len(extreme_values) / len(backtest_data) )

# Plot the extreme values and look for clustering
plt.stem(extreme_values.index, extreme_values, use_line_collection=True)
plt.ylabel("Extreme values > VaR_95"); plt.xlabel("Date")
plt.show()
```

## Advanced Risk Management

### Block maxima
Until now you've worked with a portfolio of four investment banks for the period 2005 - 2010. Now you'll zero in on a single asset, the stock of General Electric, for the same period and apply extreme value theory to its time series.

In this exercise, you'll examine the time series of block maxima for GE's losses over the period 2008 - 2009, using the .resample() method for three different block lengths: one week, one month, and one quarter, visualizing each series in a plot using the axis_* plot objects.


```python
losses = portfolio_losses.loc['2007-01-04':'2009-12-30']
montly_maxima = losses.resample("M").max()
```


```python
# Resample the data into monthly blocks
monthly_maxima = losses.resample("M").max()
quarterly_maxima = losses.resample("Q").max()
weekly_maxima = losses.resample("W").max()

# Plot the resulting monthly maxima
plt.plot(monthly_maxima, label = "Monthly Maxima")
plt.plot(quarterly_maxima, label = "Monthly Maxima")
plt.plot(weekly_maxima, label = "Monthly Maxima")
plt.legend()
plt.figure("monthly")
```

### Extreme events during the crisis
You can use the Generalized Extreme Value (GEV) distribution to examine extreme values in the losses of General Electric (GE) during the financial crisis in 2008 and 2009.

This period coincided with GE's liquidity crisis, and its eventual requirement of an emergency investment of $3 billion from Berkshire Hathaway's Warren Buffet to stave off defaulting on its commercial paper obligations.

GE's losses and weekly maximum losses weekly_max are available, as is the GEV genextreme distribution from scipy.stats.


```python
losses = portfolio_losses.loc['2007-01-04':'2009-12-30']
type(losses)
```


```python
# Plot the log daily losses of GE over the period 2007-2009
losses.plot()

# Find all daily losses greater than 10%
extreme_losses = losses[losses > 0.1]

# Scatter plot the extreme losses
extreme_losses.plot(style='o')
plt.show()
```


```python
weekly_max = losses.resample('W').max()
```


```python
# Generalized Extreme Value (GEV)
from scipy.stats import genextreme

# Fit extreme distribution to weekly maximum of losses
fitted = genextreme.fit(weekly_max)

# Plot extreme distribution with weekly max losses historgram
x = np.linspace(min(weekly_max), max(weekly_max), 100)
plt.plot(x, genextreme.pdf(x, *fitted))
plt.hist(weekly_max, 50, density = True, alpha = 0.3)
plt.show()
```

### GEV risk estimation
Suppose that you were holding € 1,000,000 of GE stock on January 1, 2010. You would like to cover the expected maximum losses that might occur over the next week, based upon available data from the previous two years, 2008 - 2009. You assume that maximum weekly losses for GE are distributed according to a Generalized Extreme Value (GEV) distribution.

To model expected losses you'll estimate the CVaR at the 99% confidence level for the GEV distribution, and use it to compute the amount needed in reserve to cover the expected maximum weekly loss over January, 2010.

The genextreme distribution from scipy.stats is available in your workspace, as is GE's losses for the 2008 - 2009 period.


```python
# Compute the weekly block maxima for GE's stock
weekly_maxima = losses.resample("W").max()

# Fit the GEV distribution to the maxima
p = genextreme.fit(weekly_maxima)

# Compute the 99% VaR (needed for the CVaR computation)
VaR_99 = genextreme.ppf(0.99, *p)

# Compute the 99% CVaR estimate
CVaR_99 = (1 / (1 - 0.99)) * genextreme.expect(lambda x: x, 
           args=(p[0],), loc = p[1], scale = p[2], lb = VaR_99)

# Display the covering loss amount
print("Reserve amount: ", 1000000 * CVaR_99)
```

### KDE of a loss distribution
Kernel density estimation (KDE) can fit distributions with 'fat tails', i.e. distributions with occasionally large deviations from the mean (such as the distribution of portfolio losses).

In Chapter 2 you learned about the Student's T distribution, which for low degrees of freedom can also capture this feature of portfolio losses.

You'll compare a Gaussian KDE with a T distribution, each fitted to provided portfolio losses from 2008 - 2009. You'll visualize the relative fits of each using a histogram. (Recall the T distribution uses fitted parameters params, while the gaussian_kde, being non-parametric, returns a function.)

The function gaussian_kde() is available, as is the t distribution, both from scipy.stats. Plots may be added to the provided axis object.


```python
from scipy.stats import t, gaussian_kde


# Generate a fitted T distribution over losses
params = t.fit(losses)

# Generate a Gaussian kernal density estimate over losses
kde = gaussian_kde(losses)

# Add the PDFs of both estimates to a histogram, and display
loss_range = np.linspace(np.min(losses), np.max(losses), 1000)
plt.plot(loss_range, t.pdf(loss_range, *params), label = 'T distribution')
plt.plot(loss_range, kde.pdf(loss_range), label = 'Gaussian KDE')
plt.hist(losses, bins = 50, density = True)
plt.legend(); plt.show()
```

Great! Both estimates fit the portfolio data better than a Normal distribution. In this example, while the T fits the peak of the data histogram better, the Gaussian KDE fits the tails better. Both parametric and non-parametric estimation are used extensively in statistics and risk management.

### CVaR and loss cover selection
In previous exercises you saw that both the T and the Gaussian KDE distributions fit portfolio losses for the crisis period fairly well. Given this, which of these is best for risk management? One way to choose is to select the distribution that provides the largest loss cover, to cover the "worst worst-case scenario" of losses.

The t and kde distributions are available and have been fit to 2007-2008 portfolio losses (t fitted parameters are in p). You'll derive the one day 99% CVaR estimate for each distribution; the largest CVaR estimate is then the 'safest' reserve amount to hold, covering expected losses that exceed the 99% VaR.

The kde instance has been given a special .expect() method, just for this exercise, to compute the expected value needed for the CVaR.


```python
def expect(func, lb = -np.inf):
  return integrate.quad(lambda y: func(y) * kde.pdf(y), a = lb, b = np.inf)[0]
```


```python
p = (1.8120948399346082, 0.0017173247229661467, 0.017367197331050646)
```


```python
# Find the VaR as a quantile of random samples from the distributions
VaR_99_T   = np.quantile(t.rvs(size=1000, *p), 0.99)
VaR_99_KDE = np.quantile(kde.resample(size=1000), 0.99)

# Find the expected tail losses, with lower bounds given by the VaR measures
integral_T   = t.expect(lambda x: x, args = (p[0],), loc = p[1], scale = p[2], lb = VaR_99_T)
integral_KDE = kde.expect(lambda x: x, lb = VaR_99_KDE)

# Create the 99% CVaR estimates
CVaR_99_T   = (1 / (1 - 0.99)) * integral_T
CVaR_99_KDE = (1 / (1 - 0.99)) * integral_KDE

# Display the results
print("99% CVaR for T: ", CVaR_99_T, "; 99% CVaR for KDE: ", CVaR_99_KDE)
```
