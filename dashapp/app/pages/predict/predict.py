


# landing page

import base64
import datetime
import io

import pandas as pd

# from upath import UPath

import dash
from dash import ctx
from dash import html, dcc
from dash.dependencies import Input, Output, State
from dash import dash_table
import dash_daq as daq


from app.utilities.cards import (
    standard_card,
    form_card
)


# from app.utilities.api_call_clients import APIBackendClient


# dataclient=APIBackendClient()



dash.register_page(__name__,"/predict")



layout = html.Div(
    id="dataload_page_content",
    className="dataload_page_content",
    children=[
        html.H1(children='Data'),
        html.Div(children='''
            Choose your data source.
            '''),
        html.H1(),
        html.Div(
            standard_card(
                id="data_tabs_card",
                header_text="Model Selction",
                content=[
                    html.Div([
                        dcc.Dropdown(
                            id="model_selection_dd",
                            style={"width": "280px"}
                        ),
                        html.Div(id="spacer_id"),
                        html.Button('Submit',
                            className="submit_button",
                            id='submitbutton',
                            n_clicks=0,
                        )
                    ]
                    )
                ],
                height="200px",
                width="350px"
            )
        ),
    ],
)



@dash.callback(

    Output("spacer_id", "children"),
    [
        Input("submitbutton", "n_clicks"),
    ]
)
def update_data_scaler(data_scaler):

    output = html.H3("Data Scaler")

    return output







