FROM python:3.5

# GeoIP2 requirements: https://docs.djangoproject.com/en/1.9/ref/contrib/gis/geoip2/
RUN apt-get clean && apt-get update \
    && apt-get install -y software-properties-common \
    && add-apt-repository ppa:maxmind/ppa \
    && sed --in-place 's/jessie/trusty/g' /etc/apt/sources.list.d/maxmind-ppa-jessie.list \
    && apt-get update \
    && apt-get install -y libmaxminddb0 libmaxminddb-dev mmdb-bin

# GeoDjango requirements: https://docs.djangoproject.com/en/1.9/ref/contrib/gis/install/geolibs/
RUN apt-get clean && apt-get update \
    && apt-get install -y binutils libproj-dev gdal-bin

# CRON
RUN apt-get clean && apt-get update \
    && apt-get install -y cron
COPY start-cron /usr/sbin
RUN mkfifo /var/log/cron.log \
    && chmod 0666 /var/log/cron.log

RUN rm -rf /var/lib/apt/lists/*
