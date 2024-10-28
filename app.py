import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from retrieveData import dataGather
import config

class cleanData:
    def __init__(self, data):
        self.data = data

    def prepare_data(self) -> pd.DataFrame:
        rows = []
        for date, readings in self.data.items():
            for reading in readings:
                if len(reading) == 2:
                    time_in_seconds, value = reading
                    time = pd.to_timedelta(float(time_in_seconds), unit='s')
                    rows.append({"date": date, "time": time, "reading": float(value)})  # Convert value to float
                else:
                    print(f'Skipping invalid reading format {reading}')
        return pd.DataFrame(rows)

    def plot_total_data(self, df):
        try:
            df['datetime'] = pd.to_datetime(df['date']) + df['time']
            fig = px.line(df, x='datetime', y='reading',
                          title='Total Readings Over Time',
                          labels={'datetime': 'Date and Time',
                                  'reading': 'Reading'},
                          markers=True)
            return fig
        except Exception as e:
            st.write(f'Error plotting total data: {e}')
            return go.Figure()  #return empty figure if error

    def plot_day_data(self, negative_one_df: pd.DataFrame) -> go.Figure:
        if negative_one_df.empty:
            return go.Figure()  #return an empty figure if no data

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=negative_one_df['date'],
            y=negative_one_df['reading'],
            mode='markers+lines',
            name='Readings'
        ))

        fig.update_layout(
            title="Day Data Readings",
            xaxis_title="Date",
            yaxis_title="Reading",
            hovermode='closest'
        )

        return fig

class DataApp:
    def __init__(self, data_gatherer):
        self.data_gatherer = data_gatherer

    def get_usernames(self) -> dict:
        usernames, _ = self.data_gatherer.get_clean_data(Type='getusers')
        return {name: id_ for name, id_ in usernames.items() if 'test' not in name.lower()}

    def select_user(self) -> str:
        usernames = self.get_usernames()
        selected_name = st.selectbox("Select a User", list(usernames.keys()))
        CustID = usernames[selected_name]
        return CustID

    def get_total_data(self, CustID) -> dict:
        cleaned_data, _ = self.data_gatherer.get_clean_data(Type='getconsumptionall', CustID=CustID)
        return cleaned_data

    def get_day_data(self, CustID: str) -> tuple:
        cleaned_data, negative_one_data = self.data_gatherer.get_day_data(Type='getconsumptionall', CustID=CustID)
        return cleaned_data, negative_one_data

    def prepare_and_plot_data(self, data: dict, negative_one_data: dict, data_type: str, CustID: str):
        cleaned_data = cleanData(data)
        df = cleaned_data.prepare_data()

        if data_type == "Day Data":
            negative_one_df = pd.DataFrame(negative_one_data.items(), columns=['date', 'reading'])
            negative_one_df['date'] = pd.to_datetime(negative_one_df['date'])
            negative_one_df['reading'] = negative_one_df['reading'].astype(float)

            st.dataframe(negative_one_df)

            if negative_one_df.empty:
                st.warning("No -1 readings available for the selected day.")
                return

            fig = cleaned_data.plot_day_data(negative_one_df)

            if isinstance(fig, go.Figure):
                st.plotly_chart(fig)
            else:
                st.error("Error: The figure could not be created.")

        elif data_type == "Total Data":
            st.dataframe(df)
            fig = cleaned_data.plot_total_data(df)
            st.plotly_chart(fig)

    def select_and_plot_data(self, CustID: str):
        data_type = st.selectbox("Select Data Type", ["Total Data", "Day Data"])

        if data_type == "Total Data":
            total_data = self.get_total_data(CustID)
            self.prepare_and_plot_data(total_data, {}, data_type="Total Data", CustID=CustID)
        elif data_type == "Day Data":
            day_data, negative_one_data = self.get_day_data(CustID)  # Fetch both datasets
            self.prepare_and_plot_data(day_data, negative_one_data, data_type="Day Data", CustID=CustID)

    def run(self):
        CustID = self.select_user()
        self.select_and_plot_data(CustID)

data_gatherer = dataGather(config.base_url)  # Assuming `config.base_url` is defined
app = DataApp(data_gatherer)
app.run()
