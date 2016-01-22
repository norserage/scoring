import ScoringEngine.db.tables as tables
import random
import platform
import subprocess
import re
import json
import pprint

def getRandomUser(session, passwd_db):
    user = []
    for usr in session.query(tables.PasswordDatabase).filter(tables.PasswordDatabase.db==passwd_db):
        user.append({'user':usr.user,'pass':usr.password,'domain':usr.domain,'email':usr.email})
        
    #outuser = user[random.randint(0,user.count - 1)]
    outuser = random.choice(user)
    return outuser

def getRandomEmail(session, passwd_db):
    user = []
    for usr in session.query(tables.PasswordDatabase).filter(tables.PasswordDatabase.db==passwd_db):
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
    confpair = session.query(tables.ServiceArg).filter(tables.and_(tables.ServiceArg.serviceid==service.id,tables.ServiceArg.key=='conf', tables.ServiceArg.serverid==teamserver.id))
    if confpair.count() > 0:
        conf = json.loads(confpair[0].value)
        pprint.pprint(conf)
        return conf
    else:
        return {}


