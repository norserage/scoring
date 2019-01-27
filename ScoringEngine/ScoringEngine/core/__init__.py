"""
Copyright 2016 Brandon Warner

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from ScoringEngine.core.configreader import configreader

_default_config = {
    "database": "",
    "tests": ['testers'],
    "debug": True,  # TODO this should default to false in production
    "secret": "fakesecret",  # TODO this should not be staticly set,
    "max_content_length": 25 * 1024 * 1024,
    "clam": {
        "enabled": False,
        "path": None,
        "address": None,
        "port": None,
        "stream_limit": 2.5e7,
    },
    "engine": {
        "min": 60,
        "max": 120
    },
    "logging": {
        "version": 1,
        "formatters": {
            "default": {
                "format": "%(message)s"
            },
            "simple": {
                "format": "%(asctime)s - %(module)s.%(funcName)s - %(levelname)s - %(message)s"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "DEBUG",
                "formatter": "simple",
                "stream": "ext://sys.stdout"
            },
            "defaultconsole": {
                "class": "logging.StreamHandler",
                "level": "DEBUG",
                "formatter": "default",
                "stream": "ext://sys.stdout"
            }
        },
        "loggers": {
            "ise": {
                "level": "DEBUG",
                "propagate": False,
                "handlers": [
                    "console"
                ]
            }
        },
        "root": {
            "level": "DEBUG",
            "handlers": [
                "defaultconsole"
            ]
        }
    },
    "analytics": {
        "html": ""
    },
    "session_provider": "flask.sessions.SecureCookieSessionInterface",
    "session_redis": None,
    "default_timezone": "UTC",
    "allowed_types": [
        "application/pdf",
        "image/png",
        "image/jpeg",
        "image/gif",
        "text/plain"
    ]
}

config = configreader(['config.json', '/etc/ise.json', '/etc/ise/config.json'], _default_config)

if len(config.get_item("tests")) > 0:
    import sys
    for l in config.get_item("tests"):
        sys.path.append(l)

import logging
import logging.config

logging.config.dictConfig(config.get_item("logging"))

logger = logging.getLogger('ise')