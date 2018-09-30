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
import ScoringEngine.core.db.tables as tables
import random
import platform
import subprocess
import re
import json
import pprint
import pytz
import datetime

def getRandomUser(session, passwd_db):
    user = []
    passwddb = session.query(tables.PasswordDatabase).filter(tables.PasswordDatabase.name == passwd_db).first()
    for usr in passwddb.entries:
        user.append({'user':usr.user,'pass':usr.password,'domain':usr.domain,'email':usr.email})
        
    #outuser = user[random.randint(0,user.count - 1)]
    outuser = random.choice(user)
    return outuser

def getRandomEmail(session, passwd_db):
    user = []
    passwddb = session.query(tables.PasswordDatabase).filter(tables.PasswordDatabase.name == passwd_db).first()
    for usr in passwddb.entries:
        user.append(usr.email)
    #outuser = user[random.randint(0,user.count - 1)]
    outuser = random.choice(user)
    return outuser

# This way we don't have to run as root
def Ping(hostname,timeout):
    if platform.system() == "Windows":
        command="ping "+hostname+" -n 1 -w "+str(timeout*1000)
    else:
        command="ping -i "+str(timeout)+" -c 1 " + hostname
    proccess = subprocess.Popen(command, stdout=subprocess.PIPE)
    matches=re.match('.*time=([0-9]+)ms.*', proccess.stdout.read(),re.DOTALL)
    if matches:
        return matches.group(1)
    else: 
        return False

def getServiceConfig(session, service, teamserver):
    # TODO change how this is done to be easier to manage from the web interface
    confpair = session.query(tables.ServiceArg).filter(
        tables.and_(tables.ServiceArg.serviceid == service.id, tables.ServiceArg.key == 'conf', tables.ServiceArg.serverid == teamserver.id))
    if confpair.count() > 0:
        conf = json.loads(confpair[0].value)
        pprint.pprint(conf)
        return conf
    else:
        return {}
