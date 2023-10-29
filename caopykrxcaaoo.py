from pykrx import stock
import pandas as pd
from pandas.tseries.offsets import BDay
import numpy as np
import time
from tqdm import tqdm
from datetime import date, timedelta

today = date.today()
last_bday = (today - BDay(1)).date()
fifty_bdays_ago = (last_bday - BDay(50)).date()
last_bday_str = last_bday.strftime('%Y%m%d')
fifty_bdays_ago_str = fifty_bdays_ago.strftime('%Y%m%d')

# pykrx 주가정보 불러오기
ticker_df = pd.DataFrame({'종목코드':stock.get_market_ticker_list(market="ALL")})
ticker_df['종목명'] = ticker_df['종목코드'].map(lambda x: stock.get_market_ticker_name(x))
fundamental_df = pd.DataFrame(stock.get_market_fundamental_by_ticker(date=last_bday_str, market="ALL"))
fundamental_df = fundamental_df.reset_index()
fundamental_df.rename(columns={'티커':'종목코드'}, inplace=True)

merged_df0 = pd.merge(ticker_df, fundamental_df, left_on='종목코드', right_on='종목코드', how='outer')

price_df = stock.get_market_ohlcv_by_ticker(date=last_bday_str, market="ALL")
price_df = price_df.reset_index()
price_df.rename(columns={'티커':'종목코드'}, inplace=True)

merged_df1 = pd.merge(merged_df0, price_df, left_on='종목코드', right_on='종목코드', how='outer')
merged_df1 = merged_df1.replace([0], np.nan)
merged_df1 = merged_df1.dropna(axis=0)


# top100
# 내재가치, 가치비율 계산
merged_df1['내재가치'] = (merged_df1['BPS'] + (merged_df1['EPS']) * 10) / 2
merged_df1['가치비율'] = (merged_df1['내재가치'] / merged_df1['종가'])
sorted_by_tradingvolume_df = merged_df1.sort_values(by='가치비율')
value_ratio_TOP100 = sorted_by_tradingvolume_df.head(100)[['종목코드', '종목명', '가치비율']].reset_index(drop=True)

# 거래량
sorted_by_tradingvolume_df = merged_df1.sort_values(by=['거래량'], ascending=[False])
tradingvolume_TOP100 = sorted_by_tradingvolume_df.head(100)[['종목코드', '종목명', '거래량']].reset_index(drop=True)

# 등락률
sorted_by_flucuation_df = merged_df1.sort_values(by=['등락률'], ascending=[False])
flucuationrate_TOP100 = sorted_by_flucuation_df.head(100)[['종목코드', '종목명', '등락률']].reset_index(drop=True)
SMA20_df = pd.DataFrame(columns=['종목코드', '종목명', 'SMA20'])

# SMA20
for ticker_df in tqdm(stock.get_market_ticker_list(), desc='Calculating SMA20'):  # tqdm 적용
    OHLCV = stock.get_market_ohlcv_by_date(fifty_bdays_ago_str, last_bday_str, ticker_df)
    recent_20_Ohlcv = OHLCV.tail(20)
    moving_average20 = recent_20_Ohlcv['종가'].mean()
    last_close_price = recent_20_Ohlcv['종가'].iloc[-1]
    SMA20 = (last_close_price / moving_average20) * 100
    SMA20_df.loc[len(SMA20_df)] = [ticker_df, stock.get_market_ticker_name(ticker_df), SMA20]
    
    time.sleep(0.25) # 0.2 ~

filtered_SMA20_result_df = SMA20_df[SMA20_df['SMA20'] <= 95]
sorted_SMA20 = filtered_SMA20_result_df.sort_values(by='SMA20', ascending=False)
sorted_SMA20.reset_index(drop=True, inplace=True)
SMA20_TOP100 = sorted_SMA20.head(100)

# 각 데이터프레임에 중요도에 따라 점수 부여하고 새로운 컬럼에 저장
value_ratio_TOP100_copy = value_ratio_TOP100.copy()
value_ratio_TOP100_copy['Score'] = (100 - value_ratio_TOP100_copy.index) * 4

tradingvolume_TOP100_copy = tradingvolume_TOP100.copy()
tradingvolume_TOP100_copy['Score'] = (100 - tradingvolume_TOP100_copy.index) * 1

fluctuationrate_TOP100_copy = flucuationrate_TOP100.copy()
fluctuationrate_TOP100_copy['Score'] = (100 - fluctuationrate_TOP100_copy.index) * 3

SMA20_TOP100_copy = SMA20_TOP100.copy()
SMA20_TOP100_copy['Score'] = (100 - SMA20_TOP100_copy.index) * 2

all_scores = pd.concat([value_ratio_TOP100_copy, tradingvolume_TOP100_copy, fluctuationrate_TOP100_copy, SMA20_TOP100_copy])
all_scores = all_scores[['종목코드', '종목명', 'Score']]
all_scores = all_scores.groupby(['종목코드', '종목명']).sum().reset_index()
all_scores = all_scores.sort_values(by='Score', ascending=False)
scores_TOP100 = all_scores.head(100)
scores_TOP100.reset_index(drop=True, inplace=True)
merged_TOP100_scores = pd.merge(scores_TOP100, fundamental_df, left_on='종목코드', right_on='종목코드', how='left')

# 추가 필터링
filterd_TOP100_score = merged_TOP100_scores[merged_TOP100_scores['PBR'] < 3.5]

average_PER = fundamental_df['PER'].mean()
filterd_TOP100_score = filterd_TOP100_score[filterd_TOP100_score['PER'] <= average_PER]

# 출력
filterd_TOP100_score.reset_index(drop=True, inplace=True)
print(filterd_TOP100_score)
