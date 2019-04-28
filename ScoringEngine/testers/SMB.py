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

from smb.SMBConnection import SMBConnection
import ScoringEngine.engine.options
import ScoringEngine.utils
from ScoringEngine.core import logger
from ScoringEngine.engine import helper


def _a(a):
    return a.encode('ascii', 'ignore')


def test(event, service):

    service_config = helper.get_service_config_old(service['team_server_id'], service['service_id'])

    if all([key in service_config for key in ['passdb', 'share', 'path', 'file', 'remote_name']]):
        logger.error("")
        return

    try:
        user = helper.get_random_user(service_config['passdb'])
        conn = SMBConnection(
            username=_a(user['user']),
            password=_a(user['pass']),
            my_name=_a("LepusISE"),
            remote_name=_a(service_config['remote_name']),
            domain=_a(user['domain']),
            is_direct_tcp=(service['port'] == 445)
        )
        if conn.connect(_a(service['ip']), service['port']):
            if 'regex' not in service_config or service_config['regex'].strip() == "":
                files = conn.listPath(service_config['share'], service_config['path'])
                for file in files:
                    if file.filename == service_config['file']:
                        helper.save_new_service_status(
                            event=event,
                            service=service,
                            status=True,
                            extra_info=[f.filename for f in files]
                        )
                        conn.close()
                        return
                helper.save_new_service_status(
                    event=event,
                    service=service,
                    status=False,
                    extra_info=[f.filename for f in files]
                )
            else:
                import re
                import tempfile
                file_obj = tempfile.NamedTemporaryFile()
                file_attr, filesize = conn.retrieveFile(service_config['share'], service_config['path'] + "/" + service_config['file'], file_obj)
                file_obj.seek(0)
                content = file_obj.read()
                file_obj.close()
                if re.search(service_config['regex'], content) is None:
                    helper.save_new_service_status(
                        event=event,
                        service=service,
                        status=False,
                        extra_info=content
                    )
                else:
                    helper.save_new_service_status(
                        event=event,
                        service=service,
                        status=True,
                        extra_info=content
                    )
        else:
            helper.save_new_service_status(
                event=event,
                service=service,
                status=False,
                extra_info=None
            )
        conn.close()
    except Exception as ex:
        helper.save_new_service_status(
            event=event,
            service=service,
            status=False,
            extra_info=None
        )


def options():
    return {
        'passdb': ScoringEngine.engine.options.PasswordDB(),
        'remote_name': ScoringEngine.engine.options.String(),
        'share': ScoringEngine.engine.options.String(),
        'path': ScoringEngine.engine.options.String(),
        'file': ScoringEngine.engine.options.String(),
        'regex': ScoringEngine.engine.options.String()
        }