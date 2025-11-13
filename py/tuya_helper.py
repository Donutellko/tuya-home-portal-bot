from tuya_iot import *
from tuya_iot import openapi as tuya_iot_openapi
from tuya_connector import openapi as tuya_connector_openapi
from py import config_helper

API_ENDPOINT = "https://openapi.tuyaeu.com"
client_id = config_helper.TUYA_SMART_CLIENT_ID
secret = config_helper.TUYA_SMART_SECRET
project_code = config_helper.TUYA_SMART_PROJECT_CODE

# import tinytuya

# tuya_cloud = tinytuya.Cloud(apiRegion = API_ENDPOINT, apiKey = client_id, apiSecret = secret)
# API_ENDPOINT: cn, us, us-e, eu, eu-w, or in. Options based on tinytuya python library

# tuya_openapi = tuya_iot_openapi.TuyaOpenAPI(API_ENDPOINT, client_id, secret)
tuya_openapi_2 = tuya_connector_openapi.TuyaOpenAPI(API_ENDPOINT, client_id, secret)
connect = tuya_openapi_2.connect()
# connect = tuya_openapi.connect()
# print(connect)
#
# tuya_mq = TuyaOpenMQ(tuya_openapi)
# tuya_mq.start()
#
# device_manager = TuyaDeviceManager(tuya_openapi, tuya_mq)
# home_manager = TuyaHomeManager(tuya_openapi, tuya_mq, device_manager)

# print(home_manager.query_scenes())

# print(tuya_openapi.is_connect())

async def open_portal():
    # openapi = TuyaOpenAPI(API_ENDPOINT, config_helper.TUYA_SMART_CLIENT_ID, config_helper.TUYA_SMART_SECRET)
    # tuya_openapi_2.connect()
    if not tuya_openapi_2.is_connect():
        connect = tuya_openapi_2.connect()

    response = tuya_openapi_2.post(f"/v1.0/homes/{config_helper.TUYA_SMART_HOME_OWNER_ID}/scenes/{config_helper.TUYA_SMART_SCENE_ID}/trigger")
    print("Portal open response:", response)
    return response.get("success"), response


async def trigger_scene() -> None:
    """Trigger a scene in the Tuya home."""


    scenes = home_manager.query_scenes()

    if not scenes:
        print("No scenes found.")
        return

    # Assuming we want to trigger the first scene
    scene: TuyaScene = scenes[0]
    response = home_manager.trigger_scene(scene.home_id, scene.scene_id)

    if response.get("success", False):
        print(f"Scene '{scene.name}' triggered successfully.")
    else:
        print(f"Failed to trigger scene '{scene.name}': {response.get('msg', 'Unknown error')}")

