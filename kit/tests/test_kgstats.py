import tempfile
import unittest
from pathlib import Path

from pyspark.sql import SparkSession

from sumqa.kgstats import load_triples


class TripleParserTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spark = SparkSession.builder.master("local[2]").appName("triple-parser-test").getOrCreate()
        cls.spark.sparkContext.setLogLevel("ERROR")

    @classmethod
    def tearDownClass(cls):
        cls.spark.stop()

    def test_long_literals_escapes_datatypes_and_iris(self):
        long_text = "abstract text " * 20000
        escaped = r'He said \"hello\" with a \\ slash.'
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "triples.nt"
            path.write_text(
                f'<urn:s> <urn:abstract> "{long_text}"@en .\n'
                f'<urn:s> <urn:escaped> "{escaped}" .\n'
                '<urn:s> <urn:count> "42"^^<http://www.w3.org/2001/XMLSchema#integer> .\n'
                '<urn:s> <urn:related> <urn:other> .\n'
                '<urn:s> <urn:empty> "" .\n',
                encoding="utf-8",
            )
            rows = {row.p: row for row in load_triples(self.spark, [str(path)]).collect()}
        self.assertEqual(len(rows), 5)
        self.assertEqual(rows["urn:abstract"].o, long_text)
        self.assertEqual(rows["urn:abstract"].lang, "en")
        self.assertEqual(rows["urn:escaped"].o, escaped)
        self.assertEqual(rows["urn:count"].dt, "http://www.w3.org/2001/XMLSchema#integer")
        self.assertEqual(rows["urn:related"].okind, "iri")
        self.assertEqual(rows["urn:related"].o, "urn:other")
        self.assertEqual(rows["urn:empty"].o, "")


if __name__ == "__main__":
    unittest.main()
