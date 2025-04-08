"""
Author: Edward Ding
Date: March 4th, 2025
Description: This script processes a CSV file containing Gradescope assignment lateness data for students, 
converts lateness from H:M:S format to a decimal representation of days and 
calculates the number of HW and Lab late days used. The results are stored in a new CSV file.
"""

import csv
import math
import argparse

def convert_lateness_to_days(lateness_str):
    # Function to convert lateness from H:M:S format to a decimal representation of days.
    
    # Check if the input is empty, None, or exactly "00:00:00"
    
    if not lateness_str or lateness_str == "00:00:00":
        return 0.0  
    
    # Split the input string into hours, minutes, and seconds
    time_parts = lateness_str.split(":")
    
    # Convert the split string values into integers
    hours = int(time_parts[0])
    minutes = int(time_parts[1])
    seconds = int(time_parts[2])
    
    # - 1 hour is 1/24 of a day
    # - 1 minute is 1/1440 of a day
    # - 1 second is 1/86400 of a day
    lateness_in_days = (hours / 24) + (minutes / 1440) + (seconds / 86400)

    if lateness_in_days < (1/24):
        print("Since late days are less than 1 hour, we will round to 0.0")
        return 0.0
    
    # Round the final result to 4 decimal places for consistency
    lateness_in_days = round(lateness_in_days, 4)
    
    # Return the computed lateness in days
    return lateness_in_days


# Set up argument parser
parser = argparse.ArgumentParser(description="Process lateness data from a Gradescope export CSV file.")
parser.add_argument("input_file", help="The name of the input CSV file")
args = parser.parse_args()

input_filename = args.input_file  # Get input file name from the command-line argument
output_filename = "processed_late_days.csv"


# Read the CSV file and process lateness columns
with open(input_filename, newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    headers = next(reader)  # Read the header row

    lateness_columns = [i for i, col in enumerate(headers) if "Lateness" in col]
    
    # Store processed rows and switch around first and second columns for (Last, First) format
    processed_data = [[headers[1], headers[0], headers[2], headers[3]] + [headers[i] for i in lateness_columns[:-1]]]  # Swap first two columns
    
    for row in reader:
        processed_row = [row[1], row[0], row[2], row[3]] + [convert_lateness_to_days(row[i]) for i in lateness_columns[:-1]]
        processed_data.append(processed_row)

    # Used for debugging purposes, just the columns from the raw spreadsheet with lateness columns, optional. 
    with open("late_columns.csv", "w", newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(processed_data[0])
        writer.writerows(processed_data[1:])



# Process the data for HW and Lab lateness count
output_rows = []
output_headers = [headers[1], headers[0], headers[2], headers[3]] + ["Num HW Late Days", "Num Lab Late Days"]

actualHeaders = processed_data[0]

for i in range(4, len(actualHeaders)):
    processed_data[0][i] = actualHeaders[i].replace("Lateness (H:M:S)", "Lateness")

# Display the results
for x in range(1,len(processed_data)):
    row = processed_data[x]
    print("Now processing" + str(row))
    numHW = 0
    numLab = 0

    for i in range(4, len(row)):
        if "H" in actualHeaders[i]:
            print("Processing", actualHeaders[i], "with row value", math.ceil(row[i]))
            if math.ceil(float(row[i])) < 3:
                numHW += math.ceil(float(row[i]))
        elif "Lab" in actualHeaders[i]:
            print("Processing", actualHeaders[i], "with row value", math.ceil(row[i]))
            if math.ceil(float(row[i])) < 3:
                numLab += math.ceil(float(row[i]))
    print("Number of HW late days used:", numHW)
    print("Number of Lab late days used:", numLab)
    output_rows.append(row[:4] + [numHW, numLab])

# Sort the rows by last name (first column in the CSV)
output_rows.sort(key=lambda x: x[0])

# Save the processed data to a new CSV file
with open("processed_late_days.csv", "w", newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(output_headers)
    writer.writerows(output_rows)

print("Processed data saved to processed_late_days.csv")



