import json
import os
from bs4 import BeautifulSoup
import re

def find_nested_type(soup, path_parts):
    current_element = soup
    for part in path_parts:
        # Find the row containing current part
        found = False
        rows = current_element.find_all('tr')
        for row in rows:
            cells = row.find_all('td')
            if len(cells) < 2:
                continue
                
            cell_text = cells[0].get_text(strip=True).replace('*', '')
            if cell_text == part:
                # Found our property, now check its type
                type_cell = cells[1]
                
                # If this is the last part in our path, extract the type
                if part == path_parts[-1]:
                    # Check for array
                    array_depth = str(type_cell).count('[')
                    
                    # Look for basic types
                    cell_text = str(type_cell)
                    if 'integer($int64)' in cell_text:
                        base_type = 'integer($int64)'
                    elif 'integer' in cell_text:
                        base_type = 'integer'
                    elif 'string' in cell_text:
                        base_type = 'string'
                    elif 'boolean' in cell_text:
                        base_type = 'boolean'
                    elif 'number' in cell_text:
                        base_type = 'number'
                    else:
                        # Check if it's an object with a wildcard property
                        wildcard_row = type_cell.find('td', string=lambda x: x and '<' in x and '>' in x)
                        if wildcard_row:
                            # Get the type of the wildcard property
                            wildcard_type = wildcard_row.find_next_sibling('td').get_text(strip=True)
                            if 'string' in wildcard_type:
                                base_type = 'string'
                            else:
                                base_type = wildcard_type
                        else:
                            base_type = 'string'  # default
                    
                    # Wrap in arrays if needed
                    result = base_type
                    for _ in range(array_depth):
                        result = [result]
                    return result
                
                # Not the last part, find the inner table for nested objects
                inner_table = type_cell.find('table', class_='model')
                if inner_table:
                    current_element = inner_table
                    found = True
                    break
        
        if not found:
            return None
            
    return None

def process_empty_objects():
    # Read the empty objects file
    with open('3-Fill Out Empty Values/empty_objects.json', 'r') as f:
        empty_objects = json.load(f)
    
    filled_objects = {}
    
    for key, _ in empty_objects.items():
        # Split the path into parts
        parts = key.split('.')
        if not parts:
            continue
            
        file_name = parts[0]
        property_path = parts[1:]  # Rest are the property path parts
        
        if not property_path:
            continue
            
        html_file = f'2-Get Raw HTML Components/models/{file_name}.html'
        
        if not os.path.exists(html_file):
            print(f"Warning: {html_file} not found")
            continue
            
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
            
        soup = BeautifulSoup(html_content, 'html.parser')
        type_def = find_nested_type(soup, property_path)
        
        if type_def:
            filled_objects[key] = type_def
        else:
            print(f"Warning: Could not find type for {key}")
    
    # Write the result to a new file
    with open('filled_objects.json', 'w') as f:
        json.dump(filled_objects, f, indent=2)

if __name__ == "__main__":
    process_empty_objects()
