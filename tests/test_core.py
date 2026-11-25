"""Tests for Tool Call Golden Cassette."""
import unittest
from tool_call_golden_cassette.core import ToolCassette, CassetteMissError


class TestToolCassette(unittest.TestCase):
    def test_record_serialize_and_replay_fifo(self):
        c = ToolCassette()
        c.record("get", {"a": 1, "b": 2}, {"seq": 1})
        c.record("get", {"b": 2, "a": 1}, {"seq": 2})
        c2 = ToolCassette.load_json(c.dump_json())
        self.assertEqual(c2.replay("get", {"a": 1, "b": 2}), {"seq": 1})
        self.assertEqual(c2.replay("get", {"a": 1, "b": 2}), {"seq": 2})
        with self.assertRaises(CassetteMissError):
            c2.replay("get", {"a": 1, "b": 2})
