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

config = configreader(['config.json', '/etc/ise.json', '/etc/ise/config.json'], {
    "database": "",
    "tests": [],
    "debug": True,  # TODO this should default to false in production
    "secret": "fakesecret",  # TODO this should not be staticly set
    "clam": {
        "enabled": False,
        "path": None,
        "address": None,
        "port": None
    }
})

if len(config.get_item("tests")) > 0:
    import sys
    for l in config.get_item("tests"):
        sys.path.append(l)
