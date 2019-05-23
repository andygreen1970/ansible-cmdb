DOCUMENTATION = '''
    name: cmdb
    plugin_type: inventory
    version_added: "0.2a"
    short_description: Использование CMDB для создания целеей Ansible
    description:
        - Использование CMDB для создания целеей Ansible:
      - constructed
      - inventory_cache
    requirements:
      - MYSQL или другой connector поддерживающий аналогичные методы доступа к данным
    options:
        plugin:
            description: token that ensures this is a source file for the 'cmdb' plugin.
            required: True
            choices: ['cmdb']
        host_field:
            description: Имя поля CMDB, содержащее имя хоста
            required: True
        type:
            description: Тип CMDB
            default: MYSQL
            choices: ['MYSQL']
        host:
            description: Адрес или имя хоста CMDB
            default: localhost
        port:
            description: Порт, на котором CMDB ожидает запросы
            default: 3306
            type: string
        user:
            description: Пользователь CMDB
            default: root
        password:
            description: Пароль для доступа кCMDB
            default: ''
        view:
            description: Имя набора данных CMDB, содержащего необходимую информацию в формате DB.DATASET
            required: True
        where:
            description: Фильтр для отбора данных в формате MYSQL WHERE
            default: ''
        groups:
            description: Список имен полей, определяющий группы хостов
        groupvars:
            description: Список полей, определеющий переменные групп для Ansible
        hostvars:
            description: Список полей, определеющий переменные хостов для Ansible
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

        root_name = self.__cmdb_fieldset['groups'][0]
        root_groups = dict()

        child_names = self.__cmdb_fieldset['groups'][1:]
        child_groups = list()

        for row in cmdb:

            if (row[root_name] not in root_groups) and row[root_name]:
                root_groups[row[root_name]] = list()
                self.inventory.add_group(row[root_name])
            self.inventory.add_host(row[self.__cmdb_fieldset['host_field']], group=row[root_name])

            for child_name in child_names:
                if (row[child_name] not in root_groups[row[root_name]]) and row[child_name]:
                    root_groups[row[root_name]].append(row[child_name])
                    self.inventory.add_group(row[child_name])

                if row[child_name] and row[root_name]:
                    self.inventory.add_child(row[root_name], row[child_name])
                self.inventory.add_host(row[self.__cmdb_fieldset['host_field']], group=row[child_name])

            # todo Реализовать Hosts in multiple groups
            # todo Не забыть добавить groupvars, если это возможно
            for varname in self.__cmdb_fieldset['hostvars']:
                self.inventory.set_variable(row[self.__cmdb_fieldset['host_field']], varname, row[varname])

        cmdb.close()

