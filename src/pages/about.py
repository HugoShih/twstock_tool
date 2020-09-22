import streamlit as st

def write():
    st.title("Stock Prediction Tool")
    st.subheader("Introduction:")
    st.markdown("""Hello and welcome to Taiwan Stock Price Prediction Tool.<br>\
        This is the project based on my Data Sciense Bootcamp at Le Wagon. \
    The project will be on going project and I will keep adoptting new models and  more function later\
        with new version.""", unsafe_allow_html=True)
    st.text("")
    st.text("Current version: v1")
    st.text("Update date: 2020.09.14")

    st.markdown("---")
    st.subheader("Disclaimer:")
    st.markdown("This app is only for research and development used only. Website and the information \
        contained herein is not intended to be a source of advice or credit analysis with respect to \
            the material presented, and the information and/or documents contained in this website do \
                not constitute investment advice. The data and result should not be considered \
                    professional financial investment advice. Please do your own research.")
    st.markdown("---")
    st.subheader("Usage Guide:")
    st.markdown("Menu:")
    st.markdown("• About (which is the current page)")
    st.markdown("• Company info / Finance")
    st.markdown("""When you click "Company info / Finance" button, you will get the following options.""")
    st.image("data/image/company_info.png", width=400)
    st.markdown("First, select the selector you are interested.")
    st.image("data/image/sector.png", width=400)
    st.markdown("It will automatically generate the list on the right side.")
    st.image("data/image/sector_lst.png", width=600)
    st.markdown("""Enter the symbol number you are interested. You can either type the number only (like "1101") or \
        full symbol name (like "1101.TW").Then, press <b>Enter</b>.""", unsafe_allow_html=True)
    st.markdown("Note: If you want to go back to the sector list, please delete the symbol number and press enter.")
    st.image("data/image/symbol.png", width=400)
    st.markdown("After you enter the symbol number, you will get the following options.")
    st.markdown("<b>On the left side:</b>", unsafe_allow_html=True)
    st.markdown("• Market Info: It will give you the OHLC dataframe based on the previous 30 days.")
    st.markdown("• Stock Price Prediction: Predict the price by using Deep Learning")
    st.image("data/image/left.png", width=400)
    st.markdown("<b>On the right side:</b>", unsafe_allow_html=True)
    st.markdown("• Business Summary: More details about this company.")
    st.markdown("• Contact Info: City, phone and website.")
    st.image("data/image/right.png", width=400)
    st.subheader("Prediction Guide:")
    st.markdown("There are 2 options for predicting stock price.")
    st.markdown("• Feature for prediction: High / Low / Open / Close")
    st.markdown("• Number of days: Prediction based on how many days of the historical price. \
        The number is higher, the training process will be slower due to the model is real-time training.")
    st.image("data/image/prediction.png", width=400)
    st.markdown("The result should look like the above image.")
    st.markdown("---")
    st.subheader("Current issue & Future update:")
    st.markdown("1. When the page is refershed or switched, the prediction result will be gone.")
    st.markdown("2. The model isn't pre-trained, and it can't be scalable. Will be fixed in later version.")













    
