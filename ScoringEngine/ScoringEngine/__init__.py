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
from __future__ import print_function
VERSION = '4.0'
VERSIONSTR = "Lepus ISE v%s DEV" % (VERSION)

def arguments():
    import argparse
    parser = argparse.ArgumentParser(description=VERSIONSTR)
    parser.add_argument('--gen-config', help='Generates a new default config file', required=False, action='store_true')
    parser.add_argument('--gen-db', help='Imports the schema into a database', required=False, action='store_true')
    parser.add_argument('--print-config', help='Prints the current configuration', required=False, action='store_true')
    parser.add_argument('-v','--version', help='Generates a new default config file', required=False, action='store_true')
    
    args = parser.parse_args()

    if args.version:
        print(VERSIONSTR)
        return False
    elif args.gen_config:
        from ScoringEngine.core import config
        config.save_default("config.json")
        return False

    if args.gen_db:
        import ScoringEngine.core.db
        import ScoringEngine.core.db.tables
        ScoringEngine.core.db.tables.Base.metadata.create_all(ScoringEngine.core.db.engine)
        s = ScoringEngine.core.db.getSession()
        u = ScoringEngine.core.db.tables.User.create("Administrator", "admin", "admin", -1, 5)
        s.add(u)
        s.commit()
        s.close()
        return False

    return True



def main():
    if arguments():
        from ScoringEngine.core.conf import conf
        from os import environ
        from ScoringEngine.web import app
        app.run('127.0.0.1', 5080)
        print("hello")
