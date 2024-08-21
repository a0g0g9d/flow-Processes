# Flow Log Processor

This project processes flow logs and maps them to tags based on a lookup table. Feel free to add input data files to the 'data' folder or the root directory, and use them to generate the output_csv file

## Prerequisites

- Python 3.6 or higher

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/a0g0g9d/flow-log-processor.git
    cd flow-log-processor
    ```

2. Create and activate a virtual environment:
    ```sh
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

## Usage

To process a flow log file:
```sh
python3 main.py <flow_log_file> <lookup_table_file> <output_file>
```

To run the code with the existing data:
```sh
python3 main.py data/temp_flow_log.txt data/temp_lookup_table.csv output_csv
```

## Test Cases

To run all the test cases in `test` folder, run following command:

```sh
python3 -m unittest discover -s test -p "*.py"
```