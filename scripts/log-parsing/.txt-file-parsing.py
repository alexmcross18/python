# Imports the json module
import json
# Imports the argparse module
import argparse

# Sets up the argument parser with a description of what the script does
parser = argparse.ArgumentParser(description="Parse a custom log .txt file into JSON format ready for DCE/Sentinel ingestion.")
# Adds an input arguement and makes it a requirement for the user to enter
parser.add_argument("--input", required=True, help="Path to the input log .txt file")
# Adds an output arguement and makes it a requirement for the user to enter
parser.add_argument("--output", required=True, help="Path to write the output .json file")
# Parses the command-line arguments and stores them as attributes on "args" (e.g. args.input, args.output)
args = parser.parse_args()

# Opens the logs file, in read mode and assigns the "lines" variable to read each line of the logs file
with open(args.input, "r") as input_file:
    lines = input_file.readlines()

# Creates an empty list to add to later
parsed_logs = []

# Creates a for loop that removes the new line character "\n" (.strip()) from the end of each line
# Splits each line on every space (.split(" ")) a maximum of 5 times
for line in lines:
    # Try/Except to handle error handling, if there is less splits or malformed/missing text in the logs file it skips
    # that line, moves onto the next and prints an error message instead of crashing the script
    try:
        split_logs = line.strip().split(" ", 4)
        # Creates a dictionary called "log_entries", makes multiple key+value pairs (e.g. key=date value=split_logs[0])
        log_entries = {
            "date": split_logs[0],
            "time": split_logs[1],
            "level": split_logs[2],
            "source": split_logs[3],
            "message": split_logs[4]
        }
        # Adds the completed dictionary for this line to the parsed_logs list
        parsed_logs.append(log_entries)
    except IndexError:
        print(f"Skipping missing/malformed line:  {line.strip()}")
    except Exception:
        # Catches anything unexpected (encoding issues, memory errors, etc.) without crashing the script
        print(f"Skipping line due to unexpected error {line.strip()}")

# Creates a new json file in write mode and adds the data from the "parsed_logs" list
# Indents the json file 4 times per row of data to make it easier to read
with open(args.output, "w") as output_file:
    json.dump(parsed_logs, output_file, indent=4)
