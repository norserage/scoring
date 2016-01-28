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
import bsddb3.db
import uuid
from ScoringEngine.conf import conf
db = None
def init():
    db = bsddb3.db.DB()
    db.open(conf['filedb'])

def insert(data):
    id = uuid.uuid4()
    db.put(id, data)
    return id

def get(id):
    return db.get(id)




