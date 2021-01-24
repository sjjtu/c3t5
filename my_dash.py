import dash
import dash_html_components as html
import pandas as pd


app = dash.Dash(__name__)
app.layout = html.Div()


if __name__ == "__main__":
    app.run_server(port=5000, debug=True)