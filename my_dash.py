import dash
import dash_html_components as html
import dash_core_components as dcc
from DataPrepper import DataPrepperWasserportal

measurement = "td"
stationid = "5865900"
from_when = "25.01.2021"

dp = DataPrepperWasserportal("https://wasserportal.berlin.de/station.php?")

app = dash.Dash(__name__, external_stylesheets=["https://codepen.io/chriddyp/pen/bWLwgP.css"])
app.layout = html.Div(style={'backgroundColor': "#2596be"}, children=[
    html.H4("Monitor"),
    html.Div("Your latest Graphs"),
    dcc.Graph(
        id="graph1",
        figure=dp.get_single_data(measurement, stationid, from_when)
    )
])


if __name__ == "__main__":
    app.run_server(port=5000, debug=True)