import yaml

conf = {}

def loadConf(config="conf.yaml",env=None):
    global conf
    f = open(config,"r")
    c = yaml.load(f)
    f.close()
    if env != None:
        conf = c[env]
    else:
        conf = c[c['env']]


def newConf(config="conf.yaml"):
    c = {
        'env':"production",
        'production':{
            'database':"postgresql://scoring:scoring@10.151.9.11/scoring",
            'listen':'0.0.0.0',
            'port':8080,
            'secret':",LHGUL}~Ge;3D>mSHg\gb>+VrQ7=BoYe",
            'debug':False
        },
        'dev':{
            'database':"postgresql://scoring:scoring@10.151.9.11/scoring",
            'listen':'localhost',
            'port':5555,
            'secret':"6y;]kL,J7d|W)(\+]0to)0Y,J{Z|-,J+",
            'debug':True
        },
        'local':{
            'database':"sqlite:///scoring.db",
            'listen':'localhost',
            'port':5555,
            'secret':"Kyw^k$!kico}YKbJF5n=T#hO9y._NBw6",
            'debug':True
        }
    }
    f = open(config,"w")
    yaml.dump(c, f)
    f.close()