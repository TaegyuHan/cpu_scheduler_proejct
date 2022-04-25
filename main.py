# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, dcc, html
from view.timeline_plot import TimeLinePlot


app = Dash(__name__)

app.layout = html.Div([
    dcc.Graph(
        id='life-exp-vs-gdp',
        figure=TimeLinePlot.show_plot("fcfs")
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)