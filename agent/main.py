from multiprocessing import Process
from time import sleep
from Config import log, DOCKER_LOGS, CUSTOM_LOGS, MOUNT_PREFIX, SCANNER_SLEEP_TIME, READER_SLEEP_TIME

from ElasticDB import ElasticDB
from LogReader import LogReader
import scanners


def scanLoop(log_reader,target_database):
    
    log.info("Starting with {} path: {}".format(log_reader.name, log_reader.path))
    while True:
        payload = log_reader.getLines()
        if payload:
            target_database.pushLogs(payload)
        sleep(READER_SLEEP_TIME)


def startProcess(log):
    current_logreader = LogReader(log['name'],log['path'],log['parse_mode'],log["logID"])
    p = Process(target=scanLoop, args=(current_logreader,target_database,))
    p.start()
    return p


if __name__ == "__main__":

    try:
        target_database = ElasticDB()
        if not target_database.isAlive():
            log.error("Remote Database is not responding")
            exit(2)

        process_list = {}


        while True:

            log_list = []
            if (DOCKER_LOGS):
                log_list.extend(scanners.getDockerLogs())
            if (CUSTOM_LOGS):
                log_list.extend(scanners.getCustomLogs())
            
            for i in range(len(log_list)):
                log_data = log_list[i]
                log_id = log_data['logID']
                log_is_valid = log_data['isValid']

                if log_is_valid:
                    if not log_id in process_list.keys(): 
                        process_list[log_id] = startProcess(log_data)
                    else:
                        if not process_list[log_id].is_alive():
                            process_list[log_id] = startProcess(log_data)
                else:
                    if ( log_id in process_list.keys() and
                            isinstance(process_list[log_id],Process) and
                            process_list[log_id].is_alive()):
                        log.info("Stopping watcher for {}".format(log_id))
                        process_list[log_id].terminate()            
                        del process_list[log_id]

            sleep(SCANNER_SLEEP_TIME)

    except Exception as e:
        log.exception(e)
        exit(2)