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
        #filter out -1 items
        cleaned_data = {}
        negative_one_data = {}

        if self.has_date_keys(data):
            for date, entries in data.items():
                #filter out '-1' entries and store them separately
                filtered_entries = []
                for entry in entries:
                    if entry[0] == '-1':
                        negative_one_data[date] = entry[1]
                    else:
                        filtered_entries.append(entry)
                cleaned_data[date] = [(self.convert_to_number(entry[0]),self.convert_to_number(entry[1])) for entry in filtered_entries]
            return cleaned_data, negative_one_data
        else:
            #print('Data does not have date keys -> returning raw data...')
            return data, {}

    def has_date_keys(self, data) ->bool:
        #checks if data coming in has dates or is another format (like user names)
        return all(self.is_date(key) for key in data.keys())

    def is_date(self, string) -> bool:
        #check if a date is in the keys of dict to decide how to process data
        try:
            pd.to_datetime(string)
            return True
        except Exception:
            return False

    def convert_to_number(self, s):
        #convert item to int or float if available
        try:
            return int(s)
        except ValueError:
            try:
                return float(s)
            except ValueError:
                return(s)

    def get_total_data(self, **kwargs) -> dict:
        #get all data for a user
        return self.fetch_data(**kwargs)

    def get_clean_data(self, **kwargs):
        data = self.get_total_data(**kwargs)
        return self.clean_data(data) #only cleans if there are date keys detected

    def get_day_data(self, **kwargs) -> dict:
        # Get the total data for a user (the -1 value)
        total_data = self.get_total_data(**kwargs)
        print(total_data)

        # Create a dictionary to store -1 values with dates {date: ounces}
        negative_one_data = {}
        cleaned_entries = {}
        debug_list = []

        for date, entries in total_data.items():
            filtered_entries = []
            for entry in entries:
                if entry[0] == '-1':
                    negative_one_data[date] = entry[1]
                    debug_list.append(f"Found -1 for date {date}: {entry[1]}")
                else:
                    filtered_entries.append(entry)

            cleaned_entries[date] = filtered_entries
        #print(debug_list)

        return cleaned_entries, negative_one_data

    def get_users(self, **kwargs):
        return self.fetch_data(**kwargs)

#response_data1 = get_data(Type='getnextserial')
#data_gatherer = dataGather(config.base_url)
#total_data = data_gatherer.get_total_data(Type='getconsumptionall', CustID='urQJ61oRG6ZiEgVpRlQo6L5AVUi1')
#day_data = data_gatherer.get_day_data(Type='getconsumptionall', CustID='urQJ61oRG6ZiEgVpRlQo6L5AVUi1')
#clean_data = data_gatherer.get_clean_data(Type='getconsumptionall', CustID='urQJ61oRG6ZiEgVpRlQo6L5AVUi1')

#sponge_users = data_gatherer.get_clean_data(Type='getusers')

#print(day_data)
