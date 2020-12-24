import requests
import json

import pandas as pd
from datetime import datetime, date, timedelta

from secrets import client_id, client_secret, venue_group_id
from emails import CompletionEmail, ErrorEmail


class SevenRoomsAPI:
    
    def __init__(self,pages,start_date):
        
        self.pages = pages
        self.start_date = start_date
        self.start = datetime.now()
        
        self.token = self.get_token()
        self.venue_ids = self.get_venue_ids()
        self.reservations = self.get_reservations()
        
    def get_token(self):
        
        url = "https://api.sevenrooms.com/2_2/auth"
        headers = {'Content-type': 'application/json'}
        
        parameters = {
            "client_id": client_id,
            "client_secret": client_secret
        }
        
        r = requests.post(
            url,
            headers=headers,
            params=parameters
        )

        return r.json()['data']['token']
    
    def get_venue_ids(self):
        
        url = "https://api.sevenrooms.com/2_2/venues"
        headers = {'authorization': self.token}
        
        parameters = {
            'venue_group_id' : venue_group_id,
            'limit':100
        }
        
        r = requests.get(
            url,
            headers=headers,
            params=parameters
        )
        
        restaurant_ids = pd.DataFrame(r.json()["data"]["results"])[["id","name"]]
        restaurant_ids.columns = ["venue_id","restaurant"]

        return restaurant_ids
    
    def get_reservations(self):
        
        headers = {'authorization': self.token}
        url = "https://api.sevenrooms.com/2_2/reservations/export" 

        page = 1
        log = ['Start']
        reservations=''

        while page <= self.pages:

            log.append("Requesting page " + str(page) + ". Duration so far: " + str(datetime.now()-self.start))

            if page==1:
                
                # On the first page of results, retrieve the cursor to use in subsequent requests & initiate the reservations dataframe from the results

                reservations_count = 0    
                
                response = requests.get(
                    url, 
                    headers=headers,
                    params={
                        'venue_group_id' : venue_group_id,
                        'from_date' : self.start_date,
                        'limit' : 400
                    }
                )
                

                if response.status_code != 200:
                    
                    cursor = 'Uninitiated'
                    error_text = str(response.text)
                    
                    log.append(error_text)
                    ErrorEmail(page, reservations_count, error_text, cursor, log, self.start).send()
                    
                    page = 1
                    
                else:
                    
                    cursor = response.json()['data']['cursor']
                    reservations = pd.DataFrame(response.json()['data']['results'])
                    
                    page += 1

            else:
                
                reservations_count = reservations["id"].count()

                response = requests.get(
                    url, 
                    headers=headers,
                    params={
                        'venue_group_id' : venue_group_id,
                        'from_date' : self.start_date,
                        'limit' : 400,
                        'cursor' : cursor
                    }
                )
                
                if response.status_code != 200:
                    
                    error_text = str(response.text)
                    
                    log.append(error_text)
                    ErrorEmail(page, reservations_count, error_text, cursor, log, self.start).send()
                    
                    page = 1

                if response.json()['data']['results'] == []:

                    log.append("Zero results on page " + str(page) + " at " + str(date))

                    page += 1 

                else:

                    df = pd.DataFrame(response.json()['data']['results'])
                    reservations = reservations.append(df, ignore_index=True)

                    page += 1
 
        reservations_count = reservations["id"].count()
        CompletionEmail(page, reservations_count, cursor, log, self.start).send()
        
        return reservations
