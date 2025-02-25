import argparse
from enum import Enum

VALID_FILE_EXTENSIONS = ["txt"]


class OutputColor(Enum):
    RED = "\033[31m"
    GREEN = "\033[32m"
    WHITE = "\033[0m"


def calculate_byte_count(file_name):
    with open(file_name, "rb") as file:
        # Move to the end of the file
        file.seek(0, 2)
        return file.tell()


def parse_arguments():
    argument_parser = argparse.ArgumentParser(description="wc is a tool to give word, line,"
                                                          " character and byte count for a txt file")

    argument_parser.add_argument("file_name", help="Name of the input txt file")

    argument_parser.add_argument("-c", "--byte_count",
                                 action="store_true", help="Byte count")

    return argument_parser.parse_args()


def validate_file_extension(file_name):
    file_extension = file_name.split('.')[-1]
    if file_extension not in VALID_FILE_EXTENSIONS:
        print(f"{OutputColor.RED.value}File extension .{file_extension} is unsupported{OutputColor.WHITE.value}")
        exit()


def print_output_string(file_information):
    output_string = OutputColor.GREEN.value
    if "byte_count" in file_information:
        output_string += str(file_information["byte_count"])

    output_string += f' {file_information["name"]}{OutputColor.WHITE.value}'
    print(output_string)


def compute_file_information(parsed_arguments):
    file_information = {
        "name": parsed_arguments.file_name
    }
    if parsed_arguments.byte_count:
        file_information["byte_count"] = calculate_byte_count(parsed_arguments.file_name)
    return file_information


def conqueror():
    parsed_arguments = parse_arguments()
    validate_file_extension(parsed_arguments.file_name)
    file_information = compute_file_information(parsed_arguments)
    print_output_string(file_information)


if __name__ == "__main__":
    conqueror()
