
import os
os.environ["ENV"] = "test"
from src.tnote import (
        process_tags
)
import unittest
import pandas as pd


class TestProcessTags(unittest.TestCase):
    def setUp(self):
        pass

    def test_simple(self):
        input_tags = "todo,later,new"
        expected_tags = "todo,later,new"
        output = process_tags(input_tags)

        output = output.split(",")
        expected_tags = expected_tags.split(",")
        self.assertCountEqual(expected_tags, output)

    def test_whitespace(self):
        input_tags = "todo ,   later,new"
        expected_tags = "todo,later,new"
        output = process_tags(input_tags)

        output = output.split(",")
        expected_tags = expected_tags.split(",")
        self.assertCountEqual(expected_tags, output)

    def test_empty(self):
        input_tags = "todo,later,new,,"
        expected_tags = "todo,later,new"
        output = process_tags(input_tags)

        output = output.split(",")
        expected_tags = expected_tags.split(",")
        self.assertCountEqual(expected_tags, output)
