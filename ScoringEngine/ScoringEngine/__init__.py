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
from os import environ



BUILD = "non-ci-build"
BRANCH = "unknown"

if 'CI_BRANCH' in environ:
    BRANCH = environ['CI_BRANCH']
else:
    try:
        import subprocess
        BRANCH = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])
    except Exception:
        pass
if 'CI_BUILD' in environ:
    BUILD = environ['CI_BUILD']
else:
    BUILD = '0'

VERSION = '4.1.' + BUILD + '-ALPHA'
VERSIONSTR = "Lepus ISE v%s" % (VERSION)

def arguments():
    import argparse
    parser = argparse.ArgumentParser(description=VERSIONSTR)
    parser.add_argument('--gen-config', help='Generates a new default config file', required=False, action='store_true')
    parser.add_argument('--make-config', help='Generates a new default config file', required=False)
    parser.add_argument('--gen-db', help='Imports the schema into a database', required=False, action='store_true')
    parser.add_argument('--print-config', help='Prints the current configuration', required=False, action='store_true')
    
    args = parser.parse_args()

    if args.gen_config:
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

        return False

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

def validate_env(engine=False):
    import os, os.path
    from ScoringEngine.core import logger, config
    from ScoringEngine.core.db import Session, tables

    if config.has_item("sentry_dsn"):
        import sentry_sdk
        from sentry_sdk.integrations.flask import FlaskIntegration

        sentry_sdk.init(
            dsn=config.get_item("sentry_dsn"),
            integrations=[FlaskIntegration()]
        )

    try:
        s = Session()
        logger.debug("Checking if >0 users")
        if s.query(tables.User).count() == 0:
            # We should create the default admin user if there are no users.
            logger.warning("No users found creating default admin account")
            s.add(tables.User.create("Administrator", "admin", u"admin", -1, 5))
            s.commit()

        # refresh scoretype table
        logger.debug("Refreshing scoretypes")
        for d in config.get_item("tests"):
            for f in os.listdir(d):
                if os.path.isfile(os.path.join(d, f)):
                    p = f.split('.')
                    if len(p) > 1 and p[1] == "py":
                        t = s.query(tables.ServiceType).filter(tables.ServiceType.tester == p[0]).first()
                        if not t:
                            logger.debug("Adding type: %s" % p[0])
                            t = tables.ServiceType()
                            t.tester = p[0]
                            t.name = p[0].capitalize()
                            s.add(t)

        logger.debug("Checking for engines")
        if s.query(tables.Engine).count() == 0:
            if not engine:
                logger.warning("No Engines Defined")
            else:
                from datetime import datetime
                engine_id = config.get_item("engine/id")
                logger.debug("Adding Default Engine")
                engine = tables.Engine()
                engine.id = engine_id
                engine.name = "Default"
                engine.last_checkin = datetime.utcnow()
                s.add(engine)
        s.commit()
        s.close()
    except Exception as e:
        import sys
        print(e)
        print(e.message)
        sys.exit(1)

def main():
    print(VERSIONSTR)
    print("Running Build %s on Branch %s" % (BUILD, BRANCH))
    if arguments():
        validate_env()
        from ScoringEngine.web import app
        app.run('127.0.0.1', 5080)
        print("hello")
