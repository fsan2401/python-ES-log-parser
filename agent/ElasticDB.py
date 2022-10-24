import requests
from requests.auth import HTTPBasicAuth


import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from Config import ELASTIC_HOST,ELASTIC_USER,ELASTIC_PASS,log

class ElasticDB():
    def __init__(self):
        self.auth = HTTPBasicAuth(ELASTIC_USER,ELASTIC_PASS)
        self.push_url = ELASTIC_HOST+'/_bulk'
        self.health_url = ELASTIC_HOST+'/_cat/health'
        #self.headers = headers = {'content-type': 'application/json', 'X-Auth-PassCode': self.key, 'X-Auth-AgentID': self.agentID}
        self.headers = headers = {'content-type': 'application/json' }

    def isAlive(self):
        try:
            req = requests.get(self.health_url,headers=self.headers,auth=self.auth, verify=False)
            if (req.status_code == 200):
                log.debug(req)
                return True
            return False
        except Exception as e:
            log.debug(e)
            return False

    def pushLogs(self,payload):
        data = '\n'.join(payload)+"\n";
      #  log.debug("sending payload: {}".format(data));
        try:
            res = requests.post(self.push_url,headers=self.headers,auth=self.auth, data = data,verify=False)
           # log.debug("response: {} {} ".format(res.status_code,res.text))
            if (res.status_code != 200):
                raise ValueError("Problematic payload")
            if res.json()['errors'] == True:
                raise ValueError("Problematic payload")
        except Exception as e:
            self.saveProblematicPayload(data)
            log.exception(e)
            log.error("response: {} {} ".format(res.status_code,res.text[0:300]))

    def saveProblematicPayload(self,payload):
        """
        TODO: define if problematic payload should be saved
        """
        log.info("PROBLEMATIC PAYLOAD: {}".format(payload))