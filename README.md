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

## See Config.py for 
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
- Detection of multiple-line log records **DONE-REVIEWING**
- Parsing of Container log records into JSON (whenever posible) **DONE**
- Error handling when reading, parsing or uploading data  **DONE-REVIEWING**
- Code Splitting and modularization **DONE**
- Dynamic parameters based on configuration or environment **DONE-REVIEWING**


### WORK IN PROGRESS

- MULTILINE RECORDS: added some patterns for java, still checking possible patterns
- ERROR HANDLING: all necessary exceptions are logged for further analysis, still checking some unhandled errors
- CONFIGURATION: working on Dockerfile and startup script to set main configurations and validations

### TODOs

- Code Comments 
- Add syslog and custom log support
- Add common format Parsers
- Adjust Final log Format
- Check if timezoned dates are required (ES alredy localizes client browser date)
- Exclude current container DEBUG log to avoid trash push to elastic
- Customize offset file directory ( to be shared so offsetfiles aren't lost on container rebuild)
- Handle data when ES upload fails (discard, log, save to disk to upload when ES is available)


### WORK LOG

```
  # 18-10-2022  8.45 -  9.30 - parse JSON docker sample
  # 18-10-2022 13.40 - 14.40 - docker message formats testing
  # 18-10-2022 19.40 - 20.30 - docker api (socket) testing - container scan function, directory based
  Hours: 2

  # 19-10-2022  8.15 -  9.30 - modularization and code splitting
  # 19-10-2022 10.00 - 11.10 - modularization and code splitting
  Hours: 2

  # 20-10-2022 10.00 - 11.30 - elasticsearch setup, local testing (windows)
  # 20-10-2022 18.00 - 19.30 - json message adjustment
  Hours: 3

  # 21-10-2022 10.00 - 11.30 - logging module, config module, ES module
  Hours: 1

  # 22-10-2022 14.00 - 15.30 - multiprocessing (1 log per process), ES connectivity test
  # 22-10-2022 16.00 - 18.00 - code optimization, first working project without ES push
  Hours: 3

  # 23-10-2022 20.30 - 21.30 - Multiline support (java tested) and date parsers check
  # 23-10-2022 22.30 - 23.30 - Dockerfile + Git push 
  Hours: 2

TOTAL Hours: 13

```


