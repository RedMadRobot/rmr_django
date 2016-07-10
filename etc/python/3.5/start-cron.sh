#!/usr/bin/env bash

# update default values of PAM environment variables (used by CRON scripts)
env | while read -r LINE; do  # read STDIN by line
    # split LINE by "="
    IFS="=" read VAR VAL <<< ${LINE}
    # remove existing definition of environment variable, ignoring exit code
    sed --in-place "/^${VAR}/d" /etc/security/pam_env.conf || true
    # append new default value of environment variable
    echo "${VAR} DEFAULT=${VAL}" >> /etc/security/pam_env.conf
done

# forward /var/log/cron.log to /dev/stdout
touch /var/log/cron.log
chown www-data:www-data /var/log/cron.log
ln -sf /dev/stdout /var/log/cron.log

# start cron
rsyslogd
service cron start

# trap SIGINT and SIGTERM signals and gracefully exit
trap "service cron stop; exit" SIGINT SIGTERM
while true
do
    tail -f /dev/null & wait ${!}
done
