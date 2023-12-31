

from pydoc import classname
from dash import html, dcc
import base64
import os
from dotenv import load_dotenv


def home_card(
        id,
        header_text,
        text,
        href,
        icon=None
):

    encoded_img = None
    if icon is not None:
        load_dotenv()
        local_run = os.getenv("LOCAL_RUN", False)
        if local_run:
            img_path = str(f"./dashapp/app/assets/{icon}.png")
        else:
            img_path = str(f"./app/assets/{icon}.png")
        encoded_img = base64.b64encode(open(img_path, "rb").read())

    if encoded_img is None:
        output = html.Div(
            className="gnc",
            id=id,
            children=[
                html.Div(
                    className="gnc-body",
                    children=[
                        html.A(
                            className="gnc-card-container",
                            id=f"{id}_container",
                            href=href,
                            children=[
                                html.Div(
                                    className="gnc-topbar",
                                    children=[
                                        html.Div(id=f"{id}_topbar")
                                    ]
                                ),
                                html.H2(
                                    className="gnc-header-text",
                                    children=header_text
                                ),
                                html.P(
                                    className="gnc-description",
                                    children=text
                                )
                            ]
                        )
                    ]
                )
            ]
        )
    else:
        output = html.Div(
            className="gnc",
            id=id,
            children=[
                html.Div(
                    className="gnc-body",
                    children=[
                        html.A(
                            className="gnc-card-container",
                            id=f"{id}_container",
                            href=href,
                            children=[
                                html.Div(
                                    className="gnc-topbar",
                                    children=[
                                        html.Div(id=f"{id}_topbar")
                                    ]
                                ),
                                html.H2(
                                    className="gnc-header-text",
                                    children=header_text
                                ),
                                html.Div(
                                    className="gnc-icon-description",
                                    children=[
                                        html.Img(src='data:image/png;base64,{}'.format(encoded_img.decode(),
                                            className="gnc-icon"),
                                            style={"height": "60px", "width": "60px"}
                                        ),
                                        html.P(
                                            className="gnc-description-icon",
                                            children=text
                                        )
                                    ],
                                    # style={"display": "flex"}
                                )
                            ]
                        )
                    ]
                )
            ]
        )
    return output



def standard_card(
        id,
        header_text,
        content,
        height,
        width
):
    output = html.Div(
        className="stdc",
        id=id,
        children=[
            html.Div(
                className="stdc_content",
                children=[
                    html.H3(header_text),
                    dcc.Markdown("\n---\n"),
                    html.Div(
                        dcc.Loading(*content)
                    )
                ]
            )
        ],
        style={"height": height, "width": width}
    )
    return output

# create function to create a html div card for a form where description of the manual input is side by side to the input

def form_card(
        id,
        header_text,
        height,
        width
):
    output = html.Div(
        className="fc",
        id=id,
        children=[
            html.Div(
                className="fc_content",
                children=[
                    html.H3(header_text),
                    dcc.Input(id=f"{id}_input", type="text", placeholder="Enter a value..."),
                ]
            )
        ],
        style={"height": height, "width": width}
    )
    return output


