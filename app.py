import streamlit as st
import polars as pl
import pandas as pd
import plotly.express as px
from retrieveData import data_gatherer

class cleanData:
    def __init__(self, data):
        self.data = data

    def prepare_data(self):
        rows = []
        for date, readings in self.data.items():
            for reading in readings:
                time_in_seconds, value = reading
                time = pd.to_timedelta(time_in_seconds, unit='s')
                rows.append({"date": date, "time": time, "reading": value})
        return pd.DataFrame(rows)

    def plot_data(self, df):
        try:
            df['datetime'] = pd.to_datetime(df['date']) + df['time']


            fig = px.line(df, x='datetime', y='reading',
                          title='Readings Over Time',
                          labels={'datetime': 'Date and Time',
                                  'reading': 'Reading'},
                          markers=True)
            return fig
        except:
            return st.write(f'No data for user')

usernames = data_gatherer.get_clean_data(Type='getusers')
selected_name = st.selectbox("Select a User", list(usernames.keys()))
CustID = usernames[selected_name]

total_data = data_gatherer.get_clean_data(Type='getconsumptionall', CustID=CustID)
#day_data = data_gatherer.get_day_data(Type='getconsumptionall', CustID='urQJ61oRG6ZiEgVpRlQo6L5AVUi1')

cleaned_data = cleanData(total_data)
df = cleaned_data.prepare_data()

st.write(df)

fig = cleaned_data.plot_data(df)
try:
    st.plotly_chart(fig)
except: st.write(f'No data to display')