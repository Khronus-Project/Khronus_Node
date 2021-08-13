from os import environ 
import json
from dotenv import load_dotenv

load_dotenv()
with open(environ["GRAMMARS"]) as f:
    grammars = json.load(f)

# The action flag will be always the tailing part of the byte input 

def get_action_type(_byte_input):
    byte_input_length = len(_byte_input)
    action_flag_length = 3
    raw_bytes = _byte_input[byte_input_length-action_flag_length:byte_input_length]
    action_type = type_switch(3)(raw_bytes)
    print(action_type)
    if action_type not in grammars["Action_Types"]:
        raise ValueError(f"The type {action_type} that came with the byte request is not a valid action type")
    else:
        return action_type


def decode(_byte_input, _action_type):
    grammar = grammars[_action_type]
    assert len(_byte_input) == grammar["InputLenght"], "Input Data is Incorrect"
    result = {}
    for field in grammar['Fields']:
        data_type = field["Type"] # 0 hex, 1 int, 2 timestamp will approximate it to the closest minute, string in UTF-8)
        location = field["Location"]
        key = field['Name']
        raw_bytes = _byte_input[location[0]:location[1]]
        result[key] = type_switch(data_type)(raw_bytes)
    return result

def type_switch(_type):
    type_definitions = {
        0:get_hex,
        1:get_int,
        2:get_time,
        3:get_string
    }
    return type_definitions.get(_type,lambda _bytes: _bytes)

# Returns and integer
def get_int(_bytes):
    return int.from_bytes(_bytes,"big")

# Returns and integer
def get_hex(_bytes):
    return str(_bytes.hex())

# Returns a unix timestamp aproximated to the closest minute
def get_time(_bytes):
    received_time = get_int(_bytes)
    seconds_from_prev = received_time%60
    prev_min = received_time - seconds_from_prev
    if seconds_from_prev <= 30:
        return prev_min
    else:
        return prev_min+60

def get_string(_bytes):
    return _bytes.decode('UTF-8')


    