import os

from functools import partial

import yaml
from ctfcli.cli.exceptions import ComposeStackFileNotFound


class FileContentLoader(yaml.SafeLoader):
    def __init__(self, stream: str, base_dir: str):
        self._base_dir = base_dir
        super(FileContentLoader, self).__init__(stream)

    def filecontent(self, node):
        filepath = os.path.join(self._base_dir, self.construct_scalar(node))
        try:
            with open(filepath, 'r') as f:
                return f.read()
        except FileNotFoundError as e:
            raise ComposeStackFileNotFound from e
         
def get_yaml_loader(base_dir: str):
    FileContentLoader.add_constructor('!filecontents', FileContentLoader.filecontent)
    return partial(FileContentLoader, base_dir=base_dir)