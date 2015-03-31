import ScoringEngine.db.tables as tables
import random

def getRandomUser(session, passwd_db):
    user = []
    for usr in session.query(tables.PasswordDatabase).filter(tables.PasswordDatabase.db==passwd_db):
        user.add({'user':usr.user,'pass':usr.password,'domain':usr.domain,'email':usr.email})
    outuser = user[random.randint(0,user.count - 1)]
    return outuser

def getRandomEmail(session, passwd_db):
    user = []
    for usr in session.query(tables.PasswordDatabase).filter(tables.PasswordDatabase.db==passwd_db):
        user.add(usr.email)
    outuser = user[random.randint(0,user.count - 1)]
    return outuser