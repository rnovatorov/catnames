import requests
from sovyak import app


class VKOAuther(object):


    def __init__(self, VK_APP_ID, VK_APP_SECRET,
                 VK_REDIRECT_URI="http://ovz1.novrr.6pqj1.vps.myjino.ru", # "https://oauth.vk.com/blank.html",
                 VK_API_VERSION="5.63"):
        self.VK_APP_ID = VK_APP_ID
        self.VK_APP_SECRET = VK_APP_SECRET
        self.VK_REDIRECT_URI = VK_REDIRECT_URI
        self.VK_API_VERSION = VK_API_VERSION

    def compose_auth_url(self, VK_PERMISSIONS=""):
        return ("https://oauth.vk.com/authorize?"
                "client_id={VK_APP_ID}&"
                "scope={VK_PERMISSIONS}&"
                "redirect_uri={VK_REDIRECT_URI}&"
                "response_type=code&"
                "v={VK_API_VERSION}".format(**{
                    "VK_APP_ID": self.VK_APP_ID,
                    "VK_PERMISSIONS": VK_PERMISSIONS,
                    "VK_REDIRECT_URI": self.VK_REDIRECT_URI,
                    "VK_API_VERSION": self.VK_API_VERSION
                }))


    def _compose_token_url(self, VK_CODE):
        return ("https://oauth.vk.com/access_token?"
                "client_id={VK_APP_ID}&"
                "client_secret={VK_APP_SECRET}&"
                "code={VK_CODE}&"
                "redirect_uri={VK_REDIRECT_URI}".format(**{
                    "VK_APP_ID": self.VK_APP_ID,
                    "VK_APP_SECRET": self.VK_APP_SECRET,
                    "VK_CODE": VK_CODE,
                    "VK_REDIRECT_URI": self.VK_REDIRECT_URI
                }))

    def get_access_token(self, VK_CODE):
        token_url = self._compose_token_url(VK_CODE)
        try:
            response = requests.get(token_url)
            return response.json()
        except Exception as e:
            app.logger.error(e)
            return None
