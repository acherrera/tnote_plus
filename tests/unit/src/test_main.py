import os

os.environ["ENV"] = "test"
from src.tnote import process_tags
import unittest
from unittest.mock import patch


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


class TestGetKeys(unittest.TestCase):
    def setUp(self):
        patcher1 = patch("src.tnote.getkey")
        self.mock_get_key = patcher1.start()
        self.addCleanup(patcher1.stop)

    def test_simple(self):
        # TODO
        pass
