# plexpy-influxdb-export

This script will query your PlexPy to pull basic stats and store them in influxdb. Stay tuned for further additions!

I suggest you intall the script as a service to boot with your OS.

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
  With the data exported to influxdb, you can create some useful stats/graphs in graphing tools such as grafana (http://grafana.org/)
  
  ![alt tag](https://cloud.githubusercontent.com/assets/4528753/17122931/7176e2aa-52a5-11e6-8ff1-89ab6a8e7f82.png)
  
  
