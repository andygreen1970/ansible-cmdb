from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = '''

'''

EXAMPLE = '''

'''

# import connector
import os
from ansible import constants as C
from ansible.errors import AnsibleError
from ansible.module_utils._text import to_native
from ansible.plugins.inventory import BaseInventoryPlugin, Constructable, Cacheable


class InventoryModule(BaseInventoryPlugin, Constructable, Cacheable):
    NAME = 'cmdb'

    def __init__(self):
        super(InventoryModule, self).__init__()

    def verify_file(self, path):

        valid = False

        if super(InventoryModule, self).verify_file(path):
            file_name, ext = os.path.splitext(path)

            if not ext or ext in C.YAML_FILENAME_EXTENSIONS:
                valid = True

        return valid

    def parse(self, inventory, loader, path, cache=False):

        super(InventoryModule, self).parse(inventory, loader, path, cache=cache)
        self._read_config_data(path)
        # addr = self._options['address']
        self.inventory.add_host('host-{}'.format(len(self._options)))
        self.inventory.add_host('host-{}'.format(loader))
