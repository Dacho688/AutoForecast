from pmdarima import auto_arima
import pandas as pd

def forecast(df, column_name: str, seasonality: int, ahead: int):
    data = df[column_name]
    oos = round(len(data) * .1)
    model = auto_arima(data,m = seasonality, max_order = 10, information_criterion = 'oob', stepwise = False, out_of_sample_size = oos, scoring = 'mse')
    forecasts = model.predict(ahead,return_conf_int = False)
    return forecasts