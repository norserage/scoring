﻿import ScoringEngine.db.tables as tables
import random
import platform
import subprocess
import re

def getRandomUser(session, passwd_db):
    user = []
    for usr in session.query(tables.PasswordDatabase).filter(tables.PasswordDatabase.db==passwd_db):
        user.add({'user':usr.user,'pass':usr.password,'domain':usr.domain,'email':usr.email})
    #outuser = user[random.randint(0,user.count - 1)]
    outuser = random.choice(user)
    return outuser

def getRandomEmail(session, passwd_db):
    user = []
    for usr in session.query(tables.PasswordDatabase).filter(tables.PasswordDatabase.db==passwd_db):
        user.add(usr.email)
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