import unittest
from unittest.mock import patch, mock_open
from collections import defaultdict
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from flow_log_processor import FlowLogProcessor

class TestFlowLogProcessorUnit(unittest.TestCase):
    common_read_data = (
        'dstport,protocol,tag\n'
        '25,tcp,sv_P1\n'
        '68,udp,sv_P2\n'
        '23,tcp,sv_P1\n'
        '31,udp,sv_P3\n'
        '443,tcp,sv_P2\n'
        '22,tcp,sv_P4\n'
        '3389,tcp,sv_P5\n'
        '0,icmp,sv_P5\n'
        '110,tcp,email\n'
        '993,tcp,email\n'
        '143,tcp,email\n'
    )

    def setUp(self):
        patcher = patch('builtins.open', new_callable=mock_open, read_data=self.common_read_data)
        self.addCleanup(patcher.stop)
        self.mock_file = patcher.start()
        self.processor = FlowLogProcessor('dummy_lookup_table.csv')

    def test_load_lookup_table(self):
        """Test that the lookup table is loaded correctly from the CSV file."""
        lookup_table = self.processor.lookup_table
        expected = defaultdict(list, {
            (25, 'tcp'): ['sv_p1'],
            (68, 'udp'): ['sv_p2'],
            (23, 'tcp'): ['sv_p1'],
            (31, 'udp'): ['sv_p3'],
            (443, 'tcp'): ['sv_p2'],
            (22, 'tcp'): ['sv_p4'],
            (3389, 'tcp'): ['sv_p5'],
            (0, 'icmp'): ['sv_p5'],
            (110, 'tcp'): ['email'],
            (993, 'tcp'): ['email'],
            (143, 'tcp'): ['email']
        })
        self.assertEqual(lookup_table, expected)

    def test_parse_flow_log_line(self):
        """Test that a flow log line is parsed correctly into a dictionary."""
        line = '2 3 4 5 6 7 22 6 9 10'
        expected = {'dstport': 22, 'protocol': 6}
        self.assertEqual(self.processor.parse_flow_log_line(line), expected)

    def test_get_protocol_string(self):
        """Test that the protocol number is correctly converted to a protocol string."""
        self.assertEqual(self.processor.get_protocol_string(6), 'tcp')
        self.assertEqual(self.processor.get_protocol_string(17), 'udp')
        self.assertEqual(self.processor.get_protocol_string(1), 'icmp')
        self.assertEqual(self.processor.get_protocol_string(999), 'unknown')

    def test_process_flow_logs_chunk(self):
        """Test that a chunk of flow logs is processed correctly, counting tags and port/protocol combinations."""
        chunk = '2 3 4 5 6 7 22 6 9 10\n2 3 4 5 6 7 25 6 9 10\n'
        tag_counts, port_protocol_counts = self.processor.process_flow_logs_chunk(chunk)
        expected_tag_counts = defaultdict(int, {'sv_p4': 1, 'sv_p1': 1})
        expected_port_protocol_counts = defaultdict(int, {(22, 'tcp'): 1, (25, 'tcp'): 1})
        self.assertEqual(tag_counts, expected_tag_counts)
        self.assertEqual(port_protocol_counts, expected_port_protocol_counts)

if __name__ == '__main__':
    unittest.main()