import yaml

conf = {}

def loadConf(config="conf.yaml",env=None):
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
        },
        'dev':{
            'database':"postgresql://scoring:scoring@10.151.9.11/scoring",
            'listen':'localhost',
            'port':5555,
        },
        'local':{
            'database':"sqlite:///scoring.db",
            'listen':'localhost',
            'port':5555,
        }
    }
    f = open(config,"w")
    yaml.dump(c, f)
    f.close()