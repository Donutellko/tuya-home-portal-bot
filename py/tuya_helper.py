from tuya_connector import openapi as tuya_connector_openapi
from py import config_helper

API_ENDPOINT = "https://openapi.tuyaeu.com"
client_id = config_helper.TUYA_SMART_CLIENT_ID
secret = config_helper.TUYA_SMART_SECRET
project_code = config_helper.TUYA_SMART_PROJECT_CODE

tuya_openapi = tuya_connector_openapi.TuyaOpenAPI(API_ENDPOINT, client_id, secret)
connect = tuya_openapi.connect()
print("Tuya connected:", connect)

async def open_portal():
    if not tuya_openapi.is_connect():
        connect = tuya_openapi.connect()
        print("Tuya reconnected:", connect)

    response = tuya_openapi.post(f"/v1.0/homes/{config_helper.TUYA_SMART_HOME_OWNER_ID}/scenes/{config_helper.TUYA_SMART_SCENE_ID}/trigger")
    print("Portal open response:", response)
    return response.get("success"), response
