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
import imaplib
from ScoringEngine.core import logger
from ScoringEngine.engine import helper
import ScoringEngine.engine.options

def test(event, service):

    service_config = helper.get_service_config_old(service['team_server_id'], service['service_id'])

    try:
        imap = imaplib.IMAP4_SSL(service['ip'], service['port'])
        if 'passdb' not in service_config:
            logger.error(
                "Service configuration error with service (%i,%i)." % (
                service['team_server_id'], service['service_id']))
            return

        user = helper.get_random_user(service_config['passdb'])

        r = imap.login(user['user'], user['pass'])

        if r[0] == 'OK':
            helper.save_new_service_status(
                event=event,
                service=service,
                status=True,
                extra_info=r
            )
        else:
            helper.save_new_service_status(
                event=event,
                service=service,
                status=False,
                extra_info=r
            )
        try:
            imap.close()
        except Exception as ep2:
            pass
    except Exception as ep:
        helper.save_new_service_status(
            event=event,
            service=service,
            status=False,
            extra_info=r
        )

def options():
    return {
        'passdb': ScoringEngine.engine.options.PasswordDB()
        }