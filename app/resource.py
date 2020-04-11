from pathlib import Path

import attr


@attr.s(auto_attribs=True)
class Resource:

    root: Path = Path(__file__).parent.parent / "resources"

    def words(self, name):
        with open(self._word_lists_dir / name, encoding="utf-8") as f:
            return f.read().split()

    @property
    def word_lists(self):
        return self._word_lists_dir.iterdir()

    @property
    def _word_lists_dir(self):
        return self.root / "word_lists"
