import requests
import urllib.parse
from config import Config

class SendSms:
    def __init__(self):
        self.config = Config()

    def sendMessage(self, msg):
        for freeMobile in self.config.FREE_MOBILE_SMS_GATEWAY:
            response = requests.get('https://smsapi.free-mobile.fr/sendmsg?user=' + freeMobile['userId'] + '&pass=' + freeMobile['apiKey'] + '&msg=' + urllib.parse.quote(msg))
            # if response.status_code == 200: print('Send SMS, success')
            # else: print('Send SMS, failed')


# sendSms = SendSms()
# sendSms.sendMessage('Hello')