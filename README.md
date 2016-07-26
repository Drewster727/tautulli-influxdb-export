# plexpy-influxdb-export

This script will query your PlexPy to pull basic stats and store them in influxdb

## Parameters
  * --interval (in seconds, default: 5)
  * --plexpywebprotocol (default: http)
  * --plexpyhost (default, localhost)
  * --plexpyport (default: 8181)
  * --plexpyapikey (required, default: empty)
  * --influxdbhost (default: localhost)
  * --influxdbport (default: 8086)
  * --influxdbuser (default: empty)
  * --influxdbpassword (default: empty)
  * --influxdbdatabase (default: plexpy)

## Example

  ```
  python /path/to/plexpy_export_influxdb.py --plexpyhost <host> --plexpyapikey <key>
  ```
  
## Use-Case
  With this data exported to influxdb, you can create some useful stats/graphs in graphing tools such as grafana (http://grafana.org/)
  
  
