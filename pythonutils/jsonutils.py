# -*- coding: UTF-8 -*-


import json


def json2dict(json_string):
    if isinstance(json_string, str):
        if json_string is None or json_string == "":
            return None

        json_data = json_string
        json_dict = json.loads(json_data)
        return json_dict
    else:
        pass


def dict2json(json_dict, default="{}"):
    if json_dict is not None and len(json_dict) != 0:
        return json.dumps(json_dict, ensure_ascii=False).encode("utf8")
    else:
        return default


def list2json(json_list, default="[]"):
    if json_list is not None and len(json_list) != 0:
        return json.dumps(json_list, ensure_ascii=False).encode("utf8")
    else:
        return default


def pretty_format(json_str):
    if isinstance(json_str, dict):
        return json.dumps(json_str, sort_keys=True, indent=4)
    else:
        return "{}"