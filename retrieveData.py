'''
Retrieve data from the db with this
'''
#TODO: Add data pulling down, we want to pull down all of db data.  May need
# to add function to API to facilitate this...

import config
import requests

class dataGather:
    def __init__(self, APIurl):
        self.APIurl = APIurl
    def get_data(self, **kwargs) -> dict:
        #TODO: get the data for all a user
        response = requests.get(self.APIurl, params=kwargs)

        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

#response_data1 = get_data(Type='getnextserial')
data_gatherer = dataGather(config.base_url)
response_data2 = data_gatherer.get_data(Type='getconsumptionall', CustID='urQJ61oRG6ZiEgVpRlQo6L5AVUi1')
print(response_data2)
