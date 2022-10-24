import requests
from requests.auth import HTTPBasicAuth

import Config

class TargetDatabase():
    def __init__(self):
        self.host = Config.ELASTIC_HOST
        self.user = Config.ELASTIC_USER
        self.password = Config.ELASTIC_PASS
        self.auth = HTTPBasicAuth(user,password)

        self.push_url = '/_bulk'
        self.health_url = '/_cat/health'
        #self.headers = headers = {'content-type': 'application/json', 'X-Auth-PassCode': self.key, 'X-Auth-AgentID': self.agentID}
        self.headers = headers = {'content-type': 'application/json' }

    def isAlive(self):
        try:
            req = requests.get(self.health_url,headers=headers,auth=self.auth)
            if (req.status_code == 200):
                return True
            return False
        except:
            return False

    def pushLogs(payload):
        print(payload.join('\n'))