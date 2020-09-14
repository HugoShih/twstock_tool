import streamlit as st
import pandas as pd
from data import get_tw_equity, get_company_info, stock_ohlc, get_stock_history
import datetime
import math
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM
from sklearn import metrics
import matplotlib.pyplot as plt

def write():
    st.title("Company")
    df = get_tw_equity()
    tw_equity_sector = sorted(df["sector"].unique().tolist())
    tw_sector = st.sidebar.selectbox("Select sector", tw_equity_sector)
    stock = st.sidebar.text_input("Enter symbol", value="")
    stock_lst = df[df.sector == tw_sector].rename(columns={"longName":"Company Name"})
    st.write(f"Sector: {tw_sector}")

    if stock == "":
        st.table(stock_lst[["symbol","Company Name"]].reset_index(drop=True))
    else:
        company_info = get_company_info(f"{stock}.TW")
        st.write(f"Company Name: {company_info['longName']}")
        st.write(f"Industry: {company_info['industry']}")
        business_summary = st.checkbox("Business Summary")
        if business_summary:
            st.write(company_info['longBusinessSummary'])
        contact_info = st.checkbox("Contact Info")
        if contact_info:
            st.write(f"City: {company_info['city']}")
            st.write(f"Phone: {company_info['phone']}")
            st.write(f"Website: {company_info['website']}")

        st.sidebar.header("Finance")
        market_info = st.sidebar.checkbox("Market Info")

        if market_info:
            st.subheader("Open - High - Low - Close")
            st.text("1 Month History Data")
            time_range = "1mo"
            st.dataframe(stock_ohlc(stock, time_range))
        stock_pred = st.sidebar.checkbox("Stock Price Prediction")
        if stock_pred:
            st.subheader("Next day stock predictions")

            option = {"High":"highest", "Low":"lowest", "Open":"open", "Close":"close"}
            def format_func(item):
                return option[item]
            word = st.selectbox('Select a feature you want to predict', options=list(option.keys()))
            
            num_days= st.text_input("Enter a number of days", "1")
            num_days = int(num_days)
            st.info(f"Predict the {format_func(word)} price of the next deal day based on past {num_days} days")

            df = get_stock_history(f"{stock}.TW")
            df_new = df[[word]]
            dataset = df_new.values
            #test:train = 3:7
            training_data_len = math.ceil(len(dataset) *.7)
            scaler = MinMaxScaler(feature_range=(0, 1))
            scaled_data = scaler.fit_transform(dataset)

            #Create a training data set that contains the past 1 day closing price values
            #that we want to use to predict the 15st closing price value.
            train_data = scaled_data[0:training_data_len, : ]
            x_train, y_train = [], []
            for i in range(num_days,training_data_len):
                x_train.append(scaled_data[i-num_days:i,0])
                y_train.append(scaled_data[i,0])
            x_train, y_train = np.array(x_train), np.array(y_train)
            x_train = np.reshape(x_train, (x_train.shape[0],x_train.shape[1],1))

            lstm = Sequential()
            lstm.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1],1)))
            lstm.add(LSTM(units=50))
            lstm.add(Dense(1))
            lstm.compile(loss='mean_squared_error', optimizer='adam')

            if st.button('Train the model'):
                with st.spinner("Training may take time based on number of days. Please wait..."):
                    history_lstm = lstm.fit(x_train, y_train, epochs=25, batch_size=10, verbose=2)
                    st.success("Model is ready!")


                test_data = scaled_data[training_data_len - num_days: , : ]
                x_test = []
                y_test =  dataset[training_data_len : , : ]
                for i in range(num_days,len(test_data)):
                    x_test.append(test_data[i-num_days:i,0])
                x_test = np.array(x_test)
                x_test = np.reshape(x_test, (x_test.shape[0],x_test.shape[1],1))

                pred = lstm.predict(x_test)
                pred = scaler.inverse_transform(pred)

                st.header("Prediction")
                #inputs are data of past ? days
                inputs = df_new.iloc[len(df_new)-num_days:len(df_new)].values
                inputs = inputs.reshape(-1,1)
                inputs  = scaler.fit_transform(inputs)
                p = inputs.reshape(1,num_days,1)#(Samples,time_step,features)
                result = lstm.predict(p)
                result = scaler.inverse_transform(result)
                st.write("The {} price of next deal day is :".format(word))
                st.info(round(float(result),2))

                def get_mape(y_true, y_pred):
                    """
                    Compute mean absolute percentage error (MAPE)
                    """
                    y_true, y_pred = np.array(y_true), np.array(y_pred)
                    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

                st.header("Model Evaluation")
                st.write('R Square - ',round(metrics.r2_score(y_test,pred),2))
                st.write('Mean absolute percentage error(MAPE) - ', round(get_mape(y_test,pred), 2))
                st.write('Root Mean Square Error(RMSE) -', round(np.sqrt(metrics.mean_squared_error(y_test,pred)),2))
                st.write('Mean Absolute Error(MAE) - ', round(metrics.mean_absolute_error(y_test,pred),2))

                # #st.header('Model Loss')
                # plt.figure(figsize=(5,5))
                # plt.plot(history_lstm.history['loss'], label='Train')
                # plt.legend()
                # plt.title('Model Loss')
                # plt.xlabel('Epoch')
                # plt.ylabel('Mean Square Error')
                # st.pyplot()

                # #Plot/Create the data for the graph
                # train = df_new[:training_data_len]
                # val = df_new[training_data_len:]
                # val['Predictions'] = pred

                # st.header('Testing Results')
                # #Visualize the data
                # plt.figure(figsize=(16,8))
                # plt.title('LSTM Model',fontsize=18)
                # plt.xlabel('Date', fontsize=18)
                # plt.ylabel("{} price USD ($)".format(word), fontsize=18)
                # plt.plot(train[word])
                # plt.plot(val[[word, 'Predictions']])
                # plt.legend(['Train', 'Val', 'Predictions'], loc='lower right')
                # st.pyplot(clear_figure=True)
