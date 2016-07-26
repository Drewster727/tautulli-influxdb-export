
#!/usr/bin/python

import time
import argparse # for arg parsing...
import json # for parsing json
import urllib2 # for calling the api
from multiprocessing import Process
from datetime import datetime # for obtaining the curren time and formatting it
from influxdb import InfluxDBClient # via apt-get install python-influxdb

plexpy_url_format = '{0}://{1}:{2}/api/v2?apikey={3}'

def get_activity(plexpy_url,influxdb_client):
        try:
		data = json.load(urllib2.urlopen('{0}{1}'.format(plexpy_url, '&cmd=get_activity')))

		if data:
					total_stream_count = int(data['response']['data']['stream_count'])

					# loop over the streams
					sessions = data['response']['data']['sessions']
					total_stream_playing_count = 0
					transcode_stream_count = 0
					transcode_stream_playing_count = 0
					direct_stream_count = 0
					direct_stream_playing_count = 0

					for s in sessions:
						if s['video_decision'] == 'direct': # direct = 'video_decision' == 'direct' ?
							direct_stream_count += 1
							if s['state'] == 'playing':
								direct_stream_playing_count += 1
						else: # transcode = 'video_decision' == 'copy' or 'transcode'
							transcode_stream_count += 1
							if s['state'] == 'playing':
								transcode_stream_playing_count += 1
						if s['state'] == 'playing':
							total_stream_playing_count += 1

					json_body = [
							{
									"measurement": "get_activity",
									"time": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
									"fields" : {
											"stream_count": total_stream_count,
											"stream_playing_count": total_stream_playing_count,
											"stream_transcode_count": transcode_stream_count,
											"stream_transcode_playing_count": transcode_stream_playing_count,
											"stream_direct_count": direct_stream_count,
											"stream_direct_playing_count": direct_stream_playing_count
									}
							}
					]
					influxdb_client.write_points(json_body)
        except Exception:
          pass

def get_users(plexpy_url,influxdb_client):
        try:
                data = json.load(urllib2.urlopen('{0}{1}'.format(plexpy_url, '&cmd=get_users')))

                if data:
                                        users = data['response']['data']
					total_users = len(users)
 					total_home_users = 0

					for s in users:
                                                if s['is_home_user'] == '1':
                                                        total_home_users += 1

                                        json_body = [
                                                        {
                                                                        "measurement": "get_users",
                                                                        "time": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
                                                                        "fields" : {
                                                                                        "user_count": total_users,
											"home_user_count": total_home_users
                                                                        }
                                                        }
                                        ]
                                        influxdb_client.write_points(json_body)
        except Exception:
          pass

def create_database(influxdb_client, database):
	try:
		influxdb_client.query('CREATE DATABASE IF NOT EXISTS {0}'.format(database))
	except Exception:
	  pass

def init_exporting(interval, plexpy_url, influxdb_client):
	while True:
		getactivity = Process(target=get_activity, args=(plexpy_url,influxdb_client,))
		getactivity.start()
    		getactivity.join()

    		getusers = Process(target=get_users, args=(plexpy_url,influxdb_client,))
    		getusers.start()
    		getusers.join()

		time.sleep(interval)

def get_url(protocol,host,port,apikey):
	return plexpy_url_format.format(protocol,host,port,apikey)

def parse_args():
    parser = argparse.ArgumentParser(description='Export plexpy data to influxdb')
    parser.add_argument('--interval', type=int, required=False, default=5, help='Interval of export in seconds')
    parser.add_argument('--plexpywebprotocol', type=str, required=False, default="http", help='PlexPy web protocol (http)')
    parser.add_argument('--plexpyhost', type=str, required=False, default="localhost", help='PlexPy host (test.com))')
    parser.add_argument('--plexpyport', type=int, required=False, default=8181, help='PlexPy port')
    parser.add_argument('--plexpyapikey', type=str, required=True, default="", help='PlexPy API key')
    parser.add_argument('--influxdbhost', type=str, required=False, default="localhost", help='InfluxDB host')
    parser.add_argument('--influxdbport', type=int, required=False, default=8086, help='InfluxDB port')
    parser.add_argument('--influxdbuser', type=str, required=False, default="", help='InfluxDB user')
    parser.add_argument('--influxdbpassword', type=str, required=False, default="", help='InfluxDB password')
    parser.add_argument('--influxdbdatabase', type=str, required=False, default="plexpy", help='InfluxDB database')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    plexpy_url = get_url(args.plexpywebprotocol, args.plexpyhost, args.plexpyport, args.plexpyapikey)
    influxdb_client = InfluxDBClient(args.influxdbhost, args.influxdbport, args.influxdbuser, args.influxdbpassword, args.influxdbdatabase)
    create_database(influxdb_client, args.influxdbdatabase)
    init_exporting(args.interval, plexpy_url, influxdb_client)
