import unittest
import sys
sys.path.append("/Users/skumar/Desktop/sample py")  # Adjust the path to your project directory
from functions.utils import get_sample_rows, filter

class TestTripDistance(unittest.TestCase):
    def setUp(self):
        # Prompt user for CSV file path
        csv_file_path = input("Enter the path to the CSV file: ").strip()
        
        # Read CSV file and randomly select sample rows
        sample_size = 5  # Number of sample rows to select
        self.sample_rows = get_sample_rows(csv_file_path, sample_size)


    def test_filter_greater_than(self):
        for row in self.sample_rows:
        # Test filter function with 'greater than' condition
            cumulative_tipAmount = float(row['cumulative_tipAmount'])
            self.assertTrue(filter(cumulative_tipAmount, 0.0, 'ge'))

            cumulative_tollsAmount = float(row['cumulative_tollsAmount'])
            self.assertTrue(filter(cumulative_tollsAmount, 0.0, 'ge'))

            totalAmount = float(row['totalAmount'])
            self.assertTrue(filter(totalAmount, 0.0, 'gt'))
            
    
    def test_rate_code_id_range(self):
        """
        Test if the 'rateCodeId' field falls within the range of 1 to 5 as provided in the NYC dataset documentation.

        This test case iterates through sample rows and checks if the 'rateCodeId'
        values are between 1 and 5 (inclusive).

        It verifies that the 'rateCodeId' field in each sample row falls within the
        expected range.

        """
        for row in self.sample_rows:
            # Retrieve the 'rateCodeId' value from the sample row
            rate_code_id = int(row['rateCodeId'])
            
            # Assert that the 'rateCodeId' is between 1 and 5 (inclusive)
            self.assertTrue(1 <= rate_code_id <= 5)


if __name__ == '__main__':
    unittest.main()

# /Users/skumar/Desktop/sample py/output/tripDistance.csv
# output/amountPaid.csv  