"""
    LogReader Class

    Scans for new records
"""

import logparsers
from Message import Message
from pygtail import Pygtail

from Config import log,message_prefix

class LogReader():

    def __init__(self,name,path,parse_mode,containerID=""):
        self.name = name
        self.path = path
        self.parseFunction = logparsers.getParser(parse_mode)
        self.container_id = containerID
        self.reader = Pygtail(path,offset_file=name+".offset",read_from_end=True,encoding='latin-1')


    def getLines(self):
        """
        """
        newLines = []
        try:
            newLines = self.reader.readlines()
        except Exception as e:
            log.exception(e)

        if len(newLines) > 0:
            log.debug("Log {} has {} new lines @ {}".format(self.path,len(newLines),self.name))
            message_list = []
            for i, line in enumerate(newLines):
                message = Message(line,self)
                try:
                    message.setData(self.parseFunction(line))
                except Exception as e:
                    log.debug(e)

                if len(message.data['message']) > 0: #avoid empty messages
                    if (len(message_list) > 0 and message.isMultiline(prevMessage)):
                        prevMessage.appendLine(message)
                        message_list[len(message_list)-1] = message_prefix+prevMessage.getData()
                    else:
                        message_list.append(message_prefix+message.getData())
                        prevMessage = message
                else:
                    log.debug("discard empty message {}".format(message.getData()))
            return message_list
        return False
