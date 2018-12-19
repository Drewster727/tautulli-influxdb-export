FROM python:3
ENV INTERVAL 5
ENV TAUTULLI_HOST localhost
ENV TAUTULLI_PORT 8181
ENV TAUTULLI_KEY NONE
ENV TAUTILLI_BASE_URL NONE
ENV INFLUXDB_HOST localhost
ENV INFLUXDB_PORT 8086
ENV INFLUXDB_DB tautulli

RUN mkdir /work
COPY . /work
WORKDIR /work

RUN python setup.py install
CMD python tautulli_influxdb_export.py --tautullihost "$TAUTULLI_HOST" --tautulliport "$TAUTULLI_PORT" --tautulliapikey "$TAUTULLI_KEY" --interval "$INTERVAL" --influxdbhost "$INFLUXDB_HOST" --influxdbport "$INFLUXDB_PORT" --influxdbdatabase "$INFLUXDB_DB"
