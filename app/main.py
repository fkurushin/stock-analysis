from datadownloader.loader import download_data
from prophetmodel.model import forecast
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
from datadownloader.tickers import tickers
from datadownloader.periods import periods


def main():
    # Set Streamlit app title and description
    st.title('Time Series Forecasting App')
    st.write('My Forecast Data.')

    # Create a data form
    with st.form("my_data_form"):
        ticker = st.selectbox("Select a ticker to predict", tickers.keys(), index=0)

        # period_name = st.selectbox("Select a ticker to predict", periods.keys(), index=0)
        # period = periods[period_name]

        # days_to_predict = st.text_input(f"Add period to predict in ({period_name})")

        days_to_predict = st.number_input("Add period to predict", min_value=0, max_value=1000, step=1, value=10)

        start = st.date_input("Start date", format="DD.MM.YYYY", value=(datetime.today() - timedelta(days=365)).date())
        end = st.date_input("End date", format="DD.MM.YYYY", value=datetime.today())
        start = start.strftime('%d.%m.%Y')
        end = end.strftime('%d.%m.%Y')

        submit_button = st.form_submit_button("Predict")

    if submit_button:
        df = download_data(ticker, 7, start, end)
        # df = df.fillna(0)
        df = df[['<DATE>', '<CLOSE>']]
        df.columns = ['ds', 'y']

        forecast_data = forecast(df, days_to_predict)

        df['ds'] = pd.to_datetime(df['ds'])
        df['y'] = df['y'].astype(float)

        fig, ax = plt.subplots()
        ax.plot(df.ds, df.y, label='quotes')
        ax.plot(forecast_data.ds, forecast_data.yhat, label='predict')
        plt.xticks(rotation=45)
        plt.title(ticker)
        plt.legend()
        st.pyplot(plt.gcf())


if __name__ == '__main__':
    main()
