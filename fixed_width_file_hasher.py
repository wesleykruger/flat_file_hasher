from pathlib import Path
import random
import string
import os.path


# This must come before the user definition section
class ScrambleObject:
    def __init__(self, record_type_start_pos: int, record_value: str,
                 scramble_start_pos: int, scramble_length: int, data_type: str):
        self.record_type_start_pos = record_type_start_pos
        self.record_value = record_value
        self.scramble_start_pos = scramble_start_pos
        self.scramble_length = scramble_length
        self.data_type = data_type


# *****************************************************************
# USER INPUT SECTION

# Define the FILES you will be reading/writing. Ensure these are not directories.
# Ensure that the output file directory can be written to. If a file already exists with this name it WILL be overwritten.
input_file = Path('')
output_file = Path('')

line_limit = 7

# Enter your lines to mask here, each as a new ScrambleObject.
# Each should follow this format, and they should be separated by commas within the array:

# record_type_start_pos(int): This is where we should begin looking for an indicator that a value needs to be scrambled on this line. If it is the first character, it will be 0.
# record_value(str): This is the value that we should be looking for to know to scramble a different part of the line.
# scramble_start_pos(int): This is the first character in the string that needs to be scrambled. Remember it is 0-based.
# scramble_length(int): This is the length of the string starting at scramble_start_pos that needs to be scrambled.
# data_type(either 'str' or 'int): This tells us whether the output of the scramble needs to be letters or numbers. The purpose of this is to ensure that the output can still be processed as valid test data.
# data_type property in each object should be either 'str' or 'int'. Anything else will produce an error.

# Ex: scramble_array = scramble_array = [
#     ScrambleObject(record_type_start_pos=0, record_value='A', scramble_start_pos=43, scramble_length=18, data_type='str'),
#     ScrambleObject(record_type_start_pos=0, record_value='C', scramble_start_pos=9, scramble_length=10, data_type='int'),
# ]
# All strings are case-sensitive

scramble_array = [
    ScrambleObject(record_type_start_pos=0, record_value='A', scramble_start_pos=43, scramble_length=18, data_type='str'),
    ScrambleObject(record_type_start_pos=0, record_value='B', scramble_start_pos=33, scramble_length=9, data_type='str'),
    ScrambleObject(record_type_start_pos=0, record_value='C', scramble_start_pos=9, scramble_length=10, data_type='int'),
    ScrambleObject(record_type_start_pos=0, record_value='D', scramble_start_pos=28, scramble_length=1, data_type='int'),
    ScrambleObject(record_type_start_pos=0, record_value='E', scramble_start_pos=62, scramble_length=5, data_type='int')
]

# END USER DEFINITIONS
# ********************************************************************


def validate_objects(obj):
    if type(obj.record_type_start_pos) != int or type(obj.record_value) != str \
            or type(obj.scramble_start_pos) != int or type(obj.scramble_length) != int:
        return 'TypeError'
    elif obj.data_type != 'str' and obj.data_type != 'int':
        return 'DataType'
    else:
        return True


def random_string(text_or_int, data_type):
    length = len(text_or_int)
    if data_type == 'int':
        numbers = '0123456789'
        characters = ''.join(random.choice(numbers) for i in range(length))
    else:
        letters = string.ascii_letters
        characters = ''.join(random.choice(letters) for i in range(length))
    return characters


def scramble(arr):
    lines = []
    if not os.path.isfile(input_file):
        raise FileNotFoundError('Input file does not exist, please enter a valid path.')

    # Initial quick sweep to make sure that all entries are valid
    for index, validate_entry in enumerate(arr):
        # Zero-based index is confusing for error message
        error_index = index + 1
        if validate_objects(validate_entry) == 'TypeError':
            raise TypeError('You are using the incorrect data type for one of your properties '
                            'in object number {}'.format(error_index))
        elif validate_objects(validate_entry) == 'DataType':
            raise Exception("The data type you selected in scramble object number {} is incorrect. "
                            "Please select either 'str' or 'int'.".format(error_index))

    # Overwrite output file if it already exists so we're not appending each time
    if os.path.isfile(output_file):
        open(output_file, 'w',).close()
    # Read through each line one at a time, write when we hit our limit to ensure we don't go over available memory
    with open(input_file, 'r', encoding='utf8') as fileobject:
        for line in fileobject:
            for entry in arr:
                if line[entry.record_type_start_pos: entry.record_type_start_pos + len(entry.record_value)] == entry.record_value:
                    text_to_replace = line[entry.scramble_start_pos:entry.scramble_start_pos + entry.scramble_length]
                    scramble_values = random_string(text_to_replace, entry.data_type)
                    line = line[:entry.scramble_start_pos] + scramble_values + line[entry.scramble_start_pos + len(scramble_values):]
            print(line)
            lines.append(line)
            if len(lines) >= line_limit:
                with open(output_file, 'a+', encoding='utf8') as a:
                    a.write(''.join(lines))
                    lines = []
    # Final append write for any lines left over
    if len(lines) > 0:
        with open(output_file, 'a+', encoding='utf8') as w:
            w.write(''.join(lines))
            w.close()


if __name__ == '__main__':
    scramble(scramble_array)
