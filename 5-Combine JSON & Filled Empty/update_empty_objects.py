import json
import os

def get_object_paths(obj, current_path='', paths=None):
    """Recursively find all paths to empty objects in a JSON structure."""
    if paths is None:
        paths = []
    
    if isinstance(obj, dict):
        for key, value in obj.items():
            new_path = f"{current_path}.{key}" if current_path else key
            if value == {}:
                # Remove leading dot if present
                clean_path = new_path[1:] if new_path.startswith('.') else new_path
                paths.append(clean_path)
            else:
                get_object_paths(value, new_path, paths)
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            new_path = f"{current_path}[{i}]"
            get_object_paths(item, new_path, paths)
    
    return paths

def find_matching_path(path, filled_objects):
    """Find a matching path in filled_objects by trying different combinations."""
    # Split path into components
    components = path.split('.')
    
    # Try different combinations of the path
    for i in range(len(components)):
        # Create potential paths by joining different numbers of components
        potential_path = '.'.join(components[i:])
        if potential_path in filled_objects:
            return potential_path
        
        # Also try with the last component
        if i == 0:
            last_component = components[-1]
            if last_component in filled_objects:
                return last_component
    
    return None

def update_value_at_path(obj, path, new_value):
    """Update a value at a specific path in a nested dictionary."""
    if not path:
        return

    components = path.split('.')
    current = obj
    
    # Navigate to the parent of the target
    for component in components[:-1]:
        if '[' in component:  # Handle array indices
            base = component[:component.index('[')]
            index = int(component[component.index('[')+1:component.index(']')])
            current = current[base][index]
        else:
            current = current[component]
    
    # Update the target
    last_component = components[-1]
    if '[' in last_component:  # Handle array indices
        base = last_component[:last_component.index('[')]
        index = int(last_component[last_component.index('[')+1:last_component.index(']')])
        current[base][index] = new_value
    else:
        current[last_component] = new_value

def main():
    # File paths
    base_dir = 'd:/Repositories/crossref_json_model'
    expanded_model_path = os.path.join(base_dir, '1-Get JSON Raw', 'crossref_models_expanded.json')
    filled_objects_path = os.path.join(base_dir, '4-Fill Empty Objects', 'filled_objects.json')
    output_path = os.path.join(base_dir, '5-Combine JSON & Filled Empty', 'crossref_models_expanded_updated.json')

    # Read the JSON files
    with open(expanded_model_path, 'r', encoding='utf-8') as f:
        expanded_model = json.load(f)
    
    with open(filled_objects_path, 'r', encoding='utf-8') as f:
        filled_objects = json.load(f)

    # Find all paths to empty objects
    empty_paths = get_object_paths(expanded_model)
    
    # Update each empty object with its corresponding value from filled_objects
    updates_made = 0
    for path in empty_paths:
        # Find the best matching path in filled_objects
        matching_path = find_matching_path(path, filled_objects)
        
        if matching_path:
            update_value_at_path(expanded_model, path, filled_objects[matching_path])
            updates_made += 1
            print(f"Updated: {path} with value from {matching_path}")
        else:
            print(f"Warning: No matching value found for {path}")

    # Save the updated model
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(expanded_model, f, indent=2)

    print(f"\nCompleted! Made {updates_made} updates.")
    print(f"Updated file saved to: {output_path}")

if __name__ == "__main__":
    main()
