import requests
from io import StringIO
import pandas as pd
import plotly.express as px

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

    def draw_graph(self):
        pass
