import requests
from io import StringIO
import pandas as pd
import plotly.express as px
import config
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

lay = Layout(
    plot_bgcolor="rgb(214, 213, 197)",
    paper_bgcolor="rgb(214, 213, 197)"
)


class DataPrepperWasserportal:
    def __init__(self, base):
        self.base = base

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
        fig.update_layout(template="simple_white")
        fig.layout.plot_bgcolor = "#d6d5c5"
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
    key = config.key
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
