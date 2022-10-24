"""
	Global configuration options
"""
import os
import json
import logging

##GLOBAL VARIABLES
HOSTNAME = os.getenv("HOSTNAME") or "NoHost"
SITENAME = os.getenv("SITENAME") or "NoSite"

LOG_LEVEL = os.getenv("LOG_LEVEL") or "WARN"

#DATE MODIFIERS
TIMEZONE = os.getenv("TZ") or "UTC"
DATE_FORMAT = os.getenv("DATE_FORMAT") or "%Y-%m-%dT%H:%M:%S.%f"

## TIMINGS
READER_SLEEP_TIME = os.getenv("LOGREADER_SLEEP_TIME") or 10
SCANNER_SLEEP_TIME = os.getenv("LOGSCANNER_SLEEP_TIME") or 10
MULTILINE_TIME_OFFSET = os.getenv("MULTILINE_TIME_OFFSET") or 1

## PROGRAM LOGGING
FORMAT = '%(asctime)s %(message)s'
log = logging
log.basicConfig(format=FORMAT,level=LOG_LEVEL)


## ELASTICSEARCH
ELASTIC_HOST = os.getenv("ELASTIC_HOST") 
ELASTIC_USER = os.getenv("ELASTIC_USER")
ELASTIC_PASS = os.getenv("ELASTIC_PASS")
ELASTIC_INDEX = os.getenv("ELASTIC_INDEX") or "logdata"

#do_not_edit
message_prefix = '{"index": {"_index": "'+ELASTIC_INDEX+'"} } \n'

#LOGS
MOUNT_PREFIX = os.getenv("MOUNT_PREFIX") or '/data'
DOCKER_LOGS = os.getenv("DOCKER_LOGS") or '/var/lib/docker/containers'
CUSTOM_LOGS = os.getenv("CUSTOM_LOGS") or False

