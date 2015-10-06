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