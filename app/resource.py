from dataclasses import dataclass
from pathlib import Path

from . import config


@dataclass
class Resource:

    app_dir: Path = config.APP_DIR

    def words(self, name):
        with open(self._word_lists_dir / name, encoding='utf-8') as f:
            return f.read().split()

    @property
    def _word_lists_dir(self):
        return self._root_dir / 'word_lists'

    @property
    def _root_dir(self):
        return self.app_dir / 'resources'
