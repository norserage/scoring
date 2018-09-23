#!/usr/bin/env bash

COLOR_DEFAULT="\e[39m"
COLOR_BLACK="\e[30m"
COLOR_RED="\e[31m"
COLOR_GREEN="\e[32m"
COLOR_YELLOW="\e[33m"
COLOR_BLUE="\e[34m"
COLOR_MAGENTA="\e[35m"
COLOR_CYAN="\e[36m"


function out {
    echo "[$1$2$COLOR_DEFAULT] $3"
}

function setup {
    if [ ! -e "/etc/ise/config.json" ]; then
        out $COLOR_YELLOW "Warning" "Missing config file beginning setup"
        out $COLOR_MAGENTA "Setup" "Creating config file"
        python /app/runserver.py --make-config=/etc/ise/config.json
        out $COLOR_MAGENTA "Setup" "Creating database"
        PGPASSWORD=$POSTGRES_ENV_POSTGRES_PASSWORD psql -h $POSTGRES_PORT_5432_TCP_ADDR -U postgres -c 'create database ise;'
        out $COLOR_MAGENTA "Setup" "Setting up database"
        python /app/runserver.py --gen-db
    fi
    echo "Setup Complete"
}

function web_start {
    /usr/local/bin/supervisord -n -c /setup/supervisord.conf
}

function score_start {
    python /app/runscore.py
}

setup

case "$1" in
    web)
        web_start
        ;;
    score)
        score_start
        ;;
    *)
        echo $"Usage: $0 {web|score}"
esac
