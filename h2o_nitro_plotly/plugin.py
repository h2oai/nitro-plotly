# Copyright 2022 H2O.ai, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Optional
import io
import json
from base64 import b64encode
from h2o_nitro import box, Box, Plugin, Script

try:
    from plotly.io._utils import plotly_cdn_url  # ugh!

    cdn_url = plotly_cdn_url()
except:
    # Fallback in case plotly_cdn_url() disappears in a future plotly version.
    cdn_url = 'https://cdn.plot.ly/plotly-2.16.1.min.js'

# Javascript function for embedding the Plotly plot.
# See: https://plotly.com/python/interactive-html-export/
# Here, we export one function called embed(), which we can later invoke from our Python box().
_plotly_embed_js = '''
exports.embed = (context, element, data) => {
    Plotly.newPlot(element, JSON.parse(data.figure));
};
'''


def plotly_plugin(plotly_js_path: Optional[str] = None):
    """
    Creates a Nitro plugin for the currently installed version of Plotly.
    :param plotly_js_path: URL of plotly.js Javascript file. Defaults to Plotly's CDN.
    :return: A plugin
    """
    return Plugin(
        name='plotly',
        scripts=[
            # Install the Plotly library.
            Script(source=plotly_js_path or cdn_url),
            # Install our custom Plotly-embedding Javascript.
            Script(source=_plotly_embed_js, type='inline'),
        ],
    )


def plotly_box(figure) -> Box:
    """
    Creates a Nitro box from a Plotly figure.
    :param figure: A Plotly figure (required).
    :return: A box
    """
    return box(mode='plugin:plotly.embed', data=dict(figure=figure.to_json(remove_uids=True)), ignore=True)
