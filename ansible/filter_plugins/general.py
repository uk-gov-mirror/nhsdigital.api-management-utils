from typing import List


def dict_list_to_map(list_of_maps: List[dict], key_attr: str, val_attr: str = None):

    def _get_val(current):
        if not val_attr:
            return current
        return current.get(val_attr)

    return {item[key_attr]: _get_val(item) for item in list_of_maps}


class FilterModule:

    @staticmethod
    def filters():
        return {
            'dict_list_to_map': dict_list_to_map
        }
