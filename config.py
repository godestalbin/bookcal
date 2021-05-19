import os
import json
if os.name != 'nt':
    from google.cloud import secretmanager

class Config(object):
    # SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    WTF_CSRF_ENABLED = False  # Obliged to disable because cookie is not transferred in iframe
    GCLOUD_PROJECT_ID = os.environ.get('GCLOUD_PROJECT_ID')
    GOOGLE_APPLICATION_CREDENTIALS = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
    # print('GCLOUD_PROJECT_ID=', GCLOUD_PROJECT_ID)
    # print('GOOGLE_APPLICATION_CREDENTIALS=', GOOGLE_APPLICATION_CREDENTIALS)

    # Mongo keys defined at https://cloud.mongodb.com/v2/5fc2042fdc81aa5cf552a7af#clusters

    # Free mobile data to send SMS
    # https://mobile.free.fr/account/mes-options to get your API key

    def __init__(self):
        self.OS_NAME = os.name  # nt for Windows, posix for Linux
        if self.OS_NAME == 'nt':  # Windows = local dev env to avoid generating cost on Google secret manager
            from private.localconfig import LocalConfig
            self.MONGO_DB = LocalConfig.MONGO_DB
            self.DATABASE = LocalConfig.DATABASE
            self.COLLECTION = LocalConfig.COLLECTION
            self.FREE_MOBILE_SMS_GATEWAY = LocalConfig.FREE_MOBILE_SMS_GATEWAY
            self.GMAIL_PASSWORD = LocalConfig.GMAIL_PASSWORD
            self.SENDER_EMAIL = LocalConfig.SENDER_EMAIL
            self.REPLY_TO_EMAIL = LocalConfig.REPLY_TO_EMAIL
        else:
            self.MONGO_DB = Config.accessSecret(self, self.GCLOUD_PROJECT_ID, 'MONGO_DB')
            self.DATABASE = Config.accessSecret(self, self.GCLOUD_PROJECT_ID, 'DATABASE')
            self.COLLECTION = Config.accessSecret(self, self.GCLOUD_PROJECT_ID, 'COLLECTION')
            self.FREE_MOBILE_SMS_GATEWAY = json.loads(Config.accessSecret(self, self.GCLOUD_PROJECT_ID, 'FREE_MOBILE_SMS_GATEWAY'))
            self.GMAIL_PASSWORD = Config.accessSecret(self, self.GCLOUD_PROJECT_ID, 'GMAIL_PASSWORD')
            self.SENDER_EMAIL = Config.accessSecret(self, self.GCLOUD_PROJECT_ID, 'SENDER_EMAIL')
            self.REPLY_TO_EMAIL = Config.accessSecret(self, self.GCLOUD_PROJECT_ID, 'REPLY_TO_EMAIL')

    def accessSecret(self, project_id, secret_id, version='latest'):
        client = secretmanager.SecretManagerServiceClient()
        name = client.secret_version_path(project_id, secret_id, version)
        response = client.access_secret_version(name=name)
        return response.payload.data.decode('UTF-8')

