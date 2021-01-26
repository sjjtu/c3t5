import dash
import dash_html_components as html
import dash_core_components as dcc
from DataPrepper import DataPrepperWasserportal, DataPrepperWeather, get_all_stations

measurement = "td"
stationid = "5865900"
from_when = "26.01.2021"

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

    html.Div([
        html.H4(html.B("Your graphs for", style={"font-family": "Roboto Slab", "text-align": "central"})),

        dcc.Dropdown(
            id="water",
            options= get_all_stations()
        )

    ]),



    html.Div([
        html.Div([html.P("TEMP",  style={"color":"#a1f57a", "font-family": "Roboto Slab"}, className="blink_me"), html.P("0 °C", id="temp")], className="block"),

        html.Div([html.P("WATER LEVEL", style={"color":"#a1f57a", "font-family": "Roboto Slab"}, className="blink_me"), html.P("12 m", id="wl")], className="block"),

        html.Div([html.P("FLOW", style={"color":"#a1f57a", "font-family": "Roboto Slab"}, className="blink_me"), html.P("12 m³/s", id="flow")], className="block")
    ], className="Row"),

    html.Div([html.Div(
        dcc.Graph(
            id="graph1",
            config={"displayModeBar": False},
            figure=dp_water.get_single_data(measurement, stationid, from_when)
        ), className="graph"

    )]),


    html.Div([
        html.Div([html.P("pH", style={"color": "#a1f57a", "font-family": "Roboto Slab"}, className="blink_me"), html.P("7", id="ph")], className="block", style={"width": "20%"}),

        html.Div([html.P("O2", style={"color": "#a1f57a", "font-family": "Roboto Slab"}, className="blink_me"), html.P("4 mg/l", id="o2")], className="block", style={"width": "25%"}),

        html.Div([html.P("O2 sat", style={"color":"#a1f57a", "font-family": "Roboto Slab"}, className="blink_me"), html.P("12%", id="o2_sat")], className="block", style={"width": "20%"})
    ]),

    html.Div(
        dcc.Graph(
            id = "graph2",
            figure=dp_water.get_single_data("wd", stationid, from_when),
            style={"height": "50%", "width": "100%"},
            config={"displayModeBar": False}
        ), className="graph"

    )

])


@app.callback(
        dash.dependencies.Output("graph1", "figure"),
        dash.dependencies.Input("water", "value")
)
def update_graph(id):
    return dp_water.get_single_data("td", id, from_when)


@app.callback(
        dash.dependencies.Output("graph2", "figure"),
        dash.dependencies.Input("water", "value")
)
def update_graph(id):
    return dp_water.get_single_data("wd", id, from_when)


@app.callback(
        dash.dependencies.Output("temp", "children"),
        dash.dependencies.Input("water", "value")
)
def update_val(id):
    return str(dp_water.return_recent_data("td", id, from_when)) + " °C"


@app.callback(
        dash.dependencies.Output("wl", "children"),
        dash.dependencies.Input("water", "value")
)
def update_val(id):
    return str(dp_water.return_recent_data("wd", id, from_when)) + " m"


@app.callback(
        dash.dependencies.Output("ph", "children"),
        dash.dependencies.Input("water", "value")
)
def update_val(id):
    return dp_water.return_recent_data("pd", id, from_when)


@app.callback(
        dash.dependencies.Output("o2", "children"),
        dash.dependencies.Input("water", "value")
)
def update_val(id):
    return str(dp_water.return_recent_data("od", id, from_when)) + " mg/L"


@app.callback(
        dash.dependencies.Output("o2_sat", "children"),
        dash.dependencies.Input("water", "value")
)
def update_val(id):
    return str(dp_water.return_recent_data("dd", id, from_when)) + " %"


@app.callback(
        dash.dependencies.Output("flow", "children"),
        dash.dependencies.Input("water", "value")
)
def update_val(id):
    return str(dp_water.return_recent_data("ld", id, from_when)/1000) + " m³/s"



if __name__ == "__main__":
    app.run_server(port=5000, debug=True)