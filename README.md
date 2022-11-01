# python-ES-log-parser

Python agent which scans all configured logs and starts one process for each one
- For container logs: 
  it checks container configuration and only spawns a process when the container is started
  When a container is stopped, the asociated process is terminated


- For custom logs (TODO):
  checks if file exists and is readable, then start a process

Each Process does its better effort to parse into JSON or plain text, with naive multiline detection and pushes formatted records to Elasticsearch

### Build and startup

```
git clone https://github.com/fsan2401/python-ES-log-parser.git
cd python-ES-log-parser

docker build -t  python-elastic-logger .

## See Config.py for options
docker run -ti \
    -e HOSTNAME=FSAN_LAPTOP \
    -e SITENAME=Tandil \
    -e ELASTIC_HOST=https://172.17.0.1:9200 \
    -e ELASTIC_USER=elastic \
    -e MOUNT_PREFIX=/data \
    -e ELASTIC_PASS=-GOALi-Ux8+Q9wH68wvV \
    -e LOG_LEVEL=INFO \
    -v /var/lib/docker:/data/var/lib/docker \
    --name=pyelastic
    python-elastic-logger

```


### PROPOSAL:


- Asynchronous polling by log **DONE**
- periodical directory re-scan for new containers/logs **DONE**
- Detection of multiple-line log records **DONE**
- Parsing of Container log records into JSON (whenever posible) **DONE**
- Error handling when reading, parsing or uploading data  **DONE-REVIEWING**
- Code Splitting and modularization **DONE**
- Dynamic parameters based on configuration or environment **DONE**


### WORK IN PROGRESS

- **DONE** MULTILINE RECORDS: added some patterns for java, still checking possible patterns
- **DONE** ERROR HANDLING: all necessary exceptions are logged for further analysis, still checking some unhandled errors
- **DONE** CONFIGURATION: working on Dockerfile and startup script to set main configurations and validations

### TODOs

- **DONE** Code Comments 
- **DONE** Add syslog support
- **DONE** Add common format Parsers
- Adjust Final log Format
- Check if timezoned dates are required (ES alredy localizes client browser date)
- Exclude current container DEBUG log to avoid trash push to elastic
- Customize offset file directory ( to be shared so offsetfiles aren't lost on container rebuild)
- Handle data when ES upload fails (discard, log, save to disk to upload when ES is available)
- 2022-11-01 - Re-Compile docker container and test missing
- 2022-11-01 - Docker container custom logging review missing
