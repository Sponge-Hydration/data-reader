import streamlit as st
import polars as pl
from retrieveData import data_gatherer
#import config

#st.write("Hello world")

total_data = data_gatherer.get_total_data(Type='getconsumptionall', CustID='urQJ61oRG6ZiEgVpRlQo6L5AVUi1')
flattened_data = [(date, entry[0], entry[1]) for date, entries in total_data.items() for entry in entries if entry[0] != -1]
df_notDays = pl.DataFrame(flattened_data, schema=["date", "ID", "value"])

st.write("notDays:", df_notDays)

#TODO: make graphs
df_filteredDays = df_notDays.filter(pl.col("value") != -1.0)
df_days = df_notDays.filter(pl.col("value") == -1.0)

st.write("Filtered Days:", df_filteredDays)
st.write("Days with -1 values:", df_days)