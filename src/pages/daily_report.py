import streamlit as st
from data import get_data, get_type
import pandas as pd

def write():
    st.header("Taiwan Stocks Daily Report")
    select_date = st.date_input("Select date")
    str_select_date = select_date.strftime("%Y%m%d")
    st.sidebar.subheader("Option")
    type_lst = get_type()
    stock_type = st.sidebar.selectbox("Select type", type_lst)
    if stock_type == "ALL - 全部":
        stock_type = "ALL"
    else:
        stock_type = stock_type[0:2]

    if st.button('Check'):
        if type(get_data(str_select_date, stock_type)) != pd.DataFrame:
            st.write("No available data .")
        else:
            df = get_data(str_select_date, stock_type)[["證券代號","證券名稱","開盤價","最高價","最低價","收盤價","本益比"]]\
                .set_index("證券代號")
            st.dataframe(df)    
