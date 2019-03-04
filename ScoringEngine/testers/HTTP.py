
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
import requests
from ScoringEngine.engine import helper
import ScoringEngine.utils
import ScoringEngine.engine.options
import re

def test(event, service):
    service_config = helper.get_service_config_old(service['team_server_id'], service['service_id'])

    try:
        url = "http://%s:%d" % (service['ip'], service['port'])
        if 'url' in service_config:
            url += service_config['url']
        res = requests.get(url)
        if 'regex' in service_config and service_config['regex'].strip() != "":
            if re.search(service_config['regex'], res.content) is None:
                helper.save_new_service_status(
                    event=event,
                    service=service,
                    status=False,
                    extra_info=res.content
                )
                return
        helper.save_new_service_status(
            event=event,
            service=service,
            status=True,
            extra_info=res.content

        )
    except Exception as e:
        helper.save_new_service_status(
            event=event,
            service=service,
            status=False,
            extra_info=str(e.message)
        )

def options():
    return {
        'url': ScoringEngine.engine.options.String(),
        'regex': ScoringEngine.engine.options.String()
        }