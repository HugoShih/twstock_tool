import requests
import pandas as pd
import datetime
import time
import streamlit as st
import yfinance as yf

@st.cache
def get_data(select_date, stock_type):
    try:
        url = "https://www.twse.com.tw/exchangeReport/MI_INDEX?response=json"
        payload = {"date":select_date, "type":stock_type}
        api_data = requests.get(url, params=payload).json()
        if stock_type == "ALL":
            stock_df = pd.DataFrame(api_data["data9"])
        else:
            stock_df = pd.DataFrame(api_data["data1"])
        column_name = ["證券代號", "證券名稱", "成交股數", "成交筆數", "成交金額", "開盤價", "最高價", \
            "最低價", "收盤價", "漲跌", "漲跌價差", "最後揭示買價", "最後揭示買量", "最後揭示賣價", "最後揭示賣量", "本益比"]
        column_name_dict = {i:j for i,j in zip(stock_df.columns, column_name)}
        stock_df = stock_df.rename(columns=column_name_dict)
        stock_df["漲跌"] = stock_df["漲跌"].str[-5:-4:]
        stock_df["本益比"] = pd.to_numeric(stock_df["本益比"], errors='coerce').fillna(0.0)
        # stock_df.to_csv(f"data/csv/{date}_tw_stock.csv", index=False)
        # print(f"Stock on {date} successfully downloaded.")
        return stock_df
        time.sleep(10)
    except KeyError:
        return False
        time.sleep(10)
        pass

def get_type():
    type_lst = ["ALL - 全部", "01 - 水泥工業", "02 - 食品工業", "03 - 塑膠工業", "04 - 紡織纖維", "05 - 電機機械", "06 - 電器電纜", \
                "07 - 化學生技醫療", "08 - 玻璃陶瓷", "09 - 造紙工業", "10 - 鋼鐵工業", "11 - 橡膠工業", "12 - 汽車工業", "13 - 電子工業", \
                    "14 - 建材營造", "15 - 航運業", "16 - 觀光事業", "17 - 金融保險", "18 - 貿易百貨", "19 - 綜合", "20 - 其他", \
                        "21 - 化學工業", "22 - 生技醫療業", "23 - 油電燃氣業", "24 - 半導體業", "25 - 電腦及週邊設備業", \
                        "26 - 光電業", "27 - 通信網路業", "28 - 電子零組件業", "29 - 電子通路業", "30 - 資訊服務業", "31 - 其他電子業"]
    return type_lst

def get_tw_equity():
    tw_equity_df = pd.read_csv("data/yf_tw_equity_list.csv")
    tw_equity_df = tw_equity_df.iloc[:,1:]
    return tw_equity_df

@st.cache
def get_company_info(stock):
    company_dict = yf.Ticker(stock).info
    return company_dict

@st.cache
def get_stock_history(stock):
    start_date = yf.Ticker(stock).history(period="max").reset_index().iloc[0][0].strftime("%Y-%m-%d")
    end_date= datetime.date.today()
    stock_history = yf.Ticker(stock).history(start=start_date, end=end_date)
    return stock_history

@st.cache
def stock_ohlc(stock, time_range):
    ohlc_info = yf.Ticker(f"{stock}.TW").history(period=time_range)
    return ohlc_info.sort_values(by="Date", ascending=False).iloc[:,:-2]
