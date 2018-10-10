from dataclasses import dataclass
from pathlib import Path

from . import config


@dataclass
class Resource:

    app_dir: Path = config.APP_DIR

    def word_list(self, name):
        with open(self._word_lists_dir / name, encoding='utf-8') as f:
            return f.read().split()

    def font(self, name):
        return str(self._fonts_dir / name)

    @property
    def _word_lists_dir(self):
        return self._root_dir / 'word-lists'

    @property
    def _fonts_dir(self):
        return self._root_dir / 'fonts'

    @property
    def _root_dir(self):
        return self.app_dir / 'resources'
