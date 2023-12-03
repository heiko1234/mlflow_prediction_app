

import pandas as pd


input = {'props': {'children': [{'props': {'children': [{'props': {'children': 'BiologicalMaterial02'}, 'type': 'H3', 'namespace': 'dash_html_components'}, {'props': {'children': 'Min: 47.5773 - Max: 68.4527'}, 'type': 'H4', 'namespace': 'dash_html_components'}, {'props': {'min': 47.5773, 'max': 68.4527, 'step': 0.2088, 'marks': {'47.5773': '47.5773', '68.4527': '68.4527'}, 'value': [47.5773, 68.4527], 'tooltip': {'placement': 'bottom', 'always_visible': True}, 'id': {'type': 'limitsinput', 'index': 'BiologicalMaterial02'}, 'drag_value': [47.5773, 68.4527]}, 'type': 'RangeSlider', 'namespace': 'dash_core_components'}]}, 'type': 'Div', 'namespace': 'dash_html_components'}, {'props': {'children': [{'props': {'children': 'ManufacturingProcess06'}, 'type': 'H3', 'namespace': 'dash_html_components'}, {'props': {'children': 'Min: 199.9995 - Max: 230.4005'}, 'type': 'H4', 'namespace': 'dash_html_components'}, {'props': {'min': 199.9995, 'max': 230.4005, 'step': 0.304, 'marks': {'199.9995': '199.9995', '230.4005': '230.4005'}, 'value': [199.9995, 230.4005], 'tooltip': {'placement': 'bottom', 'always_visible': True}, 'id': {'type': 'limitsinput', 'index': 'ManufacturingProcess06'}, 'drag_value': [199.9995, 230.4005]}, 'type': 'RangeSlider', 'namespace': 'dash_core_components'}]}, 'type': 'Div', 'namespace': 'dash_html_components'}], 'id': 'model_feature_inputs_optimizer', 'style': {'height': '550px', 'overflow': 'scroll'}}, 'type': 'Div', 'namespace': 'dash_html_components'}



input = {'props': {'children': [{'props': {'children': [{'props': {'children': 'BiologicalMaterial02'}, 'type': 'H3', 'namespace': 'dash_html_components'}, {'props': {'children': 'Min: 47.5773 - Max: 68.4527'}, 'type': 'H4', 'namespace': 'dash_html_components'}, {'props': {'min': 47.5773, 'max': 68.4527, 'step': 0.2088, 'marks': {'47.5773': '47.5773', '68.4527': '68.4527'}, 'value': [51.7533, 62.1933], 'tooltip': {'placement': 'bottom', 'always_visible': True}, 'id': {'type': 'limitsinput', 'index': 'BiologicalMaterial02'}, 'drag_value': [51.7533, 62.1933]}, 'type': 'RangeSlider', 'namespace': 'dash_core_components'}]}, 'type': 'Div', 'namespace': 'dash_html_components'}, {'props': {'children': [{'props': {'children': 'ManufacturingProcess06'}, 'type': 'H3', 'namespace': 'dash_html_components'}, {'props': {'children': 'Min: 199.9995 - Max: 230.4005'}, 'type': 'H4', 'namespace': 'dash_html_components'}, {'props': {'min': 199.9995, 'max': 230.4005, 'step': 0.304, 'marks': {'199.9995': '199.9995', '230.4005': '230.4005'}, 'value': [199.9995, 230.4005], 'tooltip': {'placement': 'bottom', 'always_visible': True}, 'id': {'type': 'limitsinput', 'index': 'ManufacturingProcess06'}, 'drag_value': [199.9995, 230.4005]}, 'type': 'RangeSlider', 'namespace': 'dash_core_components'}]}, 'type': 'Div', 'namespace': 'dash_html_components'}], 'id': 'model_feature_inputs_optimizer', 'style': {'height': '550px', 'overflow': 'scroll'}, 'n_clicks': 2, 'n_clicks_timestamp': 1701628960915}, 'type': 'Div', 'namespace': 'dash_html_components'}





input["props"]["children"]

j = input["props"]["children"][0]

j["props"]




for i in input["props"]["children"]:
    for j in i["props"]["children"]:
        try:
            if j["props"]["id"]["type"] == "limitsinput":

                print(j["props"]["id"]["index"])
                print(j["props"]["value"])
                print(j["props"]["min"])
                print(j["props"]["max"])
        except:
            pass






def create_feature_div_df(dict):

    # df = pd.DataFrame(columns=["feature", "value", "min", "max"])

    output = {}


    for i in dict["props"]["children"]:
        for j in i["props"]["children"]:
            try:
                if j["props"]["id"]["type"] == "limitsinput":

                    # output[j["props"]["id"]["index"]] = {"min": j["props"]["min"], "max": j["props"]["max"]}

                    output[j["props"]["id"]["index"]] = {"min": j["props"]["value"][0], "max": j["props"]["value"][1]}


            except:
                pass
    return output




output_dict = create_feature_div_df(input)


output_dict


# >>> output_dict
# {'BiologicalMaterial02': {'min': 47.5773, 'max': 68.4527}, 
#  'ManufacturingProcess06': {'min': 199.9995, 'max': 230.4005}}





