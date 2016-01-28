import argparse
import ScoringEngine
import os

parser = argparse.ArgumentParser(description=ScoringEngine.VERSIONSTR)
parser.add_argument('-c','--config', help='Specify the config file', required=False)
parser.add_argument('-d','--db', help='Specify the database', required=False)

parser.add_argument('-q','--quite', help='', required=False, action='store_true')
parser.add_argument('-v','--version', help='prints the versions information', required=False, action='store_true')
    
args = parser.parse_args()

if args.version:
    print(ScoringEngine.VERSIONSTR)
    os._exit(0)

conf = "conf.yaml"

if args.config != None:
    conf = args.config

def myprint(s):
    if not args.quite:
        print(s)

if not args.quite:
    c = raw_input("Location for conf [" + conf + "]:")
    if not c == None:
        conf = c

import ScoringEngine.conf
ScoringEngine.conf.newConf(conf)
    
db = args.db
if not args.quite:
    d = raw_input("Location for db [" + db + "]:")
    if not d == None:
        db = d

import yaml
with open(conf) as f:
    cnf = yaml.load(f)
    cnf["production"]["database"] = db
    yaml.dump(cnf, f)

