import requests_oauthlib
from requests_oauthlib import OAuth2Session
import webbrowser
import json
import re

from appFuncs import getConfig as getConfig
from appFuncs import saveConfig as saveConfig
from appFuncs import authorize as authorize
from appFuncs import parseAuthCode as parseAuthCode
from appFuncs import accessToken as accessToken

tokenConfigFile = 'tokenConfig'

conf = getConfig(tokenConfigFile)
auth = authorize(tokenConfigFile)

webbrowser.open_new_tab(auth)

try:
    while True:
        with open("temp.html", "r") as f:
            lines = f.readlines()
            for line in lines:
                match = re.search(r"code=([\w-]+)&state=([\w-]+)", line)
                if match:
                    conf['auth_code'] = match.group(1)
                    conf['state'] = match.group(2)
                    break
        if conf.get('auth_code'):
            break
except FileNotFoundError:
    pass

accToken = accessToken(conf)
print('\n\n' + str(accToken) + '\n\n')
print(conf['auth_code'])

conf['access_token'] = accToken['access_token']
conf['refresh_token'] = accToken['refresh_token']
conf['expires_at'] = accToken['expires_at']
token = {'access_token': conf['access_token'], 'token_type': 'Bearer' }
saveConfig(tokenConfigFile, conf)
