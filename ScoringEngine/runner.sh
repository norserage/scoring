#!/usr/bin/env bash

function setup {
    if [ ! -e "/etc/ise/config.json" ]; then
        echo "Missing config file beginning setup"
        python /app/runserver.py --make-config=/etc/ise/config.json
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
