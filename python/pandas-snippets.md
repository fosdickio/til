# Pandas Snippets

## Load a CSV
```python
import pandas as pd

df = pd.read_csv('data/AAPL.csv')
```

## DataFrame Basics
```python
df.head()
df.tail()

# Print rows between index 10 and 20
print(df[10:21])

print(df['Open'].max())
print(df['Close'].mean())
```

## Create an Empty DataFrame
```python
start_date = '2010-01-22'
end_date = '2010-01-26'
dates = pd.date_range(start_date, end_date)
df1 = pd.DataFrame(index=dates)
```

## Join Data
[Join Documentation](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.join.html)
```python
df_spy = pd.read_csv('data/SPY.csv', index_col='Date', parse_dates=True,
                     usecols=['Date', 'Adj Close'], na_values=['nan'])
df1 = df1.join(df_spy)
df1 = df1.dropna()
```

## Matplotlib
```python
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('data/GOOG.csv')

# Plot one column
df['Adj Close'].plot()
plt.show()

# Plot two columns
df[['Close', 'Adj Close']].plot()
plt.show()
```
