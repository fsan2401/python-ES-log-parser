import json
from Parser import Parser
import datetime

"""
    Custom Parsers:

        return data: {
            "@timestamp":   formatted_date_string when available outside message 
            "message":      plain text message ## DO NOT FILL IF
            "message_data": json or additional parsed fields
            "parsed":       flag for selecting custom data 
        }

"""

def parseSyslog(p_line):
    """
    Sample of syslog object
    {'timestamp': datetime.datetime(2016, 7, 11, 19, 3, 45), 'hostname': 'cory-desktop', 'appname': 'dbus-daemon', 'pid': '1906', 'message': '[session uid=1000 pid=1906] Activating via systemd: service name=\'org.freedesktop.Tracker1.Miner.Extract\' unit=\'tracker-extract.service\' requested by \':1.2\' (uid=1000 pid=1902 comm="/usr/libexec/tracker-miner-fs " label="unconfined")'}
    """
    line = syslog_parser.parse(p_line)
    #line = str(line['appname'])+' '+str(line['pid']) +' '+str(line['message'])

    return {
        "@timestamp": formatDate( line['timestamp']),
        "message_data": json.dumps(line),
        "parsed": "syslog"
    }

def parseContainerJSONLog(p_line):
    """
    TODO: only works for json logs, add support for custom log drivers
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
    Custom logging drivers - TODO: remove special characters
    """

    return  {
        "message": p_line,
        "parsed": parsed
    }


def getParser(parse_mode):
    parseFunction = {
            "syslog": parseSyslog,
            "docker-json": parseContainerJSONLog,
            "docker-plain": parseContainerPlainLog
        }.get(parse_mode,"NA")

    if parseFunction == "NA":
        raise ValueError("No parser function defined for {}".format(parse_mode))
    
    return parseFunction     