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


app.layout = html.Div(style={"background-color": "white", "background-size": "contain"}, children=[
    #html.H4("Monitor"),
    #html.Div("Your latest Graphs"),
    html.Div(style={"height":"50px"}),
    html.Iframe(srcDoc=weather_widget),

    html.Div([
        html.H4(html.B("Your graphs for", style={"font-family": "Roboto Slab", "text-align": "central"})),

        dcc.Dropdown(
            id="water",
            options= get_all_stations()
        )

    ]),

    #html.Button("Open Card 1", id="button1"),
    html.Div([
        html.Div([
            html.Div([html.P("TEMP", style={"color": "#006300", "font-family": "Roboto Slab"}, className="blink_me"),
                      html.P("0 °C", id="temp")], className="block"),

            html.Div(
                [html.P("WATER LEVEL", style={"color": "#006300", "font-family": "Roboto Slab"}, className="blink_me"),
                 html.P("12 m", id="wl")], className="block"),

            html.Div([html.P("FLOW", style={"color": "#006300", "font-family": "Roboto Slab"}, className="blink_me"),
                      html.P("12 m³/s", id="flow")], className="block")
        ], className="Row"),


        html.Div([

            html.Div(
            dcc.Graph(
                id="graph1",
                config={"displayModeBar": False},
                figure=dp_water.get_single_data(measurement, stationid, from_when)
            ), className="graph"

        )]),

        html.Div([
            html.Div([html.P("pH", style={"color": "#006300", "font-family": "Roboto Slab"}, className="blink_me"),
                      html.P("7", id="ph")], className="block", style={"width": "20%"}),

            html.Div([html.P("O2", style={"color": "#006300", "font-family": "Roboto Slab"}, className="blink_me"),
                      html.P("4 mg/l", id="o2")], className="block", style={"width": "25%"}),

            html.Div([html.P("O2 sat", style={"color": "#006300", "font-family": "Roboto Slab"}, className="blink_me"),
                      html.P("12%", id="o2_sat")], className="block", style={"width": "20%"})
        ]),

        # html.Div(
        #     dcc.Graph(
        #         id="graph2",
        #         figure=dp_water.get_single_data("wd", stationid, from_when),
        #         style={"height": "50%", "width": "100%"},
        #         config={"displayModeBar": False}
        #     ), className="graph"
        #
        # )
    ], className="card", id ="card1"),
    html.Br(),


    #html.Button("Open Card 2", id="button2"),
    html.Div([
        html.H4("Amphiro"),
        html.Div(
            [html.P("Flow rate", style={"color": "#006300", "font-family": "Roboto Slab"}, className="blink_me"),
             html.P("10.8 l/min")], className="block",
            style={"width": "20%"}),
        html.Div([html.P("Energy", style={"color": "#006300", "font-family": "Roboto Slab"}, className="blink_me"),
                  html.P("0.57 kWh")], className="block", style={"width": "20%"})
    ], className="card", id="card2"),
    html.Br(),

    #html.Button("Open Card 3", id="button3"),
    html.Div([
        html.H4("Orankesee"),
        #html.Img(src="assets/bade_eu.png"),
        html.Div([html.P("Water Quality", style={"color": "#006300", "font-family": "Roboto Slab"}, className="blink_me"),
                      html.P("OK", style={"background-color":"orange"}, className="wq")], className="block", style={"width": "20%"}),
        html.Div([html.P("Capacity", style={"color": "#006300", "font-family": "Roboto Slab"}, className="blink_me"),
                      html.P("67%")], className="block", style={"width": "20%"}),
        html.Div([html.P("Temp", style={"color": "#006300", "font-family": "Roboto Slab"}, className="blink_me"),
                      html.P("3°C")], className="block", style={"width": "20%"}),

    ], className="card", id="card3"),

    html.Div([
        html.H4("Weissensee"),
        # html.Img(src="assets/bade_eu.png"),
        html.Div(
            [html.P("Water Quality", style={"color": "#006300", "font-family": "Roboto Slab"}, className="blink_me"),
             html.P("Bad", style={"background-color":"red"}, className="wq")], className="block", style={"width": "20%"}),
        html.Div([html.P("Capacity", style={"color": "#006300", "font-family": "Roboto Slab"}, className="blink_me"),
                  html.P("3%")], className="block", style={"width": "20%"}),
        html.Div([html.P("Temp", style={"color": "#006300", "font-family": "Roboto Slab"}, className="blink_me"),
                  html.P("25°C")], className="block", style={"width": "20%"}),
    ], className="card", id="card4"),

    html.Div([
        html.H4("Ploetzensee"),
        # html.Img(src="assets/bade_eu.png"),
        html.Div(
            [html.P("Water Quality", style={"color": "#006300", "font-family": "Roboto Slab"}, className="blink_me"),
             html.P("Good", style={"background-color":"green"}, className="wq")], className="block", style={"width": "20%"}),
        html.Div([html.P("Capacity", style={"color": "#006300", "font-family": "Roboto Slab"}, className="blink_me"),
                  html.P("45%")], className="block", style={"width": "20%"}),
        html.Div([html.P("Temp", style={"color": "#006300", "font-family": "Roboto Slab"}, className="blink_me"),
                  html.P("20°C")], className="block", style={"width": "20%"}),
    ], className="card", id="card5"),

    html.Div([
        html.H4("Ploetzensee"),
        # html.Img(src="assets/bade_eu.png"),
        html.Div(
            [html.P("Water Quality", style={"color": "#006300", "font-family": "Roboto Slab"}, className="blink_me"),
             html.P("Good", style={"background-color":"green"}, className="wq")], className="block", style={"width": "20%"}),
        html.Div([html.P("Capacity", style={"color": "#006300", "font-family": "Roboto Slab"}, className="blink_me"),
                  html.P("45%")], className="block", style={"width": "20%"}),
        html.Div([html.P("Temp", style={"color": "#006300", "font-family": "Roboto Slab"}, className="blink_me"),
                  html.P("20°C")], className="block", style={"width": "20%"}),
    ], className="card")


])


@app.callback(
    dash.dependencies.Output('card1', 'style'),
    [dash.dependencies.Input('button1', 'n_clicks')],
    )
def button_toggle(n_clicks):
    if n_clicks % 2 == 1:
        return {'display': 'block'}
    else:
        return {'display': 'none'}


@app.callback(
    dash.dependencies.Output('card2', 'style'),
    [dash.dependencies.Input('button2', 'n_clicks')],
    )
def button_toggle(n_clicks):
    if n_clicks % 2 == 1:
        return {'display': 'block'}
    else:
        return {'display': 'none'}


@app.callback(
    dash.dependencies.Output('card3', 'style'),
    [dash.dependencies.Input('button3', 'n_clicks')],
    )
def button_toggle(n_clicks):
    if n_clicks % 2 == 1:
        return {'display': 'block'}
    else:
        return {'display': 'none'}


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
    app.run_server(port=5000, debug=True, host="0.0.0.0")