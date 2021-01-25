import dash
import dash_html_components as html
import dash_core_components as dcc
from DataPrepper import DataPrepperWasserportal, DataPrepperWeather

measurement = "td"
stationid = "5865900"
from_when = "25.01.2021"

weather_widget = """<a class="weatherwidget-io" href="https://forecast7.com/en/52d5413d50/13055/" data-label_1="Berlin" data-label_2="13055" data-font="Roboto Slab" data-icons="Climacons Animated" data-days="3" data-theme="original" data-basecolor="#406682" >13055 13055</a>
<script>
!function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0];if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src='https://weatherwidget.io/js/widget.min.js';fjs.parentNode.insertBefore(js,fjs);}}(document,'script','weatherwidget-io-js');
</script>
"""


dp_water = DataPrepperWasserportal("https://wasserportal.berlin.de/station.php?")
dp_weather = DataPrepperWeather()

app = dash.Dash(__name__, external_stylesheets=["https://codepen.io/chriddyp/pen/bWLwgP.css"], meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ])


app.layout = html.Div(style={"background-color": "#d6d5c5"}, children=[
    #html.H4("Monitor"),
    #html.Div("Your latest Graphs"),
    html.Iframe(srcDoc=weather_widget),

    dcc.Dropdown(
        id="water",
        options=[
            {'label': 'New York City', 'value': 'NYC'},
            {'label': 'Montreal', 'value': 'MTL'},
            {'label': 'San Francisco', 'value': 'SF'}
        ]
    ),

    html.Div([
        html.Div("0 °C", className="block"),

        html.Div("12 m", className="block"),

        html.Div("14k m/h", className="block")
    ]),

    dcc.Graph(
        id="graph1",
        figure=dp_water.get_single_data(measurement, stationid, from_when),
        style={"background-color": "#d6d5c5"}
    ),

    html.Div([
        html.Div("pH", className="block"),

        html.Div("O2", className="block"),

        html.Div("50%", className="block")
    ]),


    dcc.Graph(
        id="graph2",
        figure=dp_water.get_single_data("wd", stationid, from_when)
    )
])


if __name__ == "__main__":
    app.run_server(port=5000, debug=True)