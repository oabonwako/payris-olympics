import numpy as np
import pandas as pd
import random
from random import randint, choice
import sys
import faker
from datetime import date, timedelta
import os
os.environ['TZ'] = 'Asia/Kolkata'
fak = faker.Faker()

sdate = date(2019,1,1)   # start date
edate = date(2024,12,31)   # end date

def dates_bwn_twodates(start_date, end_date):
    fut_dates = np.arange(sdate, edate, dtype="datetime64[D]")
    date_lists = [dt.strftime("%Y-%m-%d") for dt in pd.to_datetime(fut_dates)]
    return date_lists

def random_values():
    view = random.randint(1,1440)
    Ad_rev = random.randint(50,5000)
    session = random.randint(1,5000)
    return view,Ad_rev,session

dictionary = {'request': ['GET', 'POST', 'PUT'], 'endpoint': ['/usr', '/usr/login', '/usr/register'], 'statuscode': [
    '303', '404', '500', '403', '202', '304','200'], 'country': ['India','South Africa', 'Poland', 'Saudia Arabia','Sweden','Mexico','Malaysia','Russia','Turkey','Australia','Brazil','Spain',
    'Colombia','United States','China','Peru','Netherlands','Argentina','Italy','Britain','Canada','Germany','Hungary','Chile','France','Japan','South Korea','Belgium','Botswana'],
    'device_type': ['mobile','laptop','tablet','Desktop'], 'browser_type': ['FireFox','Edge','Chrome','Explorer','Safari','Opera'],'sports_event': ['Basketball','Athletics','Boxing','Badminton','Archery','Golf','Hockey', 'Skateboard','Swimming', 'Football','Equastrian','Tennis','Surfing','Volleyball','Wrestling','Weightlifting'],
            'traffic_source': ['organic search','twitter','Facebook','Youtube','Instagram','direct'],
            'interaction_type': ['likes','comment','share','no interaction']}

f = open("websitelog.csv","w")
for _ in range(1,100001):
    f.write('%s,%s,"%s %s HTTP/1.0",%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n' %
        (fak.ipv4(),
         choice(dates_bwn_twodates(sdate,edate)),
         choice(dictionary['request']),
         choice(dictionary['endpoint']),
         choice(dictionary['statuscode']),
         choice(dictionary['sports_event']),
         choice(dictionary['interaction_type']),
         random_values()[0],
         random_values()[1],
         random_values()[2],
         choice(dictionary['country']),
         choice(dictionary['traffic_source']),
         choice(dictionary['device_type']),
         choice(dictionary['browser_type']),
         random.randint(1,1000),
         random.randint(1,5000)))

f.close()