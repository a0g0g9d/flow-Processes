import csv
import logging
from collections import defaultdict
from constants import PROTOCOL_MAP, CHUNK_SIZE, ENCODING

class FlowLogProcessor:
    def __init__(self, lookup_table_file):
        self.lookup_table = self.load_lookup_table(lookup_table_file)

    def load_lookup_table(self, file_path):
        logging.info("Loading lookup table from: %s", file_path)
        lookup = defaultdict(list)
        try:
            with open(file_path, 'r', encoding=ENCODING['ASCII']) as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        key = (int(row['dstport']), row['protocol'].strip().lower())
                        lookup[key].append(row['tag'].strip().lower())
                    except (ValueError, KeyError) as e:
                        logging.error("Error parsing lookup table row: %s", e)
                        continue
        except Exception as e:
            logging.error("Error loading lookup table: %s", e)
            raise
        logging.info("Loaded lookup table with %d entries.", len(lookup))
        return lookup

    def parse_flow_log_line(self, line):
        fields = line.strip().split()
        try:
            if fields[0] != '2':
                raise ValueError("Invalid flow log version in log line %s" % line)
            if fields[6] == '-' or fields[7] == '-':
                return None
            
            dstport = int(fields[6])
            protocol = int(fields[7])
            
        except (ValueError, IndexError) as e:
            logging.error("Error parsing line: %s", e)
            return None

        return {
            'dstport': dstport,
            'protocol': protocol
        }

    def get_protocol_string(self, protocol):
        return PROTOCOL_MAP.get(protocol, 'unknown')

    def process_flow_logs_chunk(self, chunk):
        '''
        Process a chunk of flow logs, counting tags and port/protocol combinations.
        
        Args:
            chunk (str): A chunk of flow log lines.
        
        Returns:
            tuple: Two defaultdicts, one for tag counts and one for port/protocol counts.
        '''
        logging.debug("Processing chunk...")
        tag_counts = defaultdict(int)
        port_protocol_counts = defaultdict(int)
        for line in chunk.splitlines():
            parsed = self.parse_flow_log_line(line)
            if parsed:
                protocol_str = self.get_protocol_string(parsed['protocol']).lower()
                key = (parsed['dstport'], protocol_str)
                tags = self.lookup_table.get(key, ['untagged'])
                for tag in tags:
                    tag_counts[tag] += 1
                port_protocol_counts[key] += 1

        return tag_counts, port_protocol_counts

    def process_flow_logs(self, flow_log_file):
        '''
        Process the entire flow log file, counting tags and port/protocol combinations.
        
        Args:
            flow_log_file (str): Path to the flow log file.
        
        Returns:
            tuple: Two defaultdicts, one for tag counts and one for port/protocol counts.
        '''
        tag_counts = defaultdict(int)
        port_protocol_counts = defaultdict(int)

        try:
            with open(flow_log_file, 'r', encoding=ENCODING['ASCII']) as f:
                while True:
                    chunk = f.read(CHUNK_SIZE)
                    if not chunk:
                        break
                    chunk_tag_counts, chunk_port_protocol_counts = self.process_flow_logs_chunk(chunk)
                    for tag, count in chunk_tag_counts.items():
                        tag_counts[tag] += count
                    for key, count in chunk_port_protocol_counts.items():
                        port_protocol_counts[key] += count
        except Exception as e:
            logging.error("Error processing flow log file: %s", e)
            raise

        return tag_counts, port_protocol_counts