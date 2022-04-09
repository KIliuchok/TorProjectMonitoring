import json


def json_extract(obj, key):

    array = []

    def extract(obj, array, key):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, array, key)
                elif k == key:
                    array.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, array, key)

        return array

    values = extract(obj, array, key)
    return values

def json_extract_from_file(file, key):
    with open(file, 'r') as _file:
        
        data = json.load(_file)

        return json_extract(data, key)