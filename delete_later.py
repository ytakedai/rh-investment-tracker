import pandas as pd

STOCKS = pd.read_csv("stocks.csv")
print(STOCKS.dtypes)

num = STOCKS.loc[STOCKS['Symbol'] == 'FB', 'LocalMin'].tolist()[0]
print(num)
type(num)
