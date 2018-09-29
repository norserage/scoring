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
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ScoringEngine.core import config

engine = create_engine(config.get_item('database'))
Session = sessionmaker(bind=engine)

_session = None

def getSession():
    global _session
    if _session is None:
        _session = Session()
    return _session

def closeSession():
    global _session
    if _session is not None:
        _session.close()
        _session = None