import sys, os

file_name = sys.argv[1]
number_to_check = sys.argv[2]

# Open the file for reading
with open(file_name, 'r') as file:
    lines = file.readlines()

# Check if the specified number is present and 'eHadCoinTime_Offset' is present in the next line
found_eHadCoinTime_Offset = False

for i in range(len(lines)):
    if number_to_check in lines[i]:
        if i + 1 < len(lines) and 'eHadCoinTime_Offset' in lines[i + 1]:
            found_eHadCoinTime_Offset = True
            break

if not os.path.exists('noCT_Offset_runs.txt'):
    open('noCT_Offset_runs.txt', "w").close()
# Output to noCT_Offset_runs.txt if conditions are not met
if not (found_eHadCoinTime_Offset):
    print("{} not found!".format(number_to_check))
    with open('noCT_Offset_runs.txt', 'a') as output_file:
        output_file.write("{}\n".format(int(number_to_check)))
