import logging

def write_output(output_file, tag_counts, port_protocol_counts):
    try:
        with open(output_file, 'w') as out:
            out.write("Tag,Count\n")
            for tag, count in sorted(tag_counts.items()):
                out.write(f"{tag},{count}\n")

            out.write("\nPort/Protocol Combination Counts:\n")
            out.write("Port,Protocol,Count\n")
            for (port, protocol), count in sorted(port_protocol_counts.items()):
                out.write(f"{port},{protocol},{count}\n")
    except Exception as e:
        logging.error("Error writing output file: %s", e)
        raise