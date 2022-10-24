"""
    Message Class
"""

from datetime import datetime
import json
import os
#import pytz
import dateutil.parser
import re 

from Config import HOSTNAME,SITENAME,DATE_FORMAT,MULTILINE_TIME_OFFSET,log

multiline_regex = r"^(\t|\s\s|\\u0009\\u0009).*$"
dateregex = "(\d{4}(-|\/)\d{2}(-|\/)\d{2}T?\s?\d{2}:\d{2}:\d{2}(\.|,)?\d*(|-|\+)?.*?)(\s|\])"


def formatDate(date_obj):
    #local_time = pytz.timezone(timeZone)
    #local_datetime = local_time.localize(naive_datetime, is_dst=None)
    #utc_datetime = local_datetime.astimezone(pytz.utc)
    return date_obj.strftime(DATE_FORMAT);




class Message():
    def __init__(self,line,reader):
        
        self.parsed_date = False
        self.data = {
            "hostName": HOSTNAME,
            "siteName": SITENAME,
            "logFile":  reader.path,
            "container": reader.name,
            "message": line,
            "parsed": "false"
        }

    def extractDate(self):
        try:
            matches = re.match(dateregex, self.data['message'], re.MULTILINE)
            log.debug("line: {} Matches: {}".format(self.data['message'],matches))
            if matches is not None:
                return dateutil.parser.parse(matches[0])
        except:
            #log.exception(e)
            return False

    def setData(self,payload):

        for key in payload:
            self.data[key] = payload[key];

        ## if no timestamp, try to extract from message
        if not '@timestamp' in self.data.keys():
            parsed_date = self.extractDate()
            self.data['@timestamp'] = formatDate(parsed_date or datetime.now)
            self.parsed_date = parsed_date
        else:
            self.parsed_date =  dateutil.parser.parse(self.data['@timestamp'])
            self.data['@timestamp'] = formatDate(self.data['@timestamp'])




    def getData(self):
        log.debug("current message: {} {}".format(self.data,self.parsed_date))

        ## remove unnecesary fields here
        removekeys = [] # ['parsed','original_date']
        for key in removekeys:
            if key in self.data:
                del self.data[key]

        return json.dumps(self.data);


    def appendLine(self,new_message):
       # print("NMD: {}" new_message.data)
        self.data['message'] += new_message.data['message']

    def isMultiline(self,prevMessage):
        """
            
        """
        #json is never multiline
        if self.data['parsed'] == "json": 
            return False

        if not self.parsed_date or not prevMessage.parsed_date:
            return False

        datediff = abs((self.parsed_date-prevMessage.parsed_date).total_seconds())
        #if date is out of range, different message
        if datediff > MULTILINE_TIME_OFFSET:
            return False

        #try to match common multiline patterns
        matches = re.match(multiline_regex, self.data["message"], re.MULTILINE)
        log.debug("line: {} Matches: {}".format(self.data["message"],matches))
        if matches is not None:
            return True
        return False

