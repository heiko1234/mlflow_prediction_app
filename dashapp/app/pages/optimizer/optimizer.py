

# https://stackoverflow.com/questions/64994341/gauge-needle-for-plotly-indicator-graph

# optimizer page

import base64
import datetime
import io
from io import StringIO

import pandas as pd

# from upath import UPath

import dash
from dash import ctx
from dash import html, dcc
from dash.dependencies import Input, Output, State, MATCH, ALL

from dash import dash_table
from upath import UPath

from app.utilities.cards import (
    standard_card,
    form_card
)

from app.utilities.additional import (
    flatten_dict,
    create_feature_div_df,
    create_feature_div_dict,
    gauge_color
)


from app.utilities.api_call_clients import APIBackendClient


## Diskcache
from dash.long_callback import DiskcacheLongCallbackManager
import diskcache
cache = diskcache.Cache("./cache")
long_callback_manager = DiskcacheLongCallbackManager(cache)


def bounds_from_dict(bounds_dict):
    bounds = [[bounds_dict[element]["min"], bounds_dict[element]["max"]] for element in bounds_dict.keys()]
    return bounds


dataclient=APIBackendClient()



dash.register_page(__name__,"/optimizer")



layout = html.Div(
    id="optimizer_page_content",
    className="optimizer_page_content",
    children=[
        html.H1(children='Data'),
        html.Div(children='''
            Choose your data source.
            '''),
        html.H1(),
        html.Div([
            html.Div([
                html.Div(
                    standard_card(
                        id="optimizer_selection_card",
                        header_text="Model Selction",
                        content=[
                            html.Div([
                                dcc.Dropdown(
                                    id="model_selection_dd_optimizer",
                                    style={"width": "280px"},
                                ),
                                # html.Button('Submit',
                                #     className="submit_button",
                                #     id='submit-val',
                                #     n_clicks=0,
                                #     style={"margin": "10px"}
                                # )
                            ],
                            style={"display": "flex", "flex-direction": "column", "align-items": "center"}
                            )
                        ],
                        height="230px",
                        width="350px"
                    )
                ),
                html.Div(
                    standard_card(
                        id="optimizer_target_card",
                        header_text="Target",
                        height="430px",
                        width="350px",
                        content=[
                            html.Div([
                                html.Div(id="target_div_optimizer"),
                                html.Button('Submit',
                                        className="submit_button",
                                        id='submit-val',
                                        n_clicks=0,
                                        style={"margin": "15px"}
                                    )
                            ],
                            style={"display": "block",
                                "align-items": "center",
                                "justify-content": "center",
                                "overflow": "scroll",
                                "height": "350px"
                                })
                        ]
                    ),
                ),
                html.Div(
                    standard_card(
                        id="model_features_card_optimizer",
                        header_text="Model Features",
                        height="700px",
                        width="350px",
                        content=[
                            html.Div([
                                html.Div(id="list-container-div_optimizer"),
                                html.Div(id="model_feature_output_div_optimizer")
                            ])
                        ],
                    )
                )
            ], style={"display": "block"}
            ),
            html.Div([
                html.Div([
                    standard_card(
                        id="model_prediction_table_card",
                        header_text="Model Prediction",
                        height="250px",
                        width="950px",
                        content=[
                            dcc.Loading(id="model_prediction_table_loading")
                        ]
                    ),
                    standard_card(
                        id="model_prediction_card_optimizer",
                        header_text="Model Prediction",
                        height="950px",
                        width="950px",
                        content=[
                            dcc.Loading(id="model_prediction_loading_optimizer")
                        ]
                    )
                ], style={"display": "block"}
                )
            ]),
        ], style={"display": "flex"}
        ),
    ],
)



@dash.callback(
    [
        Output("model_selection_dd_optimizer", "options"),
        Output("model_selection_dd_optimizer", "value"),
    ],
    [
        Input("model_selection_dd_optimizer", "value"),
    ]
)
def update_dd_model_selection(dd_value):


    try:
        headers = None
        endpoint = "list_available_models"


        response = dataclient.Backendclient.execute_get(
            headers=headers,
            endpoint=endpoint,
            )

        if response.status_code == 200:
            output = response.json()


            output = ["project_name"]


            if isinstance(output, list):
                listed_models = output
            else:
                listed_models = [output]

        else:
            listed_models = None
            options = None
            value = None

            return value


        listed_models = list(set(listed_models))


        options = [
            {"label": i, "value": i} for i in listed_models
        ]

        if dd_value is None:
            value = listed_models[0]

        else:
            value = dd_value

        return options, value

    except Exception as e:
        print(e)
        return None, None



@dash.callback(
    Output("target_div_optimizer", "children"),
    Input("model_selection_dd_optimizer", "value"),
)
def update_target_div(model_selection_dd_value):

    try:
        headers = None
        endpoint = "get_model_artifact"


        artifact_value = "target_limits.json"

        data_statistics_dict = {
                "account": "devstoreaccount1",
                "use_model_name": model_selection_dd_value,
                "artifact": artifact_value,
                "staging": "Staging"
            }


        response = dataclient.Backendclient.execute_post(
            headers=headers,
            endpoint=endpoint,
            json=data_statistics_dict
            )


        if response.status_code == 200:
            output = response.json()

            # print(f"optimizer: {output}")


            api_output_dict = {model_selection_dd_value: output}

        else:
            return None


        if model_selection_dd_value is None:
            return None

        else:
            output = []
            for target_element in list(api_output_dict[model_selection_dd_value].keys()):

                element_output = html.Div([
                    html.H3(children=target_element),
                    html.H4(children=f"Min: {round(api_output_dict[model_selection_dd_value][target_element]['min'], 4)} - Max: {round(api_output_dict[model_selection_dd_value][target_element]['max'], 4)}"),
                    dcc.Input(
                        id={"type": "numberinputtarget", "index": target_element},  #
                        type="number",
                        value=None,
                        min=api_output_dict[model_selection_dd_value][target_element]["min"],
                        max=api_output_dict[model_selection_dd_value][target_element]["max"],
                        # step=step_value,
                    )
                ])

                output.append(element_output)

            output = html.Div(id="model_target_inputs", children=output,
                        style={
                            #"height": "350px",
                            "maxHeight": "350px",
                            "overflow": "scroll"
                            })

    except Exception as e:
        print(e)
        output = html.H3("Please select a model")


    return output



@dash.callback(
    Output("list-container-div_optimizer", "children"),
    Input("model_selection_dd_optimizer", "value"),
)
def update_list_container_div(model_selection_dd_value):

    # api_output_dict = {
    #     "project_name": {"feature1": {"min": 60, "max": 80}, "feature2": {"min": 60, "max": 80}},
    #     "project2": {"feature3": {"min": 60, "max": 80}, "feature4": {"min": 60, "max": 80}},
    #     "model3": {"feature5": {"min": 60, "max": 80}, "feature6": {"min": 60, "max": 80}},
    #     "model4": {"feature7": {"min": 60, "max": 80}, "feature8": {"min": 60, "max": 80}, "feature9": {"min": 60, "max": 80}, "feature10": {"min": 60, "max": 80}, "feature11": {"min": 60, "max": 80}, "feature12": {"min": 60, "max": 80}, "feature13": {"min": 9, "max": 90}, "feature14": {"min": 55, "max": 76}}
    # }


    try:
        headers = None
        endpoint = "get_model_artifact"


        artifact_value = "feature_limits.json"

        data_statistics_dict = {
                "account": "devstoreaccount1",
                "use_model_name": model_selection_dd_value,
                "artifact": artifact_value,
                "staging": "Staging"
            }


        response = dataclient.Backendclient.execute_post(
            headers=headers,
            endpoint=endpoint,
            json=data_statistics_dict
            )


        if response.status_code == 200:
            output = response.json()

            # print(f"optimizer: {output}")


            api_output_dict = {model_selection_dd_value: output}

        else:
            return None


        if model_selection_dd_value is None:
            return None

        else:
            output = []
            for feature_element in list(api_output_dict[model_selection_dd_value].keys()):

                avg_value = 0.5*(api_output_dict[model_selection_dd_value][feature_element]["max"] - api_output_dict[model_selection_dd_value][feature_element]["min"]) + api_output_dict[model_selection_dd_value][feature_element]["min"]
                range_value = api_output_dict[model_selection_dd_value][feature_element]["max"] - api_output_dict[model_selection_dd_value][feature_element]["min"]
                step_value = round(range_value/100, 4)

                min_value = round(api_output_dict[model_selection_dd_value][feature_element]["min"], 4)
                max_value = round(api_output_dict[model_selection_dd_value][feature_element]["max"],4)

                element_output = html.Div([
                    html.H3(children=feature_element),
                    html.H4(children=f"Min: {round(api_output_dict[model_selection_dd_value][feature_element]['min'], 4)} - Max: {round(api_output_dict[model_selection_dd_value][feature_element]['max'], 4)}"),

                    dcc.RangeSlider(
                        id={"type": "limitsinput", "index": feature_element},
                        min=min_value,
                        max=max_value,
                        step=step_value,
                        value=[min_value, max_value],
                        marks={
                            min_value: str(min_value),
                            max_value: str(max_value)
                        },
                        tooltip={"placement": "bottom", "always_visible": True}
                    )
                ])

                output.append(element_output)

            output = html.Div(id="model_feature_inputs_optimizer", children=output, style={"height": "550px", "overflow": "scroll"})

            return output

    except Exception as e:
        print(e)
        return None




# model_prediction_loading_optimizer

@dash.callback(
    Output("model_prediction_table_loading", "children"),
    Input('submit-val', 'n_clicks'),
    State("list-container-div_optimizer", "children"),
    prevent_initial_call=True
)
def update_list_container_div(n_clicks, optimizer_feature_inputs):

    # print(optimizer_feature_inputs)

    print(create_feature_div_dict(optimizer_feature_inputs))

    # {'BiologicalMaterial02': {'min': 52.7973, 'max': 61.5669}, 'ManufacturingProcess06': {'min': 207.296, 'max': 220.368}}


    headers = None
    endpoint = "model_make_optimizing"


    blobstorage_environment = "devstoreaccount1"


    limits_dict = create_feature_div_dict(optimizer_feature_inputs)

    data_statistics_dict = {
        "account": blobstorage_environment,
        "use_model_name": "project_name",
        "limits_dict": limits_dict,
        "staging": "Staging",
        "target": 44
    }


    data_statistics_dict


    response = dataclient.Backendclient.execute_post(
        headers=headers,
        endpoint=endpoint,
        json=data_statistics_dict
        )


    if response.status_code == 200:
        output = response.json()

    output_df = pd.DataFrame.from_dict(output, orient='index')


    print(output_df)


    # output should be a dash_table.DataTable

    output = dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in output_df.columns],
        data=output_df.to_dict('records'),
        style_cell={'textAlign': 'left'},
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold'
        }
    )

    return output




