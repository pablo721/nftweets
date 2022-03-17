import pandas as pd
import ccxt


def get_prices(ticker, exchange, interval, since):
    exchange = getattr(ccxt, exchange)()
    data = []
    count = 0
    while True:
        d2 = exchange.fetch_ohlcv(ticker, interval, since)
        data += d2
        count += 1
        if len(d2) <= 1:
            break
        else:
            since = d2[-1][0]
    df = pd.DataFrame(data)
    df.drop_duplicates(subset=0, inplace=True)
    df.name = ticker + '_' + exchange.id + '_' + interval
    # df.set_index(0, inplace=True)
    return df


def get_corr_matrix(df):
    matrix = pd.DataFrame(columns=df.columns, index=df.columns)
    matrix.index.name = 'corr matrix'
    for col in df.columns:
        for col2 in df.columns:
            matrix.loc[col, col2] = df[col].corr(df[col2]).__round__(3)
    return matrix