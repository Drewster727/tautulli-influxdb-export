# plexpy-influxdb-export

This script will query PlexPy to pull basic stats and store them in influxdb. Stay tuned for further additions!

I suggest you intall the script as a service to boot with your OS.

## Dependencies
  * PlexPy (https://github.com/drzoidberg33/plexpy)
  * Python
  * InfluxDB (https://github.com/influxdata/influxdb)
  * InfluxDB Python Client (https://github.com/influxdata/influxdb-python)
    - install on linux via 'apt-get install python-influxdb'

## Parameters
  * --interval (in seconds, default: 5)
  * --plexpywebprotocol (http/https, default: http)
  * --plexpyhost (default, localhost)
  * --plexpyport (default: 8181)
  * --plexpyapikey (required, default: empty)
  * --plexpybaseurl (default: empty)
  * --influxdbhost (default: localhost)
  * --influxdbport (default: 8086)
  * --influxdbuser (default: empty)
  * --influxdbpassword (default: empty)
  * --influxdbdatabase (default: plexpy)

## Example

  ```
  python /path/to/plexpy_influxdb_export.py --plexpyhost <host> --plexpyapikey <key>
  ```

## Exported Data
  * Activity
    - *#* Total Streams
    - *#* Total Streams (Playing)
    - *#* Transcode Streams
    - *#* Transcode Streams (Playing)
    - *#* Direct Play Streams
    - *#* Direct Play Streams (Playing)
  * Users
    - *#* Total Users
    - *#* Home Users
  * more to come...
  
### To Do:
  * Activity
    - *#* Audio Transcode Streams
    - *#* Audio Transcode Streams (Playing)
    - *#* Audio Direct Play Streams
    - *#* Audio Direct Play Streams (Playing)
  * Users
    - Current Streaming Users Location Data (via IP lookup)
  * Home Page Stats
    - *#* Concurrent Streams
    - *#* Concurrent Streams w/ different IP addresses
  * Library Stats
    - *#* Movies
    - *#* TV Shows
    - *#* Albums

## Use-Case
  With the data exported to influxdb, you can create some useful stats/graphs in graphing tools such as grafana (http://grafana.org/)
  
  ![alt tag](https://cloud.githubusercontent.com/assets/4528753/17122931/7176e2aa-52a5-11e6-8ff1-89ab6a8e7f82.png)
  
  
