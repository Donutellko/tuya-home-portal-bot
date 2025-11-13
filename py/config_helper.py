import configparser

config = configparser.ConfigParser()
config.read('config.ini')
print(config.sections())
TOKENS = config["tokens"]

BOT_ACCESS_PASSWORD = TOKENS["bot-access-password"]

TELEGRAM_TOKEN = TOKENS["telegram-token"]

TUYA_SMART_CLIENT_ID = TOKENS["tuya-smart-client-id"]
TUYA_SMART_SECRET = TOKENS["tuya-smart-secret"]
TUYA_SMART_PROJECT_CODE = TOKENS["tuya-smart-project-code"]
TUYA_SMART_DEVICE_ID = TOKENS["tuya-smart-device-id"]
TUYA_SMART_HOME_OWNER_ID = TOKENS["tuya-smart-home-owner-id"]
TUYA_SMART_SCENE_ID = TOKENS["tuya-smart-scene-id"]


