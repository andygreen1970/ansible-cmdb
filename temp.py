import yaml
import pprint

default_conf = {
 'config':
     {'host': 'localhost',
      'password': '',
      'port': 3306,
      'type': 'MYSQL',
      'user': 'root',
      'view': 'otrs.CMDB_Servers'
      },
 'hostfield': '',
 'where': '',
 'groups': [],
 'vars': {
            'group': [],
            'host': []
         }
}

with open('cmdb.yaml') as f:
    load_conf = yaml.load(f)
#pprint.pprint(load_conf)

for key in load_conf:
    pkey = str(key).lower().strip()
    if (pkey in default_conf) and isinstance(load_conf[key], type(default_conf[pkey])):
        print(key, pkey, load_conf[key])
    else:
            raise Exception('Error {}={}'.format(key, load_conf[key]))

#pprint.pprint(default_conf)
#print(yaml.dump(load_conf, default_flow_style=False))