"""
This script runs the ScoringEngine application using a development server.
"""
import sys
sys.path.append("testers/")
# Note we did not loose the bug
'''
       / .'
 .---. \/
(._.' \()
 ^"""^"
bug
'''
from os import environ
from ScoringEngine import app
#from ScoringEngine import engine
import ScoringEngine.conf
from ScoringEngine.conf import conf
import argparse

def arguments():
    parser = argparse.ArgumentParser(description='Lepus ISE v2.5')
    parser.add_argument('-e','--env', help='Environment', required=False)
    parser.add_argument('-c','--config', help='Specify the config file', required=False)
    parser.add_argument('--gen-config', help='Generates a new default config file', required=False, action='store_true')
    parser.add_argument('--gen-db', help='Imports the schema into a database', required=False, action='store_true')
    parser.add_argument('-v','--version', help='Generates a new default config file', required=False, action='store_true')
    
    args = parser.parse_args()

    env = None

    config = 'conf.yaml'
    if args.config:
        config = args.config

    if args.version:
        print "Lepus ISE v2.5"
        return False
    elif args.gen_config:
        ScoringEngine.conf.newConf(config)
        return False
    elif args.env:
        env = args.env

    if args.gen_db:
        import ScoringEngine.db
        import ScoringEngine.db.tables
        ScoringEngine.db.tables.Base.metadata.create_all(ScoringEngine.db.engine)
        return False

    ScoringEngine.conf.loadConf(config, env)
    return True

if __name__ == '__main__':
    if arguments():
        HOST = environ.get('SERVER_HOST', conf['listen'])
        try:
            PORT = int(environ.get('SERVER_PORT', str(conf['port'])))
        except ValueError:
            PORT = conf['port']
        #engine.start() # Note that this starts a thread
        app.debug = conf['debug']
        app.secret_key = conf['secret']
        app.run(HOST, PORT)
