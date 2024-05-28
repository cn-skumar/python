import sys
sys.path.append("/Users/skumar/Desktop/sample py")  # Adjust the path to your project directory
from functions.utils import * # Import necessary functions from the functions.utils module

# Check if the script is executed as the main program
if __name__ == "__main__":
    # Define the file path for reading/ writing the CSV data
    file_path = '/Users/skumar/Downloads/nyc_sample.csv'
    write_path = 'output/Question#2/out_amountPaid.csv'

    # Read and process the CSV data using the read_and_process_csv function
    # The calc_totals function is passed as an argument to perform the processing
    data = read_and_process_csv(file_path, calc_totals)
    print("Data processed successfully.")

    # Define the headers for the output CSV file
    headers = ['rateCodeId', 'cumulative_tipAmount', 'cumulative_tollsAmount', 'totalAmount']

    # Initialize an empty list to store the rows of the output CSV file
    rows = []

    # Iterate through the processed data, sorted by rateCodeId
    for rateCodeId, values in sorted(data.items()):
        # Create a dictionary representing a row of the output CSV file
        row = {
            'rateCodeId': rateCodeId,
            'cumulative_tipAmount': round(values['tipAmount'], 2),
            'cumulative_tollsAmount': round(values['tollsAmount'], 2),
            'totalAmount': round(values['totalAmount'], 2)
        }

        # Append the row to the list of rows
        rows.append(row)

    # Write the processed data to the output CSV file using the write_data function
    write_data(write_path, headers, rows)