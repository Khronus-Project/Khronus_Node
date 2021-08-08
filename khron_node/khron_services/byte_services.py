import os, json
from dotenv import load_dotenv

load_dotenv()
with open(os.environ['DATADICT']) as f:
    datadict = json.load(f)

def decode(_byte_input):
    assert len(_byte_input) == datadict["InputLenght"], "Input Data is Incorrect"
    result = {}
    for field in datadict['Fields']:
        data_type = field["Type"] # 0 hex, 1 int, 2, timestamp (This will approximate it to the closest minute)
        location = field["Location"]
        key = field['Name']
        raw_bytes = _byte_input[location[0]:location[1]]
        result[key] = type_switch(data_type, raw_bytes)
    return result

def type_switch(_type, _bytes):
    if _type == 0:
        return get_hex(_bytes)
    elif _type == 1:
        return get_int(_bytes)
    elif _type == 2:
        return get_time(_bytes) 
    else:
        return _bytes

def get_int(_bytes):
    return int.from_bytes(_bytes,"big")

def get_hex(_bytes):
    return _bytes.hex()

def get_time(_bytes):
    received_time = get_int(_bytes)
    seconds_from_prev = received_time%60
    print(seconds_from_prev)
    prev_min = received_time - seconds_from_prev
    if seconds_from_prev <= 30:
        return prev_min
    else:
        return prev_min+60


    