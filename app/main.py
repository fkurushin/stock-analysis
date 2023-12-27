from datadownloader.loader import download_data
from prophetmodel.model import forecast

import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd


def main():
    # Set Streamlit app title and description
    st.title('Time Series Forecasting App')
    st.write('My Forecast Data.')

    ticker = "SBER"  # задаём тикер
    period = 7
    start = "01.01.2023"
    end = "26.12.2023"

    df = download_data(ticker, period, start, end)
    df = df[['<DATE>', '<CLOSE>']]
    df.columns = ['ds', 'y']

    forecast_data = forecast(df, 20)

    df['ds'] = pd.to_datetime(df['ds'])
    df['y'] = df['y'].astype(float)

    fig, ax = plt.subplots()
    ax.plot(df.ds, df.y, label='quotes')
    ax.plot(forecast_data.ds, forecast_data.yhat, label='predict')
    plt.title(ticker)
    plt.legend()
    st.pyplot(plt.gcf())


if __name__ == '__main__':
    main()
