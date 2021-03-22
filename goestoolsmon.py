# uses https://plotly.com/python/gauge-charts/
import nnpy
import json
import threading
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from datetime import datetime

global viterbi_last_sec, reed_solomon_last_sec, skipped_symbols_last_sec

sub = nnpy.Socket(nnpy.AF_SP, nnpy.SUB)
sub.connect('tcp://192.168.1.109:6002')
sub.setsockopt(nnpy.SUB, nnpy.SUB_SUBSCRIBE, '')

app = dash.Dash()
app.layout = html.Div([dcc.Graph(id='goestools-gauges'),
                       dcc.Interval(id='interval-component',interval=1*1000,n_intervals=0),])

def update_stats():
    global viterbi_last_sec, reed_solomon_last_sec, skipped_symbols_last_sec

    sub = nnpy.Socket(nnpy.AF_SP, nnpy.SUB)
    sub.connect('tcp://192.168.1.109:6002')
    sub.setsockopt(nnpy.SUB, nnpy.SUB_SUBSCRIBE, '')

    viterbi_last_sec = 0
    reed_solomon_last_sec = 0
    skipped_symbols_last_sec = 0
    viterbi_errors = 0
    reed_solomon_errors = 0
    skipped_symbols = 0
    num = 1
    timeold = 0

    while True:
        data = json.loads(sub.recv())
        time=datetime.fromisoformat(data['timestamp'][:-1]).second
        if time != timeold:
            viterbi_last_sec = int(viterbi_errors/num)
            reed_solomon_last_sec = int(reed_solomon_errors/num)
            skipped_symbols_last_sec = int(skipped_symbols/num)
            print(num, viterbi_last_sec, reed_solomon_last_sec, skipped_symbols_last_sec)
            viterbi_errors = 0
            reed_solomon_errors = 0
            skipped_symbols = 0
            num = 0
            timeold = time
        viterbi_errors += data['viterbi_errors']
        reed_solomon_errors += data['reed_solomon_errors']
        skipped_symbols += data['skipped_symbols']
        num += 1

@app.callback(Output('goestools-gauges','figure'),Input('interval-component','n_intervals'))
def update_viterbi(n):
    global viterbi_last_sec, reed_solomon_last_sec, skipped_symbols_last_sec

    fig = make_subplots(
        rows=1, cols=3,
            column_widths=[0.3, 0.3, 0.3],
            row_heights=[1.0,],
            specs=[[{"type": "indicator"}, {"type": "indicator"}, {"type": "indicator"},],])

    if viterbi_last_sec >500:
        scale=2500
    else:
        scale=500
    fig.add_trace(go.Indicator(
        mode = "gauge+number",
        value = viterbi_last_sec,
        domain = {'x': [0, 1], 'y': [0, 1]},
        gauge = {'axis': {'range': [None, scale]}},
        title = {'text': "Viterbi Errors"}),
        row=1,col=1)

    if reed_solomon_last_sec > 10:
        scale=100
    else:
        scale=10
    fig.add_trace(go.Indicator(
        mode = "gauge+number",
        value = reed_solomon_last_sec,
        domain = {'x': [0, 1], 'y': [0, 1]},
        gauge = {'axis': {'range': [None, 10]}},
        title = {'text': "Reed Soloman Errors"}),
        row=1,col=2)

    if skipped_symbols_last_sec > 10:
        scale=60
    else:
        scale=10
    fig.add_trace(go.Indicator(
        mode = "gauge+number",
        value = skipped_symbols_last_sec,
        domain = {'x': [0, 1], 'y': [0, 1]},
        gauge = {'axis': {'range': [None, 60]}},
        title = {'text': "Skipped Symbols"}),
        row=1,col=3)

    fig.update_layout(height=500, width=1000)
    return fig

if __name__ == "__main__":
    thread = threading.Thread(target=update_stats).start()
    app.run_server(debug=False, use_reloader=False)  # Turn off reloader if inside Jupyter
