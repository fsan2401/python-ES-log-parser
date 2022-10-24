from Config import DOCKER_LOGS,MOUNT_PREFIX,log
from os import listdir,path,access,R_OK
from os.path import isfile
import json

def getDockerLogs():
    """
    Scans a docker containers directory for child folders 
    and loads name and logfile from container conf

    TODO: review custom logging drivers
    """ 
    list_of_containers = [];
    try:
        docker_directory = MOUNT_PREFIX+DOCKER_LOGS
        log.debug(docker_directory)
        for container_folder in listdir(docker_directory):
            full_path=path.join(docker_directory,container_folder)
            if path.isdir(full_path):
                possible_config_file=path.join(full_path, "config.v2.json")
                if isfile(possible_config_file):
                    container_config_data=json.load(open(possible_config_file,))

                    container_ID = str(container_config_data["ID"]).strip("/")
                    container_name = str(container_config_data["Name"]).strip("/")
                    log_path = container_config_data['LogPath']
                    running = container_config_data['State']['Running']

                    ##REVIEW TTHIS BLOCK
                    if log_path == "":
                        cached_log = path.join(full_path,"container-cached.log")
                        local_logs = path.join(full_path,"local_logs/container.log")
                        if isfile(cached_log) and access(cached_log,R_OK):
                            log_path = cached_log
                            parse_mode = "docker-plain"
                            isFile = True
                            isaccesible = True
                        if isfile(local_logs) and access(local_log,R_OK):
                            log_path = local_log
                            parse_mode = "docker-plain"
                            isFile = True
                            isaccesible = True
                    else:
                        log_path = MOUNT_PREFIX+log_path
                        isFile = isfile(log_path) 
                        isaccesible = access(log_path, R_OK)
                        parse_mode = "docker-json"

                    log.debug("container {} (id: {}) log: {} running: {} isfile: {} isaccessible: {}".format(
                                    container_name, container_ID,log_path,running,isFile,isaccesible ))

                    list_of_containers.append({ 
                        "logID" :container_ID,
                        "name": container_name,
                        "isValid": running and isFile and isaccesible,
                        "path": log_path,
                        "parse_mode":parse_mode
                    })
        return list_of_containers

    except Exception as e:
        log.exception(e)
        exit(2)