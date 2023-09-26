


feature_div_dict = {'props': {'children': [{'props': {'children': [{'props': {'children': 'feature1'}, 'type': 'H3', 'namespace': 'dash_html_components'}, {'props': {'value': 70, 'type': 'number', 'min': 60, 'max': 80, 'id': {'type': 'numberinput', 'index': 'feature1'}}, 'type': 'Input', 'namespace': 'dash_core_components'}]}, 'type': 'Div', 'namespace': 'dash_html_components'}, {'props': {'children': [{'props': {'children': 'feature2'}, 'type': 'H3', 'namespace': 'dash_html_components'}, {'props': {'value': 70, 'type': 'number', 'min': 60, 'max': 80, 'id': {'type': 'numberinput', 'index': 'feature2'}}, 'type': 'Input', 'namespace': 'dash_core_components'}]}, 'type': 'Div', 'namespace': 'dash_html_components'}]}, 'type': 'Div', 'namespace': 'dash_html_components'}


feature_div_dict["props"]


feature_div_dict["props"]["children"][0]

feature_div_dict["props"]["children"][0]["props"]["children"][1]

feature_div_dict["props"]["children"][0]["props"]["children"][1]["props"]["id"]["index"]

feature_div_dict["props"]["children"][0]["props"]["children"][1]["props"]["value"]


feature_div_dict["props"]["children"][0]["props"]["children"][0]["props"]["id"]["index"]

feature_div_dict["props"]["children"][0]["props"]["children"][0]["props"]["value"]





feature_div_dict["props"]["children"][1]

feature_div_dict["props"]["children"][0]

# feature_div_dict["props"]["children"][2]


for i in feature_div_dict["props"]["children"]:
    # print(i["props"]["children"])
    for j in i["props"]["children"]:
        try:
            if j["props"]["id"]["type"] == "numberinput":
                print(j["props"]["id"]["index"])
                print(j["props"]["value"])
                print(j["props"]["min"])
                print(j["props"]["max"])
        except:
            pass







import pandas as pd


def create_feature_div_df(dict):

    # df = pd.DataFrame(columns=["feature", "value", "min", "max"])

    df = pd.DataFrame()


    for i in dict["props"]["children"]:
        for j in i["props"]["children"]:
            try:
                if j["props"]["id"]["type"] == "numberinput":

                    # print(f"feature: {j['props']['id']['index']}")
                    # print(f"value: {j['props']['value']}")
                    # print(f"min: {j['props']['min']}")
                    # print(f"max: {j['props']['max']}")

                    df_newrow = {"feature": j["props"]["id"]["index"], "value": j["props"]["value"], "min": j["props"]["min"], "max": j["props"]["max"]}
                    df_new = pd.DataFrame(df_newrow, index=[0])

                    df = pd.concat([df, df_new], axis=0)
                    df = df.reset_index(drop=True)

            except:
                pass
    return df



create_feature_div_df(dict=feature_div_dict)


# >>> create_feature_div_df(dict=feature_div_dict)
#     feature  value  min  max
# 0  feature1     70   60   80
# 1  feature2     70   60   80





