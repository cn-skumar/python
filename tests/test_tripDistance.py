import unittest
import sys
sys.path.append("/Users/skumar/Desktop/sample py")  # Adjust the path to your project directory
from functions.utils import get_sample_rows, filter

class TestCalcTotals(unittest.TestCase):
    def setUp(self):
        # Prompt user for CSV file path
        csv_file_path = input("Enter the path to the CSV file: ").strip()
        
        # Read CSV file and randomly select sample rows
        sample_size = 5  # Number of sample rows to select
        self.sample_rows = get_sample_rows(csv_file_path, sample_size)

    def test_filter_greater_than(self):
        for row in self.sample_rows:
        # Test filter function with 'greater than' condition
            shortestDistance = float(row['shortestDistance'])
            self.assertTrue(filter(shortestDistance, 0.0, 'gt'))

            longestDistance = float(row['longestDistance'])
            self.assertTrue(filter(longestDistance, 0.0, 'gt'))

    def test_hour_range(self):
        """
        Test if the 'hour' field falls within the range of 0 to 23.

        This test case iterates through sample rows and checks if the 'hour'
        values are between 0 and 23 (inclusive).

        It verifies that the 'hour' field in each sample row falls within the
        expected range.

        """
        for row in self.sample_rows:
            # Retrieve the 'hour' value from the sample row
            hour = int(row['hour'])
            
            # Assert that the 'hour' is between 0 and 23 (inclusive)
            self.assertTrue(0 <= hour <= 23)

if __name__ == '__main__':
    unittest.main()

# /Users/skumar/Desktop/sample py/output/tripDistance.csv
# output/amountPaid.csv  