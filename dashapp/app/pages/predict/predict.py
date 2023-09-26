
# landing page

import base64
import datetime
import io

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
    gauge_color
)


from app.utilities.api_call_clients import APIBackendClient


dataclient=APIBackendClient()



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
        html.Div([
            html.Div([
                html.Div(
                    standard_card(
                        id="model_selection_card",
                        header_text="Model Selction",
                        content=[
                            html.Div([
                                dcc.Dropdown(
                                    id="model_selection_dd",
                                    style={"width": "280px"},
                                ),
                            ],
                            )
                        ],
                        height="230px",
                        width="350px"
                    )
                ),
                html.Div(
                    standard_card(
                        id="model_features_card",
                        header_text="Model Features",
                        height="700px",
                        width="350px",
                        content=[
                            html.Div([
                                html.Div(id="list-container-div"),
                                html.Div(id="model_feature_output_div")
                            ])
                        ],
                    )
                )
            ], style={"display": "block"}
            ),
            html.Div([
                html.Div(
                    standard_card(
                        id="model_prediction_card",
                        header_text="Model Prediction",
                        height="950px",
                        width="950px",
                        content=[
                            dcc.Loading(id="model_prediction_loading")
                        ]
                    )
                )
            ]),
        ], style={"display": "flex"}
        ),
    ],
)



@dash.callback(
    [
        Output("model_selection_dd", "options"),
        Output("model_selection_dd", "value"),
    ],
    [
        Input("model_selection_dd", "value"),
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
    Output("list-container-div", "children"),
    Input("model_selection_dd", "value"),
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
            }


        response = dataclient.Backendclient.execute_post(
            headers=headers,
            endpoint=endpoint,
            json=data_statistics_dict
            )


        if response.status_code == 200:
            output = response.json()

            print(output)


            api_output_dict = {model_selection_dd_value: output}

        else:
            return None


        if model_selection_dd_value is None:
            return None

        else:
            output = []
            for feature_element in list(api_output_dict[model_selection_dd_value].keys()):

                avg_value = 0.5*(api_output_dict[model_selection_dd_value][feature_element]["max"] - api_output_dict[model_selection_dd_value][feature_element]["min"]) + api_output_dict[model_selection_dd_value][feature_element]["min"]
                element_output = html.Div([
                    html.H3(children=feature_element),
                    html.H4(children=f"Min: {round(api_output_dict[model_selection_dd_value][feature_element]['min'], 4)} - Max: {round(api_output_dict[model_selection_dd_value][feature_element]['max'], 4)}"),
                    dcc.Input(
                        id={"type": "numberinput", "index": feature_element},  #
                        type="number",
                        value=avg_value,
                        min=api_output_dict[model_selection_dd_value][feature_element]["min"],
                        max=api_output_dict[model_selection_dd_value][feature_element]["max"],
                    )
                ])

                output.append(element_output)

            output = html.Div(id="model_feature_inputs", children=output, style={"height": "550px", "overflow": "scroll"})

            return output

    except Exception as e:
        print(e)
        return None



@dash.callback(
    Output("model_prediction_loading", "children"),
    Input("list-container-div", "children"),
    # add pattern matching base on the numberinput id
    Input({"type": "numberinput", "index": ALL}, "value"),
)
def make_model_feature_output(numberinput_value, numberinput_inputs):

    output = numberinput_value

    df = create_feature_div_df(output)

    # df_output should be df pivot table with feature as columns and value as rows
    df_output = df.pivot_table(index=["feature"])
    df_output = df_output.reset_index(drop=False)
    df_output = df_output.loc[:, ["feature", "value"]]

    # print(df)
    # print(df_output)

    data_dict = df.to_dict(orient="records")


    predicted_value = 80
    target_min = 30
    target_max = 90
    target_name = "Parameter"


    output = gauge_color(value=predicted_value, min = target_min, max= target_max, ranges=[30,40,50,60, 90], color="blue", label = target_name)

    return output



