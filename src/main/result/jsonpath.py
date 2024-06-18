from jsonpath_ng import jsonpath, parse
import json
import zipfile


def create_jsonpath_for_key(json_data, target_key):
    def _create_jsonpath(json_data, target_key, current_path=''):
        if isinstance(json_data, dict):
            if target_key in json_data:
                return f"{current_path}.{target_key}"
            else:
                for key, value in json_data.items():
                    result = _create_jsonpath(value, target_key, f"{current_path}.{key}")
                    if result is not None:
                        return result

        elif isinstance(json_data, list):
            for index, item in enumerate(json_data):
                result = _create_jsonpath(item, target_key, f"{current_path}[{index}]")
                if result is not None:
                    return result
        return None

    return _create_jsonpath(json_data, target_key)[1:]  # Remove the leading '.'
