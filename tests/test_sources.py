"""核对交接资料的可读性及损坏表头的识别。"""
from pathlib import Path
import shutil
import tempfile
import unittest

from source_check import TABLES, read_sources


SOURCES = Path(__file__).resolve().parents[1] / "资料"


class SourcesTest(unittest.TestCase):
    def test_sources_follow_the_published_format(self):
        sources = read_sources(SOURCES)
        self.assertEqual(set(sources), set(TABLES))
        self.assertTrue(all(sources.values()))

    def test_wrong_header_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            copied = Path(directory) / "资料"
            shutil.copytree(SOURCES, copied)
            first = next(iter(TABLES))
            (copied / f"{first}.csv").write_text("编号,说明\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "表头"):
                read_sources(copied)
