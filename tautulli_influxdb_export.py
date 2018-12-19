#!/usr/bin/python
from __future__ import print_function
from builtins import str

import os
import time
import configargparse # for arg parsing...
import json # for parsing json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from multiprocessing import Process
from datetime import datetime, timedelta # for obtaining the curren time and formatting it
from influxdb import InfluxDBClient # via apt-get install python-influxdb
requests.packages.urllib3.disable_warnings(InsecureRequestWarning) # suppress unverified cert warnings

tautulli_url_format = '{0}://{1}:{2}{4}/api/v2?apikey={3}'

def main():
    print("Started")
    args = parse_args()
    tautulli_url = get_url(args.tautulliwebprotocol, args.tautullihost, args.tautulliport, args.tautulliapikey, args.tautullibaseurl)
    influxdb_client = InfluxDBClient(args.influxdbhost, args.influxdbport, args.influxdbuser, args.influxdbpassword, args.influxdbdatabase)
    create_database(influxdb_client, args.influxdbdatabase)
    init_exporting(args.interval, tautulli_url, influxdb_client)

def parse_args():
    parser = configargparse.ArgumentParser(
        description='Export tautulli data to influxdb')
    parser.add_argument('--interval', type=int, required=False,
                        env_var='INTERVAL', default=5,
                        help='Interval of export in seconds')
    parser.add_argument('--tautulliwebprotocol', type=str, required=False,
                        env_var='tautulliWEBPROTOCOL', default="http",
                        help='tautulli web protocol (http)')
    parser.add_argument('--tautullihost', type=str, required=False,
                        env_var='tautulliHOST', default="localhost",
                        help='tautulli host (test.com))')
    parser.add_argument('--tautulliport', type=int, required=False,
                        env_var='tautulliPORT',
                        default=8181, help='tautulli port')
    parser.add_argument('--tautulliapikey', type=str, required=True,
                        env_var='tautulliAPIKEY', default="",
                        help='tautulli API key')
    parser.add_argument('--tautullibaseurl', type=str, required=False,
                        env_var='tautulliBASEURL', default='',
                        help='Base/Root url for tautulli')
    parser.add_argument('--influxdbhost', type=str, required=False,
                        env_var='INFLUXDBHOST', default="localhost",
                        help='InfluxDB host')
    parser.add_argument('--influxdbport', type=int, required=False,
                        env_var='INFLUXDBPORT', default=8086,
                        help='InfluxDB port')
    parser.add_argument('--influxdbuser', type=str, required=False,
                        env_var='INFLUXDBUSER', default="",
                        help='InfluxDB user')
    parser.add_argument('--influxdbpassword', type=str, required=False,
                        env_var='INFLUXDBPASSWORD', default="",
                        help='InfluxDB password')
    parser.add_argument('--influxdbdatabase', type=str, required=False,
                        env_var='INFLUXDBDATABASE', default="tautulli",
                        help='InfluxDB database')
    return parser.parse_args()

def get_activity(tautulli_url,influxdb_client):
    try:
        data = requests.get('{0}{1}'.format(tautulli_url, '&cmd=get_activity'), verify=False).json()

        if data:
            total_stream_count = int(data['response']['data']['stream_count'])

            # loop over the streams
            sessions = data['response']['data']['sessions']
            users = {}
            total_stream_playing_count = 0
            transcode_stream_count = 0
            transcode_stream_playing_count = 0
            direct_play_stream_count = 0
            direct_play_stream_playing_count = 0
            direct_stream_stream_count = 0
            direct_stream_stream_playing_count = 0
            concurrent_stream_user_count = 0
            concurrent_stream_user_diffip_count = 0

            for s in sessions:
                # check for concurrent streams
                su = s['user']
                ip = s['ip_address']
                if su in users:
                    concurrent_stream_user_count += 1
                    if ip not in users[su]:
                        users[su].append(ip)
                else:
                    users[su] = [ip]

                playing = s['state'] == 'playing'
                if s['transcode_decision'] == 'direct play':
                    direct_play_stream_count += 1
                    if playing:
                        direct_play_stream_playing_count += 1
                else:
                    if s['video_decision'] == 'copy':
                        direct_stream_stream_count += 1
                        if playing:
                            direct_stream_stream_playing_count += 1
                    else: # transcode = 'transcode'
                        transcode_stream_count += 1
                        if playing:
                            transcode_stream_playing_count += 1

                if s['state'] == 'playing':
                    total_stream_playing_count += 1

            # determine how many concurrent users with diff IPs we have
            for k,v in list(users.items()):
                if len(v) > 1:
                    concurrent_stream_user_diffip_count += 1

            json_body = [
                    {
                            "measurement": "get_activity",
                            "time": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
                            "fields" : {
                                    "stream_count": total_stream_count,
                                    "stream_playing_count": total_stream_playing_count,
                                    "stream_transcode_count": transcode_stream_count,
                                    "stream_transcode_playing_count": transcode_stream_playing_count,
                                    "stream_directplay_count": direct_play_stream_count,
                                    "stream_directplay_playing_count": direct_play_stream_playing_count,
                                    "stream_directstream_count": direct_stream_stream_count,
                                    "stream_directstream_playing_count": direct_stream_stream_playing_count,
                                    "user_concurrent_count": concurrent_stream_user_count,
                                    "user_concurrent_diffip_count": concurrent_stream_user_diffip_count
                            }
                    }
            ]

            influxdb_client.write_points(json_body)

    except Exception as e:
        print(str(e))
        pass

def get_users(tautulli_url,influxdb_client):
    try:
        data = requests.get('{0}{1}'.format(tautulli_url, '&cmd=get_users'), verify=False).json()

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
    except Exception as e:
        print(str(e))
        pass

def get_libraries(tautulli_url,influxdb_client):
    try:
        data = requests.get('{0}{1}'.format(tautulli_url, '&cmd=get_libraries'), verify=False).json()

        if data:
            libraries = data['response']['data']
            utcnow = datetime.utcnow()
            json_body = []

            for l in libraries:
                utcnow = utcnow + timedelta(milliseconds=1)
                json_body.append({
                    "measurement": "get_libraries",
                    "time": utcnow.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                    "fields" : {
                        "section_name": l['section_name'],
                        "section_type": l['section_type'],
                        "count": num(l.get('count', 0)),
                        "child_count": num(l.get('child_count', 0))
                    }
                })

            influxdb_client.write_points(json_body)
    except Exception as e:
        print(str(e))
        pass

def num(s):
    try:
        return int(s)
    except ValueError:
        return float(s)

def create_database(influxdb_client, database):
    try:
        influxdb_client.query('CREATE DATABASE {0}'.format(database))
    except Exception as e:
        print(str(e))
    pass

def init_exporting(interval, tautulli_url, influxdb_client):
    while True:
        getactivity = Process(target=get_activity, args=(tautulli_url,influxdb_client,))
        getactivity.start()

        getusers = Process(target=get_users, args=(tautulli_url,influxdb_client,))
        getusers.start()

        getlibs = Process(target=get_libraries, args=(tautulli_url,influxdb_client,))
        getlibs.start()

        time.sleep(interval)

def get_url(protocol,host,port,apikey,baseurl):
    base = ""
    if baseurl:
        base = "/{}".format(baseurl)

    return tautulli_url_format.format(protocol,host,port,apikey,base)

if __name__ == '__main__':
    main()
