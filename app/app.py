from bokeh.io import curdoc
from bokeh.models import FileInput, Div, ColumnDataSource, DataTable, TableColumn, TextInput, NumericInput,Button
from bokeh.layouts import column,row
from bokeh.plotting import figure
import base64
import io
import pandas as pd
import forecast 

#Initialize an empty data source, table, and figure
source = ColumnDataSource(data={})
columns = [] # Initially empty, will be built on upload
data_table = DataTable(source=source, columns=columns, width=300, height=400)
table_title = Div(text="""<h2>Data Table</h2>""", width=300)
fig = figure(title = "Auto Forecast Plot",width=1500,height=800)
fig.title.text_font_style = 'bold'
fig.title.text_color = 'black'
fig.title.text_font_size = '14pt'
fig.title.align = 'center'
#Create bokeh objects
title = Div(text="""
    <div style="text-align: center; width: 100%;">
        <h1>Auto Forecast Tool</h1>
    </div>
""", width=1800,align='center',sizing_mode='stretch_width')
status_msg = Div(text = "<b>STATUS:</b> Ready")
file_input = FileInput(accept=".csv",title="Upload Time Series Data as CSV")
seasonality = NumericInput(value=1,title="Number of periods in season? Enter 1 if no seasonality.", mode='int')
n_ahead = NumericInput(value=12,title="Number of periods to forecast?", mode='int')
column_name = TextInput(title="Column name to forecast?")
forecast = Button(label="Auto Forecast")


def update_status():
    #Update status
    status_msg.text = "<b>STATUS:</b> Running......"
    curdoc().add_next_tick_callback(upload_callback)

def upload_callback():
    # Decode upload, save to memory, and read in as df
    decoded = base64.b64decode(file_input.value)
    file = io.BytesIO(decoded)
    df = pd.read_csv(file)

    # Make forecasts and append to df
    forecasts = forecast.forecast(df,column_name.value,seasonality.value,n_ahead.value)
    new_data = pd.DataFrame()
    new_data['Forecasts'] = forecasts
    df = pd.concat([df, new_data], ignore_index=True).reset_index()

    #Update the data source
    source.data = df.to_dict('list')
    #Update the columns based on the new file's headers
    data_table.columns = [TableColumn(field=col, title=col) for col in df.columns]

    #Update figure with all data
    fig.line(x='index',y= 'Sales',source=source,line_width=2)
    fig.line(x='index',y= 'Forecasts',source=source,line_width=2,line_color='Red')
    #Update status
    status_msg.text = "<b>STATUS:</b> Complete!"

forecast.on_click(update_status)

layout = column(row(title, align='center'),row(column(status_msg,file_input, seasonality, n_ahead, column_name,forecast, table_title, data_table),fig),sizing_mode='stretch_both')
curdoc().add_root(layout)
