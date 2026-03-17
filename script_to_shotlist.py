#!/usr/bin/env python3
"""
Convert a formatted script into a shotlist template in .csv format.

The script is formatted in markdown format. For each paragraph encountered in the script:
- If the paragraph is formatted as a heading, output a row in the spreadsheet with the content as the heading in the first column.
- If the paragraph is a number, interpret that as a scene number corresponding to the script content in the paragraph immediately following.
- If the paragraph is script content, output a row in the spreadsheet with the following columns:
  1) a true/false column entitled "Done", with the default value set to false;
  2) a "Scene" column containing the scene number, taken from the script;
  3) a "Shot" column containing the shot identifier, default set to "A:";
  4) a "Media" column indicating the type of media to be shot (video, image, or animation) with default set to video
  5) a "Set" column indicating the location where shooting will take place (with default set to blank)
  6) a "Description" field describing the content to be shot;
  7) a "File" column indicating the media file on disk that contains the content;
  8) a "Script" field containing the text from the script (escaped appropriately according to the constraints of CSV files)
  9) a blank "Notes" field for entering in director's notes.
"""

import csv
import re
import sys
from typing import List, Optional, Tuple


def parse_script(script_text: str) -> List[Tuple[str, ...]]:
    """
    Parse the script text and return a list of tuples representing rows in the CSV.
    
    Args:
        script_text: The text of the script to parse.
        
    Returns:
        A list of tuples, where each tuple represents a row in the CSV.
    """
    lines = script_text.split('\n')
    rows = []
    current_scene = None
    
    for line in lines:
        line = line.strip()
        
        # Skip empty lines
        if not line:
            continue
        
        # Check if the line is a heading (starts with #)
        if line.startswith('#'):
            heading = line.lstrip('#').strip()
            rows.append((heading,))
            continue
        
        # Check if the line is a number (scene number)
        if re.match(r'^\d+$', line):
            current_scene = line
            continue
        
        # Check if the line is script content
        if current_scene is not None:
            # Default values
            done = 'False'  # Default value for "Done" column
            media = 'video' # Default media type
            shot = 'A'  # Default shot value
            set_location = ''
            description = ''
            file_path = ''
            script_text = line
            notes = ''
            
            # Create a row for the script content
            row = (done, current_scene, shot, media, set_location, description, file_path, script_text, notes)
            rows.append(row)
            current_scene = None
    
    return rows


def write_csv(rows: List[Tuple[str, ...]], output_file: str) -> None:
    """
    Write the rows to a CSV file.
    
    Args:
        rows: A list of tuples representing rows in the CSV.
        output_file: The path to the output CSV file.
    """
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write the header
        writer.writerow(['Done', 'Scene', 'Shot', 'Media', 'Set', 'Description', 'File', 'Script', 'Notes'])
        
        # Write the rows
        for row in rows:
            # Check if this is a heading row (only 1 element)
            if len(row) == 1:
                writer.writerow(row)
            else:
                # This is a data row with all 9 columns
                done, scene, shot, media, set_location, description, file_path, script_text, notes = row
                new_row = (done, scene, shot, media, set_location, description, file_path, script_text, notes)
                writer.writerow(new_row)


def main():
    """
    Main function to parse the script and write the CSV file.
    """
    if len(sys.argv) != 3:
        print("Usage: python script_to_shotlist.py <input_script> <output_csv>")
        sys.exit(1)
    
    input_script = sys.argv[1]
    output_csv = sys.argv[2]
    
    # Read the script file
    with open(input_script, 'r', encoding='utf-8') as f:
        script_text = f.read()
    
    # Parse the script
    rows = parse_script(script_text)
    
    # Write the CSV file
    write_csv(rows, output_csv)
    
    print(f"Shotlist CSV file written to {output_csv}")


if __name__ == '__main__':
    main()