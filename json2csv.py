import json
import csv
# Transform json to csv for testing

# Sample JSON data
json_data = [
    {"name": "Alice", "age": 30, "city": "New York"},
    {"name": "Bob", "age": 25, "city": "Los Angeles"},
    {"name": "Charlie", "age": 35, "city": "Chicago"}
]

# Define the CSV file path
csv_file_path = "output.csv"

# Write JSON data to CSV
with open(csv_file_path, mode='w', newline='') as file:
    # Create a CSV writer
    writer = csv.DictWriter(file, fieldnames=json_data[0].keys())
    
    # Write the header
    writer.writeheader()
    
    # Write the rows
    writer.writerows(json_data)
    
print(f"JSON has been successfully converted to {csv_file_path}")