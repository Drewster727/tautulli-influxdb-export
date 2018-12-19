# tautulli-influxdb-export

This script will query Tautulli to pull basic stats and store them in influxdb. Stay tuned for further additions!

I suggest you intall the script as a service to boot with your OS.

## Dependencies
  * Tautulli (aka PlexPy) (https://github.com/Tautulli/Tautulli)
  * Python (v2.7.x)
  * InfluxDB (https://github.com/influxdata/influxdb)
  * InfluxDB Python Client (https://github.com/influxdata/influxdb-python)
    - install on linux via 'apt-get install python-influxdb'

## Parameters
  * --interval (in seconds, default: 5)
  * --tautulliwebprotocol (http/https, default: http)
  * --tautullihost (default, localhost)
  * --tautulliport (default: 8181)
  * --tautulliapikey (required, default: empty)
  * --tautullibaseurl (default: empty)
  * --influxdbhost (default: localhost)
  * --influxdbport (default: 8086)
  * --influxdbuser (default: empty)
  * --influxdbpassword (default: empty)
  * --influxdbdatabase (default: tautulli)

## Example

  ```
  python /path/to/tautulli_influxdb_export.py --tautullihost <host> --tautulliapikey <key>
  ```

## Docker Example

  ```
  cd <folder>
  docker build -t tautulli_influxdb_export .
  docker run -d --name=tautulli_influxdb_export --restart unless-stopped -e TAUTULLI_HOST=<host> -e TAUTULLI_KEY=<key> -e INFLUXDB_HOST=<influxdbhost> -e INFLUXDB_DB=<influxdbdatabase> tautulli_influxdb_export
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
    - *#* Users currently streaming concurrently
    - *#* Users currently streaming conurrently (with different IP addresses)
  * Libraries
    - *#* Total Items Per Library
  * more to come...

### To Do:
  * Activity
    - *#* Audio Transcode Streams
    - *#* Audio Transcode Streams (Playing)
    - *#* Audio Direct Play Streams
    - *#* Audio Direct Play Streams (Playing)
  * Users
    - Current Streaming Users Location Data (via IP lookup)

## Use-Case
  With the data exported to influxdb, you can create some useful stats/graphs in graphing tools such as grafana (http://grafana.org/)

  ![alt tag](https://cloud.githubusercontent.com/assets/4528753/17122931/7176e2aa-52a5-11e6-8ff1-89ab6a8e7f82.png)
