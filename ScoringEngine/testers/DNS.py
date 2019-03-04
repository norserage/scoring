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
from ScoringEngine.core import logger
import json
import ScoringEngine.utils
from ScoringEngine.engine import helper
import ScoringEngine.engine.options
import subprocess
import random


def test(event, service):

    service_config = helper.get_service_config_old(service['team_server_id'], service['service_id'])

    if 'servers' not in service_config:
        logger.error("Service configuration error with service (%i,%i)." % (service['team_server_id'], service['service_id']))
        return

    try:
        server = random.choice(service_config['servers'])
        sp = subprocess.Popen(["nslookup", server['dns'], service['ip']], stdout=subprocess.PIPE)
        sp.wait()
        output = sp.stdout.readlines()

        logger.debug(json.dumps(output))

        helper.save_new_service_status(
            event=event['id'],
            service=service,
            status=any([server['ip'] in line for line in output]),
            extra_info=output
        )
    except Exception as e:
        helper.save_new_service_status(
            event=event['id'],
            service=service,
            status=False,
            extra_info=output
        )

def options():
    return {
        'servers': ScoringEngine.engine.options.JSON()
        }

