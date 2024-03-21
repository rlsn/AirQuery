# Copyright (c) 2023 rlsn
#
# !pip install seaborn
import requests
import sys, argparse
import matplotlib.pyplot as plt
import seaborn as sns # pip install seaborn
sns.set_theme()

# get your token at https://aqicn.org/api/
# and replace mine here
token="9c123e8db864c46190c95b2479c64c83127f7040"

API="http://api.waqi.info/feed/{}/?token={}"

city="tokyo"
if len(sys.argv)>1:
    city=sys.argv[1]

URL = API.format(city,token)

re=requests.get(URL)

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

def print_aqi(re):

    data = re['data']
    aqi=data['aqi']
    iaqi=data['iaqi']
    print("city:",city)
    print("AQI:",aqi,classify(aqi))
    print("pm2.5:",iaqi['pm25']['v'],classify(iaqi['pm25']['v']))
    print("pm10:",iaqi['pm10']['v'],classify(iaqi['pm10']['v']))

    forecast=data['forecast']['daily']
    del forecast['o3']
    del forecast['uvi']

    fig, axs = plt.subplots(1, 1, figsize=(8,6))
    x = [d['day'][5:] for d in forecast['pm10']]
    pm10 = [[d['avg'],d['max'],d['min']] for d in forecast['pm10']]
    pm25 = [[d['avg'],d['max'],d['min']] for d in forecast['pm25']]
    avg = [max(d10[0],d25[0]) for d10, d25 in zip(pm10,pm25)]
    maxi = [max(d10[1],d25[1]) for d10, d25 in zip(pm10,pm25)]
    mini = [max(d10[2],d25[2]) for d10, d25 in zip(pm10,pm25)]

    axs.fill_between(x, maxi, mini, alpha=.5, linewidth=0)
    axs.plot(x,avg,marker='o',label="avg")
    axs.set_xlabel('date')
    axs.set_ylabel('AQI')
    axs.legend()
    # axs.xaxis.set_tick_params(rotation=-15)
    axs.set_title("AQI forecast")

    def colorize(v):
        if v<50:
            return ("dimgrey","limegreen")
        elif v<100:
            return ("dimgrey","yellow")
        elif v<150:
            return ("dimgrey","darkorange")
        elif v<200:
            return ("lightgrey","orangered")
        elif v<300:
            return ("lightgrey","blueviolet")
        else:
            return ("lightgrey","maroon")

    for i in range(len(x)):
        axs.text(x[i], avg[i], avg[i], size=9, 
            backgroundcolor=colorize(avg[i])[0],color=colorize(avg[i])[1])
        axs.text(x[i], maxi[i], maxi[i], size=9, 
            backgroundcolor=colorize(maxi[i])[0],color=colorize(maxi[i])[1])
        axs.text(x[i], mini[i], mini[i], size=9, 
            backgroundcolor=colorize(mini[i])[0],color=colorize(mini[i])[1])



if re.status_code==200:
    print_aqi(re.json())
else:
    print(re)

print("Displaying forecast")
plt.show()

