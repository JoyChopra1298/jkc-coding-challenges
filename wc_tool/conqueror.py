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


def calculate_lines(file_name):
    with open(file_name, "r") as file:
        line_count = 0
        # Using loop loads one line at a time
        for line in file:
            line_count += 1
        return line_count


def calculate_words(file_name):
    with open(file_name, "r") as file:
        word_count = 0
        for line in file:
            words = line.split()
            non_empty_words = [word for word in words if word.strip()]
            word_count += len(non_empty_words)
        return word_count


def calculate_characters(file_name):
    with open(file_name, "r") as file:
        character_count = 0
        for line in file:
            # Add 1 for '\n'
            character_count += len(line) + 1
        return character_count


def parse_arguments():
    argument_parser = argparse.ArgumentParser(description="wc is a tool to give word, line,"
                                                          " character and byte count for a txt file")

    # Positional argument - This is mandatory
    argument_parser.add_argument("file_name", help="Name of the input txt file")

    # Optional arguments
    argument_parser.add_argument("-c", "--byte_count",
                                 action="store_true", help="Byte count")
    argument_parser.add_argument("-l", "--lines",
                                 action="store_true", help="Number of lines")
    argument_parser.add_argument("-w", "--words",
                                 action="store_true", help="Number of words")
    argument_parser.add_argument("-m", "--characters",
                                 action="store_true", help="Number of characters")

    return argument_parser.parse_args()


def validate_file_extension(file_name):
    file_extension = file_name.split('.')[-1]
    if file_extension not in VALID_FILE_EXTENSIONS:
        print(f"{OutputColor.RED.value}File extension .{file_extension} is unsupported{OutputColor.WHITE.value}")
        exit()


def print_output_string(file_information):
    output_string = OutputColor.GREEN.value
    if "lines" in file_information:
        output_string += f'{str(file_information["lines"])} '
    if "words" in file_information:
        output_string += f'{str(file_information["words"])} '
    if "byte_count" in file_information:
        output_string += f'{str(file_information["byte_count"])} '
    if "characters" in file_information:
        output_string += f'{str(file_information["characters"])} '

    output_string += f'{file_information["name"]}{OutputColor.WHITE.value}'
    print(output_string)


def compute_file_information(parsed_arguments):
    file_information = {
        "name": parsed_arguments.file_name
    }
    if parsed_arguments.byte_count:
        file_information["byte_count"] = calculate_byte_count(parsed_arguments.file_name)
    if parsed_arguments.lines:
        file_information["lines"] = calculate_lines(parsed_arguments.file_name)
    if parsed_arguments.words:
        file_information["words"] = calculate_words(parsed_arguments.file_name)
    if parsed_arguments.characters:
        file_information["characters"] = calculate_characters(parsed_arguments.file_name)

    if (
        not parsed_arguments.byte_count and
        not parsed_arguments.lines and
        not parsed_arguments.words and
        not parsed_arguments.characters
    ):
        file_information["lines"] = calculate_lines(parsed_arguments.file_name)
        file_information["words"] = calculate_words(parsed_arguments.file_name)
        file_information["byte_count"] = calculate_byte_count(parsed_arguments.file_name)
    return file_information


def conqueror():
    parsed_arguments = parse_arguments()
    validate_file_extension(parsed_arguments.file_name)
    file_information = compute_file_information(parsed_arguments)
    print_output_string(file_information)


if __name__ == "__main__":
    conqueror()
