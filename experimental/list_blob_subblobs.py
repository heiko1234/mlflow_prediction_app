











import pandas as pd


from experimental.api_call_clients import APIBackendClient


dataclient=APIBackendClient()






headers = None
headers = {"accept": "application/json", "Content-Type": "application/json"}




endpoint = "list_available_models"


response = dataclient.Backendclient.execute_get(
    headers=headers,
    endpoint=endpoint,
    )


response.status_code   # 200

df = response.json()

df





headers = None
endpoint = "get_model_artifact"


blobstorage_environment = "devstoreaccount1"


data_statistics_dict = {
    "account": blobstorage_environment,
    "use_model_name": "project_name",
    "artifact": "feature_limits_unscaled.json"
}



response = dataclient.Backendclient.execute_post(
    headers=headers,
    endpoint=endpoint,
    json=data_statistics_dict
    )


response.status_code 

if response.status_code == 200:
    output = response.json()

output

# >>> output
# {'BiologicalMaterial02': {'min': 51.28, 'max': 64.75}, 
#  'BiologicalMaterial06': {'min': 44.3, 'max': 59.38}, 
#  'ManufacturingProcess13': {'min': 32.1, 'max': 38.6}}

















