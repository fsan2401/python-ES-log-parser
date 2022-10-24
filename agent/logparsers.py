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
from Parser import Parser
import datetime


def parseSyslog(p_line):
    """
    Custom Log parsing
    """
    #TODO - evaluate regexes, format json according to parsed data

    line = syslog_parser.parse(p_line)
    #line = str(line['appname'])+' '+str(line['pid']) +' '+str(line['message'])
    return {
        "@timestamp": formatDate( line['timestamp']),
        "message_data": json.dumps(line),
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
        "message": p_line,
        "parsed": parsed
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