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
    echo -e "[$1$2$COLOR_DEFAULT] $3"
}

function setup {
    if [ ! -e "/etc/ise/config.json" ]; then
        out $COLOR_YELLOW "Warning" "Missing config file beginning setup"
        out $COLOR_MAGENTA "Setup" "Creating config file"
        python /runserver.py --make-config=/etc/ise/config.json
        out $COLOR_MAGENTA "Setup" "Creating database"
        PGPASSWORD=$POSTGRES_ENV_POSTGRES_PASSWORD psql -h $POSTGRES_PORT_5432_TCP_ADDR -U postgres -c 'create database ise;'
        out $COLOR_MAGENTA "Setup" "Setting up database"
        python /runserver.py --gen-db
    fi
    out $COLOR_MAGENTA "Setup" "Setup Complete"
}

function update_db {
    out $COLOR_CYAN "Database" "Upgrading database"
    alembic upgrade head
    out $COLOR_CYAN "Database" "Upgrade Complete"
}

function web_start {
    /usr/local/bin/supervisord -n -c /setup/supervisord.conf
}

function api_score_start {
    out $COLOR_YELLOW "SCORE" "Starting in API mode"
    python /runapiscore.py
}

function db_score_start {
    update_db
    out $COLOR_YELLOW "SCORE" "Starting in DB mode"
    python /runscore.py
}

function score_start {
    if [[ -z "${SCORE_MODE}" ]]; then
        db_score_start
    else
        case "${SCORE_MODE}" in
            api)
                api_score_start
                ;;
            db)
                db_score_start
                ;;
            *)
                echo "Invalid SCORE_MODE=${SCORE_MODE}"
                ;;
        esac
    fi
}

setup

case "$1" in
    web)
        update_db
        web_start
        ;;
    score)
        score_start
        ;;
    db-score)
        db_score_start
        ;;
    api-score)
        api_score_start
        ;;
    *)
        echo $"Usage: $0 {web|score}"
esac
