import dash
import dash_html_components as html
import dash_core_components as dcc
from DataPrepper import DataPrepperWasserportal, DataPrepperWeather

measurement = "td"
stationid = "5865900"
from_when = "25.01.2021"

weahter_widget = """<a class="weatherwidget-io" href="https://forecast7.com/en/52d5413d50/13055/" data-label_1="Berlin" data-label_2="13055" data-font="Roboto" data-icons="Climacons Animated" data-days="3" data-theme="blue-mountains" >Berlin 13055</a>
<script>
!function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0];if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src='https://weatherwidget.io/js/widget.min.js';fjs.parentNode.insertBefore(js,fjs);}}(document,'script','weatherwidget-io-js');
</script>
"""


dp_water = DataPrepperWasserportal("https://wasserportal.berlin.de/station.php?")
dp_weather = DataPrepperWeather()

app = dash.Dash(__name__, external_stylesheets=["https://codepen.io/chriddyp/pen/bWLwgP.css"], meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ])
app.layout = html.Div(style={}, children=[
    #html.H4("Monitor"),
    #html.Div("Your latest Graphs"),
    html.Iframe(srcDoc=weahter_widget, height=400, style={"frameborder":0}),
    dcc.Graph(
        id="graph1",
        figure=dp_water.get_single_data(measurement, stationid, from_when)
    ),
    dcc.Graph(
        id="graph2",
        figure=dp_water.get_single_data("wd", stationid, from_when)
    )
])


if __name__ == "__main__":
    app.run_server(port=5000, debug=True)