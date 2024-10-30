'''
Retrieve data from the db with this
'''
#TODO: Add data pulling down, we want to pull down all of db data.  May need
# to add function to API to facilitate this...

#import config
import requests
import pandas as pd

class dataGather:
    def __init__(self, APIurl):
        self.APIurl = APIurl

    def fetch_data(self, **kwargs) -> dict:
        response = requests.get(self.APIurl, params=kwargs)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def clean_data(self, data) -> dict:
        cleaned_data = {}
        negative_one_data = {}

        if self.has_date_keys(data):
            for date, entries in data.items():
                filtered_entries = []
                for entry in entries:
                    if entry[0] == '-1':
                        negative_one_data[date] = entry[1]
                    else:
                        filtered_entries.append(entry)
                cleaned_data[date] = [(self.convert_to_number(entry[0]), self.convert_to_number(entry[1])) for entry in filtered_entries]
            return cleaned_data, negative_one_data
        else:
            return data, {}

    def has_date_keys(self, data) -> bool:
        return all(self.is_date(key) for key in data.keys())

    def is_date(self, string) -> bool:
        try:
            pd.to_datetime(string)
            return True
        except Exception:
            return False

    def convert_to_number(self, s):
        try:
            return int(s)
        except ValueError:
            try:
                return float(s)
            except ValueError:
                return s

    def get_total_data(self, **kwargs) -> dict:
        return self.fetch_data(**kwargs)

    def get_clean_data(self, **kwargs):
        data = self.get_total_data(**kwargs)
        return self.clean_data(data)

    def get_day_data(self, **kwargs) -> dict:
        total_data = self.get_total_data(**kwargs)
        return self.clean_data(total_data)

    def get_users(self, **kwargs):
        return self.fetch_data(**kwargs)

    def get_dates(self, **kwargs):
        return self.fetch_data(**kwargs)

    def get_filtered_date_data(self, CustID: str, start_date: str, end_date: str) -> dict:
        filtered_data = self.fetch_data(Type='getfiltereddates', CustID=CustID, DateOne=start_date, DateTwo=end_date)
        return self.clean_data(filtered_data)

#response_data1 = get_data(Type='getnextserial')
#data_gatherer = dataGather(config.base_url)
#total_data = data_gatherer.get_total_data(Type='getconsumptionall', CustID='urQJ61oRG6ZiEgVpRlQo6L5AVUi1')
#day_data = data_gatherer.get_day_data(Type='getconsumptionall', CustID='urQJ61oRG6ZiEgVpRlQo6L5AVUi1')
#clean_data = data_gatherer.get_clean_data(Type='getconsumptionall', CustID='urQJ61oRG6ZiEgVpRlQo6L5AVUi1')

#sponge_users = data_gatherer.get_clean_data(Type='getusers')

#print(day_data)
