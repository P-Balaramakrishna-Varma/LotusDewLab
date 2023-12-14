import logging
import json

def setup_logger(log_file):
    """ Set up the logger configuration. """
    logging.basicConfig(filename=log_file, level=logging.INFO, format='%(message)s')

def log_json_record(record):
    """ Log a JSON record to the specified log file. """
    logger = logging.getLogger()
    json_record = json.dumps(record)
    logger.info(json_record)


def read_last_300_json_records(log_file):
    """ Read the last 300 JSON records from the log file. """
    try:
        with open(log_file, 'r') as file:
            lines = file.readlines()
            last_300_lines = lines[-300:]
            return [json.loads(line) for line in last_300_lines]
    except Exception as e:
        print(f"Error: {e}")
        return []


log_file = 'your_log_file.log'

# Setup logger
setup_logger(log_file)

# Example of logging JSON records
for i in range(500):  # Assume you are logging 500 records
    log_json_record({"record_number": i, "data": f"Sample data {i}"})

# Read the last 300 records
last_300_records = read_last_300_json_records(log_file)
print(last_300_records)
