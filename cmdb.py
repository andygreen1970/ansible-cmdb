from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = '''
    name: cmbd
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
            description: Host to target.
            required: True
        config:
            description: Config for connection.
        where:
            description: Filter for SQL.
        groups:
            description: Group list.
        vars:
            description: Vars dictionary for host and group.
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

    def verify_file(self, path):

        valid = False
        if super(InventoryModule, self).verify_file(path):
            file_name, ext = os.path.splitext(path)

            if not ext or ext in C.YAML_FILENAME_EXTENSIONS:
                valid = True

        return valid

    # todo Лучше использовать встроенные методы из ansible (они наверняка есть)
    @staticmethod
    def option2dict(option):
        temp = {}
        for line in option:
            for key in line:
                if key in temp:
                    raise connector.ParserError("Дублирующийся параметр config: {}.".format(key))
                temp[str(key)] = str(line[key])
        return temp

    @staticmethod
    def option2list(option):
        temp = []
        for line in option:
            temp.append(str(line))
        return temp

    def parse(self, inventory, loader, path, cache=False):
        # todo Сделать управление кэшированием
        super(InventoryModule, self).parse(inventory, loader, path, cache=cache)

        self._read_config_data(path)

        groups = InventoryModule.option2list(self.get_option('groups'))
        vars = InventoryModule.option2dict(self.get_option('vars'))

        # todo Как то криво выглядит. Надо доработать
        for key in vars:
            vars[key] = vars[key][1:-1].split(',')
            i =0
            for value in vars[key]:
                vars[key][i] = value.strip().strip('\'')
                i += 1

        fields = vars['group']+vars['host']+groups
        fields.append(self.get_option('host_field'))
        # todo Рассмотреть другие способы удаления дублей из списка
        fields = set(fields)

        cmdb = connector.Cmdb(config=InventoryModule.option2dict(self.get_option('config')),
                              fields=fields)
        for row in cmdb:
            pass
        cmdb.close()
        #self.inventory.add_host()

