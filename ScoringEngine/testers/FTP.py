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
import ftplib
from ScoringEngine.core.db import Session, tables
from ScoringEngine.core import logger
import ScoringEngine.utils as utils
from ScoringEngine.engine import helper
import ScoringEngine.engine.options
from datetime import datetime

def test(event, service):

    service_config = helper.get_service_config_old(service['team_server_id'], service['service_id'])

    if 'passdb' in service_config:
        logger.error(
            "Service configuration error with service (%i,%i)." % (service['team_server_id'], service['service_id']))
        return

    ftp = ftplib.FTP()

    try:
        ftp.connect(service['ip'])
        user = helper.get_random_user(service_config['passdb'])

        ftp.login(user['user'], user['passs'])

        if 'mode' in service_config and service_config['mode'] != 'connect':
            if service_config['mode'] == 'chkfileexist':
                pass
        else:
            # We are connected so we are good
            helper.save_new_service_status(
                event=event,
                service=service,
                status=True,
                extra_info=ftp.getwelcome()
            )

    except ftplib.error_perm as ep:
        helper.save_new_service_status(
            event=event,
            service=service,
            status=False,
            extra_info=ep.message
        )
    finally:
        ftp.close()

def options():
    return {
        'passdb': ScoringEngine.engine.options.PasswordDB()
        }