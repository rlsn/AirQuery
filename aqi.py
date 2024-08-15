# Copyright (c) 2023 rlsn
#
import requests
import sys, argparse

# get your token at https://aqicn.org/api/
# and replace mine here
token="9c123e8db864c46190c95b2479c64c83127f7040"

API="http://api.waqi.info/feed/{}/?token={}"

cities=["tokyo", "beijing"]
plot_forcast = False

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def colorize(aqi, width=10):
    color = bcolors.OKGREEN
    if aqi<50:
        color = bcolors.OKGREEN
    elif aqi<100:
        color = bcolors.WARNING
    elif aqi<150:
        color = bcolors.HEADER
    elif aqi<200:
        color = bcolors.HEADER
    elif aqi<300:
        color = bcolors.FAIL
    else:
        color = bcolors.FAIL

    return ' '*(width-len(str(aqi))) + color + str(aqi) + bcolors.ENDC

def classify(aqi):
    if aqi<50:
        return bcolors.OKGREEN+"Good"+bcolors.ENDC
    elif aqi<100:
        return bcolors.WARNING+"Moderate"+bcolors.ENDC
    elif aqi<150:
        return bcolors.HEADER+"Unhealthy for Sensitive"+bcolors.ENDC
    elif aqi<200:
        return bcolors.HEADER+"Unhealthy"+bcolors.ENDC
    elif aqi<300:
        return bcolors.FAIL+"Very Unhealthy"+bcolors.ENDC
    else:
        return bcolors.FAIL+"Harzadous"+bcolors.ENDC

def print_aqi(data):
    for city in data:
        aqi=data[city]['aqi']
        iaqi=data[city]['iaqi']
        print("city:",city)
        print("AQI:",aqi,classify(aqi))
        print("pm2.5:",iaqi['pm25']['v'], classify(iaqi['pm25']['v']))
        print("pm10:",iaqi['pm10']['v'], classify(iaqi['pm10']['v']))   

def print_table(data):
    print("-"*55)
    print(f"|{'city':^20}|{'AQI':^10}|{'PM2.5':^10}|{'PM10':^10}|")
    print("-"*55)

    cities = sorted(data.keys(), key=lambda x:data[x]['aqi'])
    for city in cities:
        aqi=data[city]['aqi']
        iaqi=data[city]['iaqi']
        print(f"|{city:^20}|{colorize(aqi,10)}|{colorize(iaqi['pm25']['v'],10)}|{colorize(iaqi['pm10']['v'],10)}|")
    print("-"*55)


if __name__=="__main__":
    if len(sys.argv)>1:
        cities.extend(sys.argv[1].split(","))

    data = dict()

    for city in cities:
        URL = API.format(city,token)
        re=requests.get(URL)
        if re.status_code!=200:
            print(f"failed at {URL}: {re}")
            continue
        
        data[city] = re.json()['data']
    
    if len(data)>1:
        print_table(data)
    else:
        print_aqi(data)
    if plot_forcast:
        from plot import plot
        plot(data)
        

