import os
import csv
import json
from datetime import datetime
import random

def calc_distance(row, data):
	"""
	Processes a single row from the CSV file and updates the data dictionary.

	Parameters:
	row (dict): A dictionary representing a single row from the CSV file.
	data (dict): A dictionary to store processed data with keys as (date, hour)
				tuples and values as lists of trip distances.

	This function performs the following steps:
	1. Converts 'tripDistance' and 'totalAmount' from the row to floats.
	2. Applies filtering conditions to check if 'tripDistance' is greater
	than 0 and 'totalAmount' is greater than 0.
	3. Parses 'tpepPickupDateTime' to extract the hour and date.
	4. Constructs a key as a tuple of (date, hour).
	5. Uses setdefault to initialize a list if the key does not exist in the
	data dictionary and appends 'tripDistance' to the list.
	"""
	trip_distance = float(row['tripDistance'])
	total_amount = float(row['totalAmount'])
	
	if filter(trip_distance, 0.0, 'gt') and filter(total_amount, 0.0,'gt'):
		# Parse the pickup datetime to extract hour and date
		pickup_datetime = datetime.strptime(row['tpepPickupDateTime'], '%Y-%m-%dT%H:%M:%SZ')
		day_hour = pickup_datetime.hour
		date = str(pickup_datetime.date())
		key = (date, day_hour)
        
		# Initialize the list for this key if not exists, and append the trip distance
		data.setdefault(key, []).append(trip_distance)


def calc_totals(row,data):
	"""
    Calculates total amounts based on tip amout, trip distance, total amount, grouped at rate code ID.

    Parameters:
    row (dict): A dictionary representing a single row of data from a dataset.
    data (dict): A dictionary to store aggregated total amounts based on rate code ID.

    This function performs the following steps:
    1. Extracts trip distance, total amount, and rate code ID from the row.
    2. Checks if the trip distance and total amount are greater than 0 using a filter function.
    3. If the conditions are met, updates the total amounts for the corresponding rate code ID in the data dictionary.
    4. If the rate code ID is not present in the data dictionary, initializes it with zero values.
    5. Increments the tip amount, tolls amount, and total amount for the rate code ID with the values from the row.
    """

	trip_distance = float(row['tripDistance'])
	total_amount = float(row['totalAmount'])
	key = row['rateCodeId']
	if filter(trip_distance, 0.0, 'gt') and filter(total_amount, 0.0,'gt'):
		if key not in data:
			data[key] = {'tipAmount': 0, 'tollsAmount': 0, 'totalAmount': 0}
		data[key]['tipAmount'] += float(row['tipAmount'])
		data[key]['tollsAmount'] += float(row['tollsAmount'])
		data[key]['totalAmount'] += total_amount


def read_and_process_csv(file_path, processing_func):
	"""
    Reads a CSV file and processes each row using a specified processing function.

    Parameters:
    file_path (str): The path to the CSV file to be read.
    processing_func (function): A function that processes a single row from the CSV file. 
                                It should accept two parameters: a row (dict) and a data (dict).

    Returns:
    dict: A dictionary containing processed data.

    This function performs the following steps:
    1. Initializes an empty dictionary to store processed data.
    2. Opens the CSV file for reading.
    3. Uses csv.DictReader to read the file into a dictionary format where each row is a dictionary.
    4. Iterates over each row in the CSV file.
    5. Applies the specified processing function to each row.
    6. Handles file-related exceptions (FileNotFoundError, PermissionError, and general exceptions).
    7. Handles row-specific processing exceptions and logs errors.

    Raises:
    FileNotFoundError: If the specified file does not exist.
    PermissionError: If there are permissions issues with the specified file.
    Exception: For other general I/O errors.
    """
	# Initialize an empty dictionary to store processed data

	data = {}
	try:
		with open(file_path, mode='r', newline='') as input_file:
			table = csv.DictReader(input_file, delimiter=',')
			print(f"File successfully read from path: {file_path}")
			# Iterate over each row in the CSV file
			for row in table:
				try:
					processing_func(row, data)
				except Exception as e:
					print(f"Error processing row {row}: {e}")
	except FileNotFoundError:
		print(f"Error: The file {file_path} was not found.")
	except PermissionError:
		print(f"Error: Permission denied for file {file_path}.")
	except Exception as e:
		print(f"An error occurred while reading the file {file_path}: {e}")
	
	return data


def write_data(file_path, fields, data):
	"""
    Writes data to a CSV file with specified field names.

    Parameters:
    file_path (str): The path to the CSV file to be written.
    fields (list): A list of field names for the CSV header.
    data (list of dict): A list of dictionaries containing the data to be written to the CSV file.

    This function performs the following steps:
    1. Opens the CSV file for writing.
    2. Creates a DictWriter object with the specified field names.
    3. Writes the header to the CSV file.
    4. Writes the rows of data to the CSV file.
    5. Handles file-related exceptions (IOError).
    6. Ensures the file is properly closed after writing.
    """

	try:
		with open(file_path, 'w', newline='') as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames=fields)
			writer.writeheader()
			writer.writerows(data)
		csvfile.close()
		print(f"File successfully written to path: {file_path}")
	except IOError as e:
		print(f"An error occurred while writing the file {file_path}: {e}")


def filter(row, val, operation):
	"""
    Determines whether a given value exceeds a specified threshold.

    Parameters:
    value (float): The value to be compared.
    threshold (float): The threshold against which the value is compared.

    Returns:
    bool: True if the value is greater than the threshold, otherwise False.

    This function performs a simple comparison to check if the value exceeds the threshold.
    It is intended to be used as a filtering condition in other data processing functions.
    """

    # Check if both row and val are numeric data 
	if not isinstance(row, float) or not isinstance(val, float):
		raise TypeError("Both 'row' and 'val' must be float type")

	if operation == 'gt':
		return row > val
	elif operation == 'lt':
		return row < val
	elif operation == 'ge':
		return row >= val
	elif operation == 'le':
		return row <= val
	elif operation == 'eq':
		return row == val
	elif operation == 'ne':
		return row != val
	else:
		raise ValueError(f"Unsupported operation: {operation}")


def get_sample_rows(csv_file_path, sample_size):
    """
    Read the CSV file and return a list of randomly selected sample rows.

    Args:
        csv_file_path (str): Path to the CSV file.
        sample_size (int): Number of sample rows to select.

    Returns:
        list: List of randomly selected sample rows.
    """
    sample_rows = []
    with open(csv_file_path, 'r', newline='') as csv_file:
        reader = csv.DictReader(csv_file)
        all_rows = list(reader)
        sample_rows = random.sample(all_rows, sample_size)
    return sample_rows
