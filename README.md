# python-ES-log-parser
Python agent for docker and custom logs parsing. ElasticSearch Push


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

- Add syslog and custom log support
- Define Final log Format
- Check if timezoned dates are required (ES alredy localizes client browser date)


### WORK LOG

```
  # 18-10-2022  8.45 -  9.30 - parse JSON docker sample
  # 18-10-2022 13.40 - 14.40 - docker message formats testing
  # 18-10-2022 19.40 - 20.30 - docker api (socket) testing - container scan function, directory based

  # 19-10-2022  8.15 -  9.30 - modularization and code splitting
  # 19-10-2022 10.00 - 10.40 - modularization and code splitting

  # 20-10-2022 10.00 - 11.30 - elasticsearch setup, local testing (windows)
  # 20-10-2022 18.40 - 19.30 - json message adjustment

  # 21-10-2022 10.00 - 11.30 - logging module, config module

  # 22-10-2022 14.00 - 15.30 - multiprocessing (1 log per process), ES connectivity test
  # 22-10-2022 16.00 - 19.30 - code optimization, first working project without ES push

  # 23-10-2022 19.30 - 21.00 - ElasticSearch push function
  # 23-10-2022 21.30 - 23.30 - Multiline support (java tested) and date parsers check
```


