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
import ScoringEngine.utils as utils
from ScoringEngine.engine import helper

def test(event, service):
    try:
        r = utils.Ping(service['ip'], 5)
        if r:
            helper.save_new_service_status(
                event=event,
                service=service,
                status=True,
                extra_info={'trip': r}
            )
        else:
            helper.save_new_service_status(
                event=event,
                service=service,
                status=False,
                extra_info=None
            )
    except Exception as e:
        helper.save_new_service_status(
            event=event,
            service=service,
            status=False,
            extra_info=e.message
        )

def options():
    return {
        
        }
