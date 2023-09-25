


# import logging
import os
import json
import copy

from pathlib import Path, PurePosixPath

from azure.storage.blob import BlobServiceClient


from dash import dcc as dcc


from numpy.random import randint
from numpy.random import rand



def flatten_dict(nested_dict):
    output={}
    for key in nested_dict.keys():
        for second_key in nested_dict[key].keys():
            if second_key not in output:
                output[second_key] = nested_dict[key][second_key]
    return output


def flatten_consolidate_dict(nested_dict, take_lower_min=True, take_higher_max=True):
    output={}
    for key in nested_dict.keys():
        for second_key in nested_dict[key].keys():
            if second_key not in output:
                output[second_key] = copy.deepcopy(nested_dict[key][second_key])
            if second_key in output:
                if take_lower_min:
                    if output[second_key]["min"] > nested_dict[key][second_key]["min"]:
                        output[second_key]["min"] = copy.deepcopy(nested_dict[key][second_key]["min"])
                else:
                    if output[second_key]["min"] < nested_dict[key][second_key]["min"]:
                        output[second_key]["min"] = copy.deepcopy(nested_dict[key][second_key]["min"])
                if take_higher_max:
                    if output[second_key]["max"] < nested_dict[key][second_key]["max"]:
                        output[second_key]["max"] = copy.deepcopy(nested_dict[key][second_key]["max"])
                else:
                    if output[second_key]["max"] > nested_dict[key][second_key]["max"]:
                        output[second_key]["max"] = copy.deepcopy(nested_dict[key][second_key]["max"])
    return output


def create_warning(TAG_limit_dict, key, value, digits=2):
    if key in TAG_limit_dict.keys():
        if value < TAG_limit_dict[key]["min"]:
            return dcc.Markdown(
                f"""{key} is below min value of model:
                        {round(TAG_limit_dict[key]["min"], digits)} """
            )

        elif value > TAG_limit_dict[key]["max"]:
            return dcc.Markdown(
                f"""{key} is above max value of model:
                        {round(TAG_limit_dict[key]["max"], digits)} """
            )

        else:
            return None

    else:
        return None



def gauge_color(value, min = 20, max= 60, ranges=[0,30,40,50,60], color=None, label = "Parameter"):

    if not color:
        color ={
            "gradient": True,
            "ranges": {
                "green": [ranges[0], ranges[1]],
                "yellow": [ranges[1], ranges[2]],
                "red": [ranges[2], ranges[3]],
                "purple": [ranges[3],ranges[4]],
            },
        }
    return html.Div(
        daq.Gauge(
            id="gauge_id",
            color=color,
            showCurrentValue=True,
            units="Unit",
            value=value,
            label=label,
            max=max,
            min=min,
            size=350,
        )
    )



