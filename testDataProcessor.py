import os
import unittest
import json
from dataProcessor import read_json_file, avgAgeCountry, calculateTotalAge, countUsersByCountry, yearsToMonths

class TestDataProcessor(unittest.TestCase):
    def test_read_json_file_success(self):
        current_directory = os.path.dirname(__file__)
        file_path = os.path.join(current_directory, "users.json")

        data = read_json_file(file_path)
       
        self.assertEqual(len(data), 1000)  # Ajustar o número esperado de registros
        self.assertEqual(data[0]['name'], 'Judy Mooney')
        self.assertEqual(data[1]['age'], 48)

    def test_read_json_file_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            read_json_file("non_existent.json")

    def test_read_json_file_invalid_json(self):
        with open("invalid.json", "w") as file:
            file.write("invalid json data")
        with self.assertRaises(ValueError):
            read_json_file("invalid.json")

    def test_avgAgeCountry_empty_json(self):
        with open("empty.json", "w") as file:
            file.write("[]")
        avg_age = avgAgeCountry("empty.json")
        self.assertEqual(avg_age, {})

    def test_avgAgeCountry_missing_or_null_age(self):
        with open("missing_or_null_age.json", "w") as file:
            file.write('[{"name": "Alice", "age": null, "country": "US"}, {"name": "Bob", "age": 24, "country": "US"}]')
        avg_age = avgAgeCountry("missing_or_null_age.json")
        self.assertEqual(avg_age, {'US': 24.0})

    def test_avgAgeCountry_missing_or_null_country(self):
        with open("missing_or_null_country.json", "w") as file:
            file.write('[{"name": "Alice", "age": 30, "country": null}, {"name": "Bob", "age": 24, "country": "US"}]')
        avg_age = avgAgeCountry("missing_or_null_country.json")
        self.assertEqual(avg_age, {'US': 24.0})

    def test_calculateTotalAge(self):
        with open("test_data.json", "w") as file:
            file.write('[{"name": "Alice", "age": 30, "country": "US"}, '
                        '{"name": "Bob", "age": 24, "country": "US"}]')
            
        total_age_us = calculateTotalAge("test_data.json", "US")
        self.assertEqual(total_age_us, 54)  
    
    def test_countUsersByCountry(self):
        with open("test_country.json", "w") as file:
            file.write('[{"name": "Alice", "age": 30, "country": "US"}, '
                        '{"name": "Bob", "age": 24, "country": "US"}, '
                        '{"name": "Eva", "age": 28, "country": "UK"}, '
                        '{"name": "John", "age": 35, "country": "US"}]')
            
        user_counts = countUsersByCountry("test_country.json")
        self.assertEqual(user_counts, {'US': 3, 'UK': 1})

    def test_avgAgeCountry_with_age_transformation(self):
        with open("test_data.json", "w") as file:
            file.write('[{"name": "Alice", "age": 30, "country": "US"}, '
                        '{"name": "Bob", "age": 24, "country": "US"}, '
                        '{"name": "Eva", "age": 36, "country": "US"}, '
                        '{"name": "John", "age": 48, "country": "UK"}]')
            
        avg_age_months = avgAgeCountry("test_data.json", age_transform=yearsToMonths)
        self.assertEqual(avg_age_months, {'US': 360.0, 'UK': 576.0})

  
if __name__ == '__main__':
    unittest.main()