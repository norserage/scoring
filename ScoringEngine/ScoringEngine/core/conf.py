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
import yaml

import pprint

conf = {}

def loadConf(config="conf.yaml",env=None):
    global conf
    f = open(config,"r")
    c = yaml.load(f)
    f.close()
    pprint.pprint(c)
    if env != None:
        conf = c[env]
    else:
        conf = c[c['env']]
    pprint.pprint(conf)


def newConf(config="conf.yaml"):
    c = {
        'env':"production",
        'production':{
            'database':"postgresql://scoring:scoring@10.151.130.5/scoring",
            'filedb':'scoring.db',
            'listen':'0.0.0.0',
            'port':8080,
            'secret':",LHGUL}~Ge;3D>mSHg\gb>+VrQ7=BoYe",
            'debug':False,
            'tester locations':['testers/',''],
            'fcgi':{
                'socket':"/tmp/scoring.sock"
            },
            'logger':{
                'console':'debug',
                'file':'warning',
                'db':'info',
                'file_path':'scoring.log'
            },
            'engine':{
                'min':60,
                'max':120
            }
        },
        'dev':{
            'database':"postgresql://scoring:scoring@10.151.130.5/scoring",
            'filedb':'scoring.db',
            'listen':'localhost',
            'port':5555,
            'secret':"6y;]kL,J7d|W)(\+]0to)0Y,J{Z|-,J+",
            'debug':True,
            'tester locations':['testers/',''],
            'fcgi':{
                'socket':"/tmp/scoring.sock"
            },
            'logger':{
                'console':'debug',
                'file':'warning',
                'db':'info',
                'file_path':'scoring.log'
            },
            'engine':{
                'min':60,
                'max':120
            }
        },
        'local':{
            'database':"sqlite:///scoring.sqlite3",
            'filedb':'scoring.db',
            'listen':'localhost',
            'port':5555,
            'secret':"Kyw^k$!kico}YKbJF5n=T#hO9y._NBw6",
            'debug':True,
            'tester locations':['testers/',''],
            'fcgi':{
                'socket':"/tmp/scoring.sock"
            },
            'logger':{
                'console':'debug',
                'file':'warning',
                'db':'info',
                'file_path':'scoring.log'
            },
            'engine':{
                'min':60,
                'max':120
            }
        }
    }
    f = open(config,"w")
    yaml.dump(c, f)
    f.close()