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

    pe_ratio = st.sidebar.checkbox("本益比")
    if pe_ratio:
        pe_number_start = st.sidebar.text_input("Start", 15)
        pe_number_end = st.sidebar.text_input("End", 20)

    
    if type(get_data(str_select_date, stock_type)) != pd.DataFrame:
        st.write("No available data .")
    else:
        df = get_data(str_select_date, stock_type)[["證券代號","證券名稱","開盤價","最高價","最低價","收盤價","本益比"]]\
            .set_index("證券代號")
        if pe_ratio == True:
            df = df[(df["本益比"] >= float(pe_number_start)) & (df["本益比"] <= float(pe_number_end))]\
                .sort_values(by=["本益比"], ascending=False)
            st.dataframe(df.style.format({"本益比": '{:.2f}'}))
            symbol = st.text_input("symbol or code")
            st.write(symbol)

            

     

    

    
