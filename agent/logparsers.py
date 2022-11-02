"""
    Custom Parsers:

        return data: {
            "@timestamp":   formatted_date_string when available outside message 
            "message":      plain text message ## DO NOT FILL IF
            "message_data": json or additional parsed fields
            "parsed":       flag for selecting custom data 
        }

"""
import json
import re
from Config import log 

syslog_regex = r'(?P<date>\w{3}\s\d+\s\d{2}:\d{2}:\d{2})\s(?P<host>\S+)\s(?P<app>\S+)(\[(?P<pid>\d+)\]):(?P<message>.*)$'
syslog_reg_nopid = r'^(?P<date>\w{3}\s\d+\s\d{2}:\d{2}:\d{2})\s(?P<host>\S+)\s(?P<app>\S+):(?P<message>.*)'


def parseSyslog(p_line):
    """
    Custom Log parsing
    """
    matches = re.match(syslog_regex, p_line, re.MULTILINE)
    matchedobj = {}
    if matches is not None:
        matchedobj = matches.groupdict()
        log.debug("line: {} Matches: {}".format(p_line,matchedobj))
    else:
        matches = re.match(syslog_reg_nopid, p_line, re.MULTILINE)
        if matches is not None:
            matchedobj = matches.groupdict()
            log.debug("line: {} Matches: {}".format(p_line,matchedobj))

    return {
        "@timestamp": matchedobj.get('date'),
        "message_data": matchedobj,
        "parsed": "syslog"
    }


def parseContainerJSONLog(p_line):
    """
     Docker container json log parsing
    """ 
    j = json.loads(p_line.strip('\\r\\n'));
    try:
        ## j.log is json
        return  {
            "@timestamp": j['time'],
            "message_data": json.loads(j['log'].strip('\\r\\n')),
            "parsed": "json"
        }
    except Exception as e:
        ## j.log not json, return text in message
        return  {
            "@timestamp": j['time'],
            "message": j['log'],
            "parsed": "text"
        }
   

def parseContainerPlainLog(p_line):
    """
    Docker Custom logging drivers syslog, local (not json)
    """
    #TODO: remove special characters

    return  {
        "message": p_line[19:-3],
        "parsed": False
    }


def getParser(parse_mode):
    """
        Select parser based on configuration
    """
    parseFunction = {
            "syslog": parseSyslog,
            "docker-json": parseContainerJSONLog,
            "docker-plain": parseContainerPlainLog
        }.get(parse_mode,"NA")

    if parseFunction == "NA":
        raise ValueError("No parser function defined for {}".format(parse_mode))
    
    return parseFunction     