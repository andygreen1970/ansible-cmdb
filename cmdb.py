from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = '''
    name: cmdb
    plugin_type: inventory
    version_added: "0.1a"
    short_description: Uses CMDB to find hosts to target
    description:
        - Uses a YAML configuration file with a valid YAML extension. Uses CMDB to find hosts to target
    extends_documentation_fragment:
      - constructed
      - inventory_cache
    requirements:
      - MYSQL (or other) connector installed
    options:
        plugin:
            description: token that ensures this is a source file for the 'cmdb' plugin.
            required: True
            choices: ['cmdb']
        host_field:
            description: Host field name to ansible target.
            required: True
        type:
            description: CMDB database type.
            default: MYSQL
            choices: ['MYSQL']
        host:
            description: CMDB database host.
            default: localhost
        port:
            description: CMDB database port.
            default: 3306
            type: string
        user:
            description: CMDB database user.
            default: root
        password:
            description: CMDB database password.
            default: ''
        view:
            description: CMDB database dataset.
            required: True
        where:
            description: Filter for SQL format.
            default: ''
        groups:
            description: Ansible host group list.
        groupvars:
            description: Field list for group vars.
        hostvars:
            description: Field list for host vars.
'''


import os

from ansible import constants as C
from ansible.errors import AnsibleParserError
from ansible.module_utils._text import to_native, to_text
from ansible.plugins.inventory import BaseInventoryPlugin, Constructable, Cacheable
import connector


class InventoryModule(BaseInventoryPlugin, Constructable, Cacheable):
    # todo Разобраться с кэшированием в Ansible
    NAME = 'cmdb'

    def __init__(self):

        # todo Добавить настройку класса Cmdb
        super(InventoryModule, self).__init__()
        self.__cmdb_config = {
        'host': 'localhost',
        'password': '',
        'port': '3306',
        'type': 'MYSQL',
        'user': 'root',
        'view': '',
        'where': ''
        }
        self.__cmdb_fieldset = {
        'host_field': '',
        'groups': [],
        'groupvars': [],
        'hostvars': []
        }

    def verify_file(self, path):

        valid = False
        if super(InventoryModule, self).verify_file(path):
            file_name, ext = os.path.splitext(path)
            if not ext or ext in C.YAML_FILENAME_EXTENSIONS:
                valid = True
        return valid

    def parse(self, inventory, loader, path, cache=False):
        # todo Сделать управление кэшированием
        super(InventoryModule, self).parse(inventory, loader, path, cache=cache)

        self._read_config_data(path)

        for key in self._options:
            if key in self.__cmdb_config :
                if isinstance(self._options[key], type(self.__cmdb_config[key])):
                    self.__cmdb_config[key] = self._options[key]
                else:
                    raise AnsibleParserError('Тип опции {} должен быть {}, а не {}'.format(key,
                                                    type(self.__cmdb_config[key]), type(self._options[key])))
            if key in self.__cmdb_fieldset :
                if isinstance(self._options[key], type(self.__cmdb_fieldset[key])):
                    self.__cmdb_fieldset[key] = self._options[key]
                else:
                    raise AnsibleParserError('Тип опции {} должен быть {}, а не {}'.format(key,
                                                    type(self.__cmdb_config[key]), type(self._options[key])))

        fields = list()
        for key in self.__cmdb_fieldset:
            if isinstance(self.__cmdb_fieldset[key], list):
                fields += self.__cmdb_fieldset[key]
            else:
                # todo Проверить на иттерабельность
                fields.append(self.__cmdb_fieldset[key])

        cmdb = connector.Cmdb(config=self.__cmdb_config, fields=set(fields))

        groups = list()

        for row in cmdb:
            group_temp = list()
            for fieldname in self.__cmdb_fieldset['groups']:
                group_temp.append(row[fieldname])
                if row[fieldname] not in groups:
                    groups.append(row[fieldname])
                    self.inventory.add_group(row[fieldname])
                    self.inventory.add_child('all', row[fieldname])
            # todo Реализовать Hosts in multiple groups
            # todo Реализовать дочерние группы
            if len(group_temp) > 1:
                raise AnsibleParserError('В данной версии не реализована поддержка '
                                         'размещения хоста в нескольких группах')

            self.inventory.add_host(row[self.__cmdb_fieldset['host_field']], group=group_temp[0])
            for varname in self.__cmdb_fieldset['hostvars']:
                self.inventory.set_variable(row[self.__cmdb_fieldset['host_field']], varname, row[varname])


        cmdb.close()

