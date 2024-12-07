import re
import chardet

def detect_encoding(file_path):
    """Detect the encoding of the given file."""
    with open(file_path, 'rb') as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']

        # Treat ASCII as UTF-8 because ASCII is a subset of UTF-8
        if encoding.lower() == 'ascii':
            return 'utf-8'
        return encoding
    
def scan_errors_in_files(file_list, check_negative_timestamps):
    bpm_data = {}
    invalid_files = {}

    for file in file_list:
        try:
            # Check the encoding of the file
            encoding = detect_encoding(file)

            if encoding.lower() != 'utf-8':  # Case-insensitive check
                invalid_files[file] = "Incorrect encoding (expected UTF-8)"
            
            with open(file, 'r') as f:
                lines = f.readlines()

                bpm_found = False
                r_annotation_found = False  # To ensure we only flag 'R' once
                negative_timestamp_found = False  # To ensure we only flag negative numbers once
                for line in lines:
                    # Look for BPM pattern in all lines (even those starting with #)
                    bpm_match = re.search(r'BPM:\s*(\d+(?:,\d+)?(?:\.\d+)?)', line)
                    if bpm_match:
                        bpm_value = bpm_match.group(1)
                        # Store full BPM value (including comma)
                        bpm_data[file] = bpm_value

                        # If BPM contains a comma, consider only digits before the comma for checking if BPM is too high
                        if ',' in bpm_value:
                            if file not in invalid_files:
                                invalid_files[file] = "Contains comma in BPM"
                            elif "Contains comma in BPM" not in invalid_files[file]:
                                invalid_files[file] += "; Contains comma in BPM"
                            
                            # Consider only the digits before the comma for BPM checking
                            bpm_for_checking = bpm_value.split(',')[0]
                        else:
                            bpm_for_checking = bpm_value

                        # Convert BPM to a float for checking (using the value before the comma)
                        bpm = float(bpm_for_checking)

                        # Check if BPM is too high
                        if bpm > 350:
                            if file not in invalid_files:
                                invalid_files[file] = "BPM too high"
                            elif "BPM too high" not in invalid_files[file]:
                                invalid_files[file] += "; BPM too high"

                        bpm_found = True

                    # Ignore lines starting with '#' for R annotation and negative timestamp checks
                    if not line.strip().startswith('#'):
                        # Check for lines that begin with the letter 'R', but only flag once
                        if not r_annotation_found and line.strip().startswith('R') or line.strip().startswith('G'):
                            if file not in invalid_files:
                                invalid_files[file] = "Notes using the invalid Rap (R/G) annotation"
                            elif "Notes using the invalid Rap (R/G) annotation" not in invalid_files[file]:
                                invalid_files[file] += "Notes using the invalid Rap (R/G) annotation"
                            r_annotation_found = True  # Flagged once, no need to check further

                        # Check for negative numbers, but only if checkbox is checked
                        if check_negative_timestamps and not negative_timestamp_found:
                            negative_match = re.search(r'\s-\d+', line)  # Look for negative numbers like '-1'
                            if negative_match:
                                if file not in invalid_files:
                                    invalid_files[file] = "Negative timestamps on notes present"
                                elif "Negative timestamps on notes present" not in invalid_files[file]:
                                    invalid_files[file] += "; Negative timestamps on notes present"
                                negative_timestamp_found = True  # Flagged once, no need to check further

                # If no BPM found in the file, add file to invalid list
                if not bpm_found:
                    if file not in invalid_files:
                        invalid_files[file] = "No BPM found"

        except Exception as e:
            # Handle errors when opening the file
            invalid_files[file] = f"Error reading file: {str(e)}"

    return bpm_data, invalid_files
