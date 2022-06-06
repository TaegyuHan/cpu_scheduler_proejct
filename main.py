# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
import pandas as pd
from dash import Dash, dcc, html, Input, Output
from view.timeline_plot import TimeGanttPlot
from data.read_data import read_json
from data.statistics_table import get_pandas_statistics_table


app = Dash(__name__)
app.title = "CPU Scheduler"


def build_banner():
    """ 배너 부분 """
    return html.Div(
        id="banner",
        className="banner",
        children=[
            html.Div(
                id="banner-text",
                children=[
                    html.H5("Operating system CPU scheduling"),
                    html.H6("Software Engineering Project, Soonchunhyang University"),
                ],
            )
        ],
    )


def main_panel():
    """ 메인 패널 부분 """
    return html.Div(
        id="main",
        className="main",
        children=[
            html.Div(children=[
                html.H4('데이터 선택 및 스케줄러 선택',
                        style={'textAlign': 'center',
                               'color': '#FFFFFF'}),

                html.Label('CPU 스케줄러'),
                dcc.RadioItems(['FCFS', 'SJF', 'HRN', 'RR', 'SRT', 'NPS', 'PS'],
                               value='FCFS',
                               id="scheduler-input"),

            ], style={'padding': 20, 'flex': 1}),

            html.Div([
                dcc.Graph(id='scheduler-plot')
            ])
        ], style={'display': 'flex', 'flex-direction': 'row'}
    )


def table_panel():
    """ 테이블 패널 """
    return html.Div(
        id="table-panel",
        className="table-panel",
        children=[
            html.Div(children=[
                html.H4(children='Input Process',
                        style={"textAlign": "center"}),
                generate_table(read_json.get_pandas_dataframe())
            ], style={'padding': 20, 'flex': 1}),

            html.Div([
                html.H4(children='통계 테이블',
                        style={"textAlign": "center"}),
                html.Div(id="scheduler-statistics-table-output")
                # generate_table(get_pandas_statistics_table("RR"))
            ], style={'padding': 20, 'flex': 1})

        ], style={'display': 'flex', 'flex-direction': 'row'}
    )


def generate_table(dataframe):
    """ 테이블 생성 """
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(len(dataframe))
        ])
    ])


app.layout = html.Div(
    id="big-app-container",
    children=[
        build_banner(), # 배너 부분
        main_panel(), # 매인 패널 부분
        table_panel(), # 테이블 부분
    ]
)


@app.callback(
    Output(component_id='scheduler-plot', component_property='figure'),
    Input(component_id='scheduler-input', component_property='value')
)
def scheduler_plot(scheduler_input_value):
    """ 스케줄 간트 시각화 보여주기 """
    return TimeGanttPlot.show_plot(scheduler_input_value)


@app.callback(
    Output(component_id='scheduler-statistics-table-output', component_property='children'),
    Input(component_id='scheduler-input', component_property='value')
)
def scheduler_table(scheduler_input_value):
    """ 스케줄 테이블 보여주기 """
    return generate_table(get_pandas_statistics_table(scheduler_input_value))


if __name__ == '__main__':
    app.run_server(debug=True)