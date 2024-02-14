import sys

file_name = sys.argv[1]
number_to_check = sys.argv[2]

# Open the file for reading
with open(file_name, 'r') as file:
    lines = file.readlines()

# Check if the specified number is present and 'eHadCoinTime_Offset' is present in the next line
found_number = False
found_eHadCoinTime_Offset = False

for line in lines:
    if number_to_check in line:
        found_number = True
    elif found_number and 'eHadCoinTime_Offset' in line:
        found_eHadCoinTime_Offset = True
        break

# Output to noCT_Offset_runs.txt if conditions are not met
if not (found_number and found_eHadCoinTime_Offset):
    with open('noCT_Offset_runs.txt', 'w') as output_file:
        output_file.write("{}".format(int(number_to_check)))
