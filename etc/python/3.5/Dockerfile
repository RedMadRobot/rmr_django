FROM python:3.5

# GeoIP2 requirements: https://docs.djangoproject.com/en/1.9/ref/contrib/gis/geoip2/
RUN apt-get clean && apt-get update \
    && apt-get install -y software-properties-common \
    && add-apt-repository ppa:maxmind/ppa \
    && sed --in-place 's/jessie/trusty/g' /etc/apt/sources.list.d/maxmind-ppa-jessie.list \
    && apt-get update \
    && apt-get install -y libmaxminddb0 libmaxminddb-dev mmdb-bin \
    && rm -rf /var/lib/apt/lists/*

# GeoDjango requirements: https://docs.djangoproject.com/en/1.9/ref/contrib/gis/install/geolibs/
RUN apt-get clean && apt-get update \
    && apt-get install -y binutils libproj-dev gdal-bin \
    && rm -rf /var/lib/apt/lists/*

# CRON
RUN apt-get clean && apt-get update \
    && apt-get install -y cron \
    && rm -rf /var/lib/apt/lists/*
RUN mkfifo --mode 0666 /var/log/cron.log
# make pam_loginuid.so optional for cron
# see https://github.com/docker/docker/issues/5663#issuecomment-42550548
RUN sed --regexp-extended --in-place \
    's/^session\s+required\s+pam_loginuid.so$/session optional pam_loginuid.so/' \
    /etc/pam.d/cron
COPY start-cron /usr/sbin
