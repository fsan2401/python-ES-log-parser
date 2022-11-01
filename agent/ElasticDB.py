"""
    Elasticsearch module

    ## TODO - define if BasicAuth fits
"""
import requests
import urllib3

from requests.auth import HTTPBasicAuth
from Config import ELASTIC_HOST,ELASTIC_USER,ELASTIC_PASS,ELASTIC_KEY,ELASTIC_AGENTID,log

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class ElasticDB():

    def __init__(self):
        self.push_url = ELASTIC_HOST+'/_bulk'
        self.health_url = ELASTIC_HOST+'/_cat/health'

        if ELASTIC_USER and ELASTIC_PASS:
            self.auth = HTTPBasicAuth(ELASTIC_USER,ELASTIC_PASS)
            self.headers = headers = {'content-type': 'application/json' }
        else:
            if ELASTIC_KEY and ELASTIC_AGENTID:
                self.auth = False
                self.headers = headers = {
                    'content-type': 'application/json', 
                    'X-Auth-PassCode': ELASTIC_KEY, 
                    'X-Auth-AgentID': ELASTIC_AGENTID
                }
            else:
                raise ValueError("Must provide elastic authentication USER+PASS or KEY+AGENTID")



    def isAlive(self):
        """
        Connectivity Test
        """        
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
        """
        Sends log data to database
        """
        data = '\n'.join(payload)+"\n";
        #log.debug("sending payload: {}".format(data));
        try:
            res = requests.post(self.push_url,headers=self.headers,auth=self.auth, data = data,verify=False)
            #log.debug("response: {} {} ".format(res.status_code,res.text))
            if (res.status_code != 200):
                raise ValueError("Problematic payload")
            if res.json()['errors'] == True:
                raise ValueError("Problematic payload")
        except Exception as e:
            self.saveProblematicPayload(data)
            log.error(e)
            log.error("response: {} {} ".format(res.status_code,res.text[0:300]))


    def saveProblematicPayload(self,payload):
        """
        TODO: define if problematic payload should be saved
        """
        log.info("PROBLEMATIC PAYLOAD: {}".format(payload))