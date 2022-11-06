import numpy as np
import pandas as pd
import datetime
import pandas_datareader.data as wb
import matplotlib as plt 
import seaborn as sns
import plotly.plotly as py
import cufflinks as cf
import plotly.offline as offline
import plotly.graph_objs as go
from plotly import __version__
from plotly.offline import download_plotlyjs,init_notebook_mode,plot,iplot

start=datetime.datetime(2006,1,1)
end=datetime.datetime(2016,1,1)


BAC=wb.DataReader('BAC','yahoo',start,end)
CITI=wb.DataReader('C','yahoo',start,end)
GS=wb.DataReader('GS','yahoo',start,end)
JPM=wb.DataReader('JPM','yahoo',start,end)
MS=wb.DataReader('MS','yahoo',start,end)
WF=wb.DataReader('WF','yahoo',start,end)

#** Create a list of the ticker symbols (as strings) in alphabetical order. Call this list: tickers**

tickers=['BAC','citi','GS','JPM','MS','WF']


bank_stocks=pd.concat([BAC,CITI,GS,JPM,MS,WF],axis=1,keys=tickers)

#** Set the column name levels (this is filled out for you):**


bank_stocks.columns.names=['Bank tickers','stock info']

#** Check the head of the bank_stocks dataframe.**

bank_stocks.head()


# EDA

#**Let's explore the data a bit! Before continuing, I encourage you to check out the documentation on [Multi-Level Indexing](http://pandas.pydata.org/pandas-docs/stable/advanced.html) and [Using .xs](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.xs.html).Reference the solutions if you can not figure out how to use .xs(), since that will be a major part of this project.

#** What is the max Close price for each bank's stock throughout the time period?**


bank_stocks.xs(key='Close',axis=1,level='stock info').max()

for i in tickers:
    print(i +'    = ',bank_stocks[i]['Close'].max())



#** Create a new empty DataFrame called returns. This dataframe will contain the returns for each bank's stock. returns are typically defined by:**

#$$r_t = \frac{p_t - p_{t-1}}{p_{t-1}} = \frac{p_t}{p_{t-1}} - 1$$


returns=pd.DataFrame()


#** We can use pandas pct_change() method on the Close column to create a column representing this return value. Create a for loop that goes and for each Bank Stock Ticker creates this returns column and set's it as a column in the returns DataFrame.**


for i in tickers:
    returns[i +' return']=bank_stocks[i]['Close'].pct_change()
returns['citi return'].plot()


#** Create a pairplot using seaborn of the returns dataframe. What stock stands out to you? Can you figure out why?**


sns.pairplot(returns[1:])

#* See solution for details about Citigroup behavior....

returns.idxmin()

returns.idxmax()

#** You should have noticed that Citigroup's largest drop and biggest gain were very close to one another, did anythign significant happen in that time frame? **


#**Riskiest stock **

returns.std()

#** Create a distplot using seaborn of the 2015 returns for Morgan Stanley **

sns.set_style('whitegrid')

sns.distplot(returns.loc['2015-01-01':'2015-12-31']['MS return'],bins=50,color='g')


#** Create a distplot using seaborn of the 2008 returns for CitiGroup **

sns.distplot(returns.loc['2008':'2008']['citi return'],color='r',bins=50)

## More Visualization

#A lot of this project will focus on visualizations. Feel free to use any of your preferred visualization libraries to try to recreate the described plots below, seaborn, matplotlib, plotly and cufflinks, or just pandas.

### Imports

import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')

# Optional Plotly Method Imports
import plotly
import cufflinks as cf
cf.go_offline()


#** Create a line plot showing Close price for each bank for the entire index of time.

plt.figure(figsize=(12,4))

bank_stocks.xs(key='Close',axis=1,level='stock info').plot(figsize=(12,4))

for i in tickers:
    bank_stocks[i]['Close'].plot(figsize=(12,4),label=i)
plt.legend()


## Moving Averages 
# Let's analyze the moving averages for these stocks in the year 2008. 

#** Plot the rolling 30 day average against the Close Price for Bank Of America's stock for the year 2008**


bank_stocks['BAC']['Close'].loc['2008-01-01':'2009-01-01'].rolling(window=30).mean().plot(figsize=(12,4),label="30 day AVg rolling price")
bank_stocks['BAC']['Close'].loc['2008-01-01':'2009-01-01'].plot(label="BAC Close")
plt.legend()


#** Create a heatmap of the correlation between the stocks Close Price.**

plt.figure(figsize=(7,4))

sns.heatmap(bank_stocks.xs(key='Close',axis=1,level="stock info").corr(),annot=True)

sns.clustermap(bank_stocks.xs(key='Close',axis=1,level="stock info").corr(),annot=True)

# Part 2 (Optional)

import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')

import plotly.graph_objects as go
from plotly.offline import download_plotlyjs,init_notebook_mode,plot,iplot
# Optional Plotly Method Imports
import plotly
import cufflinks as cf
cf.go_offline()


#** Use .iplot(kind='candle) to create a candle plot of Bank of America's stock from Jan 1st 2015 to Jan 1st 2016.**

bank_stocks['BAC'].loc['2015-01-01':'2016-01-01'].iplot(kind='candle')


#** Use .ta_plot(study='sma') to create a Simple Moving Averages plot of Morgan Stanley for the year 2015.**

bank_stocks['MS'].loc['2015':'2015'].ta_plot(study='sma')

#S**Use .ta_plot(study='boll') to create a Bollinger Band Plot for Bank of America for the year 2015.**

bank_stocks['MS'].loc['2015':'2015'].ta_plot(study='boll')

print(bank_stocks)



