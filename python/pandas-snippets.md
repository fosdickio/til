# Pandas Snippets

## DataFrames

### Load a CSV
```python
import pandas as pd

df = pd.read_csv('data/AAPL.csv')
```

### DataFrame Basics
```python
df.head()
df.tail()

# Print rows between index 10 and 20
print(df[10:21])

print(df['Open'].max())
print(df['Close'].mean())
```

### Create an Empty DataFrame
- [`date_range` Documentation](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.date_range.html)

```python
start_date = '2010-01-22'
end_date = '2010-01-26'
dates = pd.date_range(start_date, end_date)
df1 = pd.DataFrame(index=dates)
```

### Join Data
- [`join` Documentation](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.join.html)
- [`dropna` Documentation](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.dropna.html)

```python
symbols = ['SPY', 'GOOG', 'IBM', 'GLD']
for symbol in symbols:
    df_temp = pd.read_csv('data/{}.csv'.format(symbol), index_col='Date', 
                          parse_dates=True, usecols=['Date', 'Adj Close'], 
                          na_values=['nan'])
    df_temp = df_temp.rename(columns={ 'Adj Close': Symbol })
df1 = df1.join(df_temp, how='inner')
df1 = df1.dropna(subset=['SPY'])
```

### DataFrame Slicing
- [Indexing and Selecting Data Documentation](https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html)

```python
# Slice by row range (dates)
print(df.ix['2020-01-01' : '2020-01-31'])

# Slice by columns (symbols)
print(df['GOOG'])
print(df['IBM', 'GLD'])

# Slice by row and column
print(df.ix['2020-01-01' : '2020-01-31'], ['SPY', 'IBM'])
```

### Normalizing
```python
# Normalize stock prices using the first row of the DataFrame
df = df / df.ix[0, :]
```

---

## Matplotlib
- [`plot` Documentation](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.plot.html)

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

# Configuring graph labels and properties
ax = df.plot(title='Stock Prices', fontsize=2)
ax.set_xlabel('Date')
ax.set_ylabel('Price')
plt.show()
```

---

## Statistical Analysis

### Global Statistics
```python
df.mean()
df.median()
df.std()
```

### Rolling Statistics
- [`rolling` Documentation](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.rolling.html)
```python
rm_spy = pd.rolling_mean(df['SPY'], window=20)

# Plot SPY, retain matplotlib axis object
ax = df['SPY'].plot(title="SPY Rolling Mean", label='SPY')

# Compute rolling mean using a 20-day window
rm_spy = df['SPY'].rolling(window=20).mean()

# Add rolling mean to same plot
rm_spy.plot(label='Rolling mean', ax=ax)

# Add axis labels and legend
ax.set_xlabel("Date")
ax.set_ylabel("Price")
ax.legend(loc='upper left')
plt.show()
```
