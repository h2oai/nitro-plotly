# Run this example easily with "nitro run URL".
# Get the nitro CLI: https://nitro.h2o.ai/cli/
#
# Like Nitro? Please star us on Github: https://github.com/h2oai/nitro
#
# ===
# About: How to use Plotly in Nitro apps
# Author: Prithvi Prabhu <prithvi.prabhu@gmail.com>
# License: Apache-2.0
# Source: https://github.com/h2oai/nitro-plotly/examples
# Keywords: [visualization]
#
# Setup:
# FILE requirements.txt EOF
# numpy
# pandas
# scipy
# plotly
# Flask>=2
# simple-websocket>=0.5
# h2o-nitro[web]
# h2o-nitro-plotly
# EOF
# RUN python -m pip install -r requirements.txt
# ENV FLASK_APP plotly_basic.py
# ENV FLASK_ENV development
# START python -m flask run
# ===
import simple_websocket
from flask import Flask, request, send_from_directory

# ----- Nitro app -----

from h2o_nitro import View, box
from h2o_nitro_web import web_directory
from h2o_nitro_plotly import plotly_plugin, plotly_box

import numpy as np
import pandas as pd
import plotly.figure_factory as ff
import plotly.graph_objects as go
import plotly.express as px


# Entry point
def main(view: View):
    # Show plots one by one.
    view(plotly_box(make_plotly_scatterplot()))
    view(plotly_box(make_plotly_distplot()))
    view(plotly_box(make_plotly_boxplot()))
    view(plotly_box(make_plotly_hist2d()))
    view(plotly_box(make_plotly_path()))


# Nitro instance
nitro = View(
    main,
    title='Nitro + Plotly',
    caption='A minimal example',
    plugins=[plotly_plugin()],  # Include the Plotly plugin
)


# ----- Plotly plotting routines -----

# Source: https://plotly.com/python/line-and-scatter/
def make_plotly_scatterplot():
    df = px.data.iris()
    return px.scatter(
        df,
        x="sepal_width",
        y="sepal_length",
        color="species",
    )


# Source: https://plotly.com/python/distplot/
def make_plotly_distplot():
    df = pd.DataFrame({
        '2012': np.random.randn(200),
        '2013': np.random.randn(200) + 1,
    })
    return ff.create_distplot([df[c] for c in df.columns], df.columns, bin_size=.25)


# https://plotly.com/python/box-plots/
def make_plotly_boxplot():
    df = px.data.tips()
    return px.box(df, x="time", y="total_bill", points="all")


# Source: https://plotly.com/python/2D-Histogram/
def make_plotly_hist2d():
    np.random.seed(1)
    x = np.random.randn(500)
    y = np.random.randn(500) + 1
    return go.Figure(go.Histogram2d(
        x=x,
        y=y
    ))


# Source: https://plotly.com/python/line-and-scatter/
def make_plotly_path():
    df = px.data.gapminder().query("country in ['Canada', 'Botswana']")
    fig = px.line(df, x="lifeExp", y="gdpPercap", color="country", text="year")
    fig.update_traces(textposition="bottom right")
    return fig


# ----- Flask boilerplate -----

app = Flask(__name__, static_folder=web_directory, static_url_path='')


@app.route('/')
def home_page():
    return send_from_directory(web_directory, 'index.html')


@app.route('/nitro', websocket=True)
def socket():
    ws = simple_websocket.Server(request.environ)
    try:
        nitro.serve(ws.send, ws.receive)
    except simple_websocket.ConnectionClosed:
        pass
    return ''


if __name__ == '__main__':
    app.run()
