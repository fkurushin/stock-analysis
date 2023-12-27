import pandas as pd
from prophet import Prophet

def forecast(df, future_period=365):
    # Create a Prophet model
    m = Prophet()

    # Fit the model to the data
    m.fit(df)

    # Make future predictions
    future = m.make_future_dataframe(periods=future_period)
    forecast = m.predict(future)

    return forecast