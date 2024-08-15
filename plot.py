import matplotlib.pyplot as plt
import seaborn as sns # pip install seaborn
sns.set_theme()

def plot(data):
    for city in data:
        forecast = data[city]['forecast']['daily']
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
        axs.set_title(f"AQI forecast {city}")

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

        print("Ploting forecast")
        fig.show()
    input("press enter to quit.")