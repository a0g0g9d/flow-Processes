import unittest
import os
from collections import defaultdict
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from flow_log_processor import FlowLogProcessor

class TestFlowLogProcessorIntegration(unittest.TestCase):

    def setUp(self):
        self.processor = FlowLogProcessor('./data/temp_lookup_table.csv')

    def test_process_flow_logs(self):
        """Test processing the entire flow log file."""
        tag_counts, port_protocol_counts = self.processor.process_flow_logs('./data/temp_flow_log.txt')
        expected_tag_counts = defaultdict(int,{'untagged': 8, 'sv_p2': 1, 'sv_p1': 2, 'email': 3})
        expected_port_protocol_counts = defaultdict(int, {(49153, 'tcp'): 1, (49154, 'tcp'): 1, (49155, 'tcp'): 1, (49156, 'tcp'): 1, (49157, 'tcp'): 1, (49158, 'tcp'): 1, (80, 'tcp'): 1, (1024, 'tcp'): 1, (443, 'tcp'): 1, (23, 'tcp'): 1, (25, 'tcp'): 1, (110, 'tcp'): 1, (993, 'tcp'): 1, (143, 'tcp'): 1})
        
        self.assertEqual(tag_counts, expected_tag_counts)
        self.assertEqual(port_protocol_counts, expected_port_protocol_counts)

if __name__ == '__main__':
    unittest.main()