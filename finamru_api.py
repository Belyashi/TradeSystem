import numpy as np
import pandas as pd

URL = ('http://export.finam.ru/data.csv?'
       'market={market}&em={em}&code={code}&apply=0&df={df}&mf={mf}&'
       'yf={yf}&from={from_date}&dt={dt}&mt={mt}&yt={yt}&to={to_date}&p=1&f=data&e=.csv&'
       'cn={code}&dtf=1&tmf=1&MSOR=1&mstime=on&mstimever=1&sep=1&sep2=1&datf=7&at=1')

STOCKS = {
    ('NASDAQ', 'AAPL'): {
        'market_id': 25,
        'stock_id': 20569,
        'code': 'US2.AAPL'
    }
}


def load_history(market, code, from_date, to_date):
    """Loads history using finam.ru. from_date and to_date is of Moscow timezone."""

    config = STOCKS.get((market, code))
    if config is None:
        raise ValueError('finam.ru do not have information about {}.{} stock'.format(market, code))

    url = URL.format(market=config['market_id'],
                     em=config['stock_id'],
                     code=config['code'],

                     df=from_date.day,
                     mf=from_date.month - 1,
                     yf=from_date.year,
                     from_date=from_date.strftime('%d.%m.%Y'),

                     dt=to_date.day,
                     mt=to_date.month - 1,
                     yt=to_date.year,
                     to_date=to_date.strftime('%d.%m.%Y'))

    df = pd.read_csv(url, dtype={
        '<DATE>': str,
        '<TIME>': np.int64,
        '<LAST>': np.float64,
        '<VOL>': np.int64
    })

    mos_time = (pd.to_datetime(df['<DATE>'], format='%Y%m%d') +
                pd.to_timedelta(df['<TIME>'], unit='s'))
    utc_time = (pd.Series(index=mos_time)
                .tz_localize('Europe/Moscow')
                .tz_convert('UTC')
                .tz_localize(None)
                .index)

    history = pd.DataFrame({
        'time': utc_time,
        'volume': df['<VOL>'],
        'price': df['<LAST>']
    })

    return history
