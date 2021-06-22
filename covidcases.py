from bs4.element import SoupStrainer
import requests
from bs4 import BeautifulSoup
import re
import time
from requests import api
from db.mysql_connection import *
from uk_covid19 import Cov19API
import json
from requests import get
from json import dumps
import datetime

#Get coventry daily postive cases and date 
#@Author: Han Wang
# todo - collect other covid related data - stored in number array - cross reference with web page

yes_time=str(datetime.date.today() - datetime.timedelta(days=1))
def coventry_states(time=yes_time):
    coventry_only = [
        'areaName=Coventry',
        f'date={time}'
    ]
    covid_states = {
        "date":"date",
        "dailycases":"newCasesBySpecimenDate",
        "cumulativecases":"cumCasesBySpecimenDate",
        "dailydeaths":"newDeaths28DaysByDeathDate",
        "cumulativedeaths":"cumDeaths28DaysByDeathDate"
    }
    
    api = Cov19API(filters=coventry_only, structure=covid_states,latest_by="newCasesByPublishDate")
    data = api.get_json()['data'][0]
   
    dt=data['date']
    dailycases=data['dailycases']
    cumulativecases=data['cumulativecases']
    dailydeaths=data['dailydeaths']
    cumulativedeaths=data['cumulativedeaths']
    
    query = "INSERT INTO coventrycovid(dt,dailycases,cumulativecases,dailydeaths,cumulativedeaths) VALUES(%s,%s,%s,%s,%s)"
    params = [(dt,dailycases,cumulativecases,dailydeaths,cumulativedeaths)]
    
    
    res = mysql_add(query, params)
    if res == 0:
        print("Failed to add coventry covid to database")
    else:
        print("sucessuflly")

    return data
   

def national_states(time=yes_time):
    


    national = [
        "areaType=overview",
        'areaName=United Kingdom',
        f'date={time}'
    ]


    covid_states = {
            "date": "date",
            "dailycases":"newCasesBySpecimenDate",
            "cumulativecases":"cumCasesByPublishDate",
            "dailydeaths":"newDeaths28DaysByDeathDate",
            "cumulativedeaths":"cumDeaths28DaysByDeathDate",
            "dailytests":"newTestsByPublishDate",
            "cumulativetests":"cumTestsByPublishDate",
            "dailyvaccination":"newPeopleVaccinatedFirstDoseByPublishDate",
            "cumulativevaccination":"cumPeopleVaccinatedFirstDoseByPublishDate"

    }


    api = Cov19API(filters=national, structure=covid_states,latest_by="newCasesByPublishDate")

    data = api.get_json()['data'][0]

    print(data)
    dt=data['date']
    dailycases=data['dailycases']
    cumulativecases=data['cumulativecases']
    dailydeaths=data['dailydeaths']
    cumulativedeaths=data['cumulativedeaths']
    dailytests=data['dailytests']
    cumulativetests=data['cumulativetests']
    dailyvaccination=data['dailyvaccination']
    cumulativevaccination=data['cumulativevaccination']

    query = "INSERT INTO ukcovid(dt,dailycases,cumulativecases,dailydeaths,cumulativedeaths,dailytests,cumulativetests,dailyvaccination,cumulativevaccination) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    params = [(dt,dailycases,cumulativecases,dailydeaths,cumulativedeaths,dailytests,cumulativetests,dailyvaccination,cumulativevaccination)]

    res = mysql_add(query, params)
    if res == 0:
        print("Failed to add coventry covid to database")
    else:
        print("sucessuflly")
   
    return data


def get_covid_cases():

    res = requests.get('https://coronavirus.data.gov.uk/search?postcode=CV1+1AH')
    html = res.content
    soup = BeautifulSoup(html, 'html.parser')
    cases = soup.find('a', attrs={'class': 'govuk-link--no-visited-state number-link number'})
    daily_date = soup.find('p', attrs={'class': "govuk-body-s"})

    last7days = soup.find('a', attrs={'class':"govuk-link--no-visited-state number-link"}).get_text()
    last7= last7days.split(" ",1)[0]
    last7detail=last7days.split(" ",1)[1]

    date = daily_date.contents[1]['datetime']
    text = cases.get_text()

    number = re.findall(r"\d+\.?\d*", text)
    timestamp = time.mktime(time.strptime(date[:date.find('.')], "%Y-%m-%dT%H:%M:%S"))
    time_local = time.localtime(timestamp)
   
   
    dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
    cases =  number[0]
    print(f"Today is {dt} , Coventry Daily postive case: {number[0]}, Have a nice day, keep safe!")
    return dt, cases
# todo - add validation to check same day not added twice
# todo - add checks on return


# def add_cases():
#     '''
#     Function to add daily covid cases to database.
#     '''
#     print("added cases")
#     dt,dailycases,cumulativecases,dailydeaths,cumulativedeaths = coventry_states()
#     query = "INSERT INTO coventrycovid(dt,dailycases,cumulativecases,dailydeaths,cumulativedeaths) VALUES(%s,%s,%s,%s,%s)"
#     params = [(dt,dailycases,cumulativecases,dailydeaths,cumulativedeaths)]
#     mysql_add(query, params)
#     return "yay"

