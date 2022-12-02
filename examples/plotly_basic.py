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
import plotly.express as px
from flask import Flask, request, send_from_directory

# ----- Nitro app -----

from h2o_nitro import View, box
from h2o_nitro_web import web_directory
from h2o_nitro_plotly import plotly_plugin, plotly_box


# Entry point
def main(view: View):
    # Show plots one by one.
    # view(plotly_box(make_plotly_scatterplot(), style='h-96'))
    view(plotly_box(make_plotly_scatterplot()) / 'h-96')


# Nitro instance
nitro = View(
    main,
    title='Nitro + Plotly',
    caption='A minimal example',
    plugins=[plotly_plugin()],  # Include the Plotly plugin
)


# ----- Plotly plotting routines -----

def make_plotly_scatterplot():
    df = px.data.iris()  # replace with your own data source
    return px.scatter(
        df,
        x="sepal_width",
        y="sepal_length",
        color="species",
    )


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
