import requests
from io import StringIO
import pandas as pd
import plotly.express as px
#import config
from plotly.graph_objs import *

abbr = {"wd": "Water Level",
        "td": "Temperature",
        "dd": "Flow meter",
        "ld": "Conductivity",
        "pd": "pH",
        "od": "Oxygen content",
        "sd": "Oxygen saturation"}


def find_outlier_indicator(raw):
    k = len("Fehlwerte: ")
    start = raw.find("Fehlwerte: ")+k
    end = raw[start:].find("\"")
    return int(raw[start:end+start])


def remove_outliers(indicator, df, col):
    df = df[df[col] != float(indicator)]
    return df[df[col] != indicator]


def get_all_stations():
    df = pd.read_csv("station.csv", header=None, encoding="windows-1252")
    df.rename(columns={0: "id", 1: "name"}, inplace=True)
    df.drop_duplicates(inplace=True)
    l = []
    for index, row in df.iterrows():
        l.append({"label": row["name"], "value": row.id})
    return l


class DataPrepperWasserportal:
    def __init__(self, base):
        self.base = base

    def return_recent_data(self, measurement, stationid, from_when, out_format="c"):
        url = f"{self.base}anzeige={measurement}&sstation={stationid}&sreihe=w&smode={out_format}&sdatum={from_when}"
        r = requests.get(url, allow_redirects=True)
        data = r.content.decode("windows-1252")
        df = pd.read_csv(StringIO(data), sep=";", decimal=",")
        df.Datum = pd.to_datetime(df['Datum'], format="%d.%m.%Y %H:%M")
        df.rename(columns={"Einzelwert": abbr[measurement]}, inplace=True)
        df[abbr[measurement]].astype(float)
        indic = find_outlier_indicator(data)
        df = remove_outliers(indic, df, abbr[measurement])
        return df[abbr[measurement]].iloc[-1]

    def get_single_data(self, measurement, stationid, from_when, out_format="c"):
        url = f"{self.base}anzeige={measurement}&sstation={stationid}&sreihe=w&smode={out_format}&sdatum={from_when}"
        r = requests.get(url, allow_redirects=True)
        data = r.content.decode("windows-1252")
        df = pd.read_csv(StringIO(data), sep=";", decimal=",")
        df.Datum = pd.to_datetime(df['Datum'], format="%d.%m.%Y %H:%M")
        df.rename(columns={"Einzelwert": abbr[measurement]}, inplace=True)
        df[abbr[measurement]].astype(float)
        indic = find_outlier_indicator(data)
        df = remove_outliers(indic, df, abbr[measurement])

        fig = px.line(df, x="Datum", y=abbr[measurement], title=abbr[measurement])
        fig.update_layout(height=200, margin=dict(t=30, r=0, l=0, b=30))
        fig.update_yaxes(title="")
        fig.layout.plot_bgcolor = "#83daec"
        fig.layout.yaxis.gridcolor = "#ffffff"
        fig.layout.xaxis.gridcolor = "#ffffff"
        fig.layout.paper_bgcolor = "#83daec"
        fig.layout.font.color = "black"
        fig.update_traces({"line": {"color": "black"}})
        return fig

    def get_daily_data(self, measurement, stationid, from_when, out_format="c"):
        url = f"{self.base}anzeige={measurement}&sstation={stationid}&sreihe=m&smode={out_format}&sdatum={from_when}"
        r = requests.get(url, allow_redirects=True)
        data = r.content.decode("windows-1252")
        df = pd.read_csv(StringIO(data), sep=";")
        return df

    def get_monthly_data(self, measurement, stationid, from_when, out_format="c"):
        url = f"{self.base}anzeige={measurement}&sstation={stationid}&sreihe=j&smode={out_format}&sdatum={from_when}"
        r = requests.get(url, allow_redirects=True)
        data = r.content.decode("windows-1252")
        df = pd.read_csv(StringIO(data), sep=";")
        return df


class DataPrepperWeather:
    key = "config.key"
    base_cur = f"https://api.openweathermap.org/data/2.5/weather?appid={key}"
    base_fore = f"pro.openweathermap.org/data/2.5/forecast/hourly?appid={key}"

    def get_data(self, zip):
        curr = requests.get(self.base_cur + f"&zip={zip},de").json()
        fore = requests.get(self.base_fore + f"zip{zip},de").json()
        temp_curr = curr["main"]["temp"]
        temp_fore = fore["list"]["main"]["temp"]
        rain_last1 = curr["rain"] if "rain" in curr else 0
        prob_prec = fore["list"]["pop"] if "pop" in fore["list"] else 0
        return{
            "temp_curr": temp_curr,
            "rain_last1": rain_last1,
            "temp_fore": temp_fore,
            "prob_prec": prob_prec
        }
