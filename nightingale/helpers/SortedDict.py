"""a sorted dictionary class that keeps the order of the keys"""
from typing import Dict, Optional, Union, List, Tuple, Set, Any

class SortedDict:
    def __init__(self, dictionary: Optional[Union[Dict[str, Any], List[Tuple[str, Any]]]] = None):
        dictionary = dictionary or {}
        self._keys = list(dictionary.keys()) if isinstance(dictionary, dict) else [key for key, value in dictionary]
        self._dict = dict(dictionary)
        assert len(self._keys) == len(self._dict), f"Key order length {len(self._keys)} is not equal to dictionary length {len(self._dict)}, dictionary is {dictionary}, {type(dictionary)}"

    def __len__(self):
        return len(self._dict)

    def __getitem__(self, key: str):
        if key not in self._dict and isinstance(key, int):
            return self.get_value_by_index(key)
        return self._dict[key]
    
    def get_value_by_index(self, index: int):
        return self._dict[self.get_key_by_index(index)]
    
    def get_key_by_index(self, index: int):
        return self._keys[index]
    
    def get_item_by_index(self, index: int):
        key = self.get_key_by_index(index)
        return key, self._dict[key]

    def __setitem__(self, key: str, value: Any):
        if key in self._dict:
            raise ValueError(f"Key {key} already exists in SortedDict, dictionary={self._dict}")
        self._dict[key] = value
        self._keys.append(key)

    def __delitem__(self, key: str):
        if key not in self._dict:
            raise ValueError(f"Key {key} does not exist in SortedDict, dictionary={self._dict}")
        del self._dict[key]
        self._keys.remove(key)

    def items(self):
        return [(key, self._dict[key]) for key in self._keys]
    
    def keys(self):
        return self._keys
    
    def values(self):
        return [self._dict[key] for key in self._keys]
    
    def __str__(self):
        str = '{' + ', '.join([f'{key}: {self._dict[key]}' for key in self._keys]) + '}'
        return str
    
    def __repr__(self):
        return f"SortedDict({str(self)})"

    def __eq__(self, other):
        return self._dict == other._dict and self._keys == other._keys

    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __contains__(self, key: str):
        return key in self._dict
    
    def __iter__(self):
        for key in self._keys:
            yield key, self._dict[key]

    def __reversed__(self):
        for key in reversed(self._keys):
            yield key, self._dict[key]

    def __add__(self, other):
        if isinstance(other, SortedDict):
            s = SortedDict({**self._dict, **other._dict})
            s._keys = self._keys + other._keys
            return s
        
        elif isinstance(other, dict):
            s = SortedDict({**self._dict, **other})
            s._keys = self._keys + list(other.keys())
            return s
        
        else:
            raise ValueError(f"Cannot add {type(other)} to SortedDict")
        
    def __radd__(self, other):
        if isinstance(other, SortedDict):
            s = SortedDict({**other._dict, **self._dict})
            s._keys = other._keys + self._keys
            return s
        
        elif isinstance(other, dict):
            s = SortedDict({**other, **self._dict})
            s._keys = list(other.keys()) + self._keys
            return s
        
        else:
            raise ValueError(f"Cannot add {type(other)} to SortedDict")

