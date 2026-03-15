import yaml
import argparse
import logging

def process_key_ops(key: str) -> list[any]:
    corrected_path = []
    for item in key.split(","):
        if item.isdigit():
            corrected_path.append(int(item))
        else:
            corrected_path.append(item)
    return corrected_path


def modify_file(file_path: str, key: list[str], value: str):
    """
    Modifies a yaml at file_path, using key as a list of operations to perform on, setting value
    Example: key = ["abc", 2, "fc"], value = 3 will set file["abc"][2]["fc"] = 3
    """
    print(f"Modifying file {file_path}")
    
    with open(file_path) as f:
        object = yaml.safe_load(f)
    
    # Walk until 2nd last element
    current = object

    for operation in key[:-1]:
        current = current[operation]

    current[key[-1]] = value
    print(object)
    with open(file_path, 'w') as f:
        yaml.safe_dump(object, f)



parser = argparse.ArgumentParser()
parser.add_argument("--file_path", help="Path of file relative to project root to modify yaml of")
parser.add_argument("--key", help="Comma separated value of operations to perform. Ex. a,b,c = f['a']['b']['c']")
parser.add_argument("--value", help="The value to update to")
args = parser.parse_args()

ops = process_key_ops(args.key)
modify_file(file_path=args.file_path, key=ops, value=args.value)
