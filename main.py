import argparse
import logging
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), './src')))
from flow_log_processor import FlowLogProcessor
from helpers import write_output

def main():
    parser = argparse.ArgumentParser(description="Process flow logs and map to tags based on a lookup table.")
    parser.add_argument('flow_log_file', help='Path to the flow log file')
    parser.add_argument('lookup_table_file', help='Path to the lookup table CSV file')
    parser.add_argument('output_file', help='Path to the output CSV file')

    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    processor = FlowLogProcessor(args.lookup_table_file)
    tag_counts, port_protocol_counts = processor.process_flow_logs(args.flow_log_file)
    write_output(args.output_file, tag_counts, port_protocol_counts)

    logging.info("Processing complete. Results written to %s", args.output_file)

if __name__ == "__main__":
    main()