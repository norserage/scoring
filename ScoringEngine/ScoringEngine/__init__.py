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
    parser.add_argument('--make-config', help='Generates a new default config file', required=False)
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
    elif args.make_config:
        import os
        from ScoringEngine.core import _default_config
        from json import dumps
        from random import choice
        from string import printable

        c = _default_config

        if 'POSTGRES_PORT' in os.environ:
            cs = "postgres://postgres:" + os.environ['POSTGRES_ENV_POSTGRES_PASSWORD'] + "@" + os.environ['POSTGRES_PORT_5432_TCP_ADDR'] + ":" + os.environ['POSTGRES_PORT_5432_TCP_PORT'] + "/ise"
            c['database'] = cs

        c['secret'] = "".join([choice(printable) for _ in range(0, 32)])
        c['debug'] = False


        with open(args.make_config, 'w') as f:
            f.write(dumps(c, indent=4))

    if args.gen_db:
        import ScoringEngine.core.db
        import ScoringEngine.core.db.tables
        ScoringEngine.core.db.tables.Base.metadata.create_all(ScoringEngine.core.db.engine)
        s = ScoringEngine.core.db.getSession()
        u = ScoringEngine.core.db.tables.User.create("Administrator", "admin", u"admin", -1, 5)
        s.add(u)
        s.commit()
        s.close()
        return False

    return True



def main():
    if arguments():
        from ScoringEngine.web import app
        app.run('127.0.0.1', 5080)
        print("hello")
