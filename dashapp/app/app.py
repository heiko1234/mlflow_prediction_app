

import dash
from dash import Dash, html, dcc
from dash.long_callback import DiskcacheLongCallbackManager

from app.utilities.sidebar_utils import (
    icon_and_text
)


from flask import Flask

# longcallbacks
# diskcache
import diskcache
cache = diskcache.Cache("./cache")
long_callback_manager = DiskcacheLongCallbackManager(cache)



server = Flask(__name__)

# session store
a_session_store = dcc.Store(
    id = "a_session_store", storage_type="session"
)
feature_limit_store = dcc.Store(
    id = "feature_limit_store", storage_type="session"
)


# localhost/dashapp/pages_id
url_base_pathname="/aisam"

app = Dash(
    __name__,
    server = server,
    url_base_pathname="/aisam/",
    use_pages=True
    )

app.title = "AI Sensor Asset Monitoring"





sidebar = html.Div(
    [
        html.Div(
            [
                html.H2("Basic App", style={"color": "white"}),
            ],
            className="sidebar-header",
            ),
        html.Div(
            dcc.Markdown("\n---\n")
        ),
        icon_and_text(id="side_home", text="Home", icon="home", href=url_base_pathname+dash.page_registry['pages.home']['path']),
        icon_and_text(id="side_predict", text="Predict", icon="ai1", href=url_base_pathname+dash.page_registry['pages.predict.predict']['path']),
        icon_and_text(id="side_optimizer", text="Optimize", icon="ai1", href=url_base_pathname+dash.page_registry['pages.optimizer.optimizer']['path']),
    ],
    className="sidebar"
)

app.layout = html.Div(
    [
        sidebar,
        a_session_store,
        html.Div(
            [
                dash.page_container
            ],
            className="content",
        ),
    ]
)

