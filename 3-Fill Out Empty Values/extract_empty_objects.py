import json

def find_empty_objects(obj, path=""):
    empty_objects = {}
    
    if isinstance(obj, dict):
        for key, value in obj.items():
            current_path = f"{path}.{key}" if path else key
            
            if isinstance(value, dict):
                if not value:  # Empty object
                    empty_objects[current_path] = {}
                else:
                    empty_objects.update(find_empty_objects(value, current_path))
            elif isinstance(value, list):
                for i, item in enumerate(value):
                    empty_objects.update(find_empty_objects(item, f"{current_path}[{i}]"))
                    
    return empty_objects

# Read the JSON file
with open('crossref_models_expanded.json', 'r') as f:
    data = json.load(f)

# Find all empty objects
empty_objects = find_empty_objects(data)

# Write results to a new JSON file
with open('empty_objects.json', 'w', encoding='utf-8') as f:
    json.dump(empty_objects, f, indent=2, sort_keys=True)

print(f"Found {len(empty_objects)} components with empty objects. Results written to empty_objects.json")
