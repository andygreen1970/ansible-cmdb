import yaml
import pprint
test =[
    {'name': 'cmdb'},
    {'confg':
         {
             'host': 'localhost',
             'port': '3606'
         }
     },
    {'host_field': 'name'},
    {'groups':
        ['g1', 'g2']
     },
    {'vars':
            ['v1', 'v2']
     }
]
def f(d, step=None):
    if not step:
        temp_keys = list(d.keys)
        temp_value = list()
        temp_dict = {key for key in d.keys}
        step = 1
    if type(d) == dict:
        temp = temp.keys()

#with open('cmdb.yaml') as f:
#    test = yaml.load(f)
#pprint.pprint(test)
#print(yaml.dump(test, default_flow_style=False))