from nightingale.helpers import SortedDict
import pytest
def test_sorted_dict():
    sd = SortedDict()
    sd['a'] = 1
    sd['b'] = 2
    sd['c'] = 3
    assert sd['a'] == 1
    assert sd['b'] == 2
    assert sd['c'] == 3

    # test order is preserved
    assert list(sd.keys()) == ['a', 'b', 'c']

    # test order is preserved after deletion
    del sd['a']
    assert sd['b'] == 2
    assert sd['c'] == 3
    assert 'a' not in sd
    assert list(sd.keys()) == ['b', 'c']
    with pytest.raises(KeyError):
        sd['a']

    # test deleted keys are not in the dict
    assert 'a' not in sd

    # test ValueError is raised when old key is added again
    with pytest.raises(ValueError):
        sd['b'] = 4

    assert list(sd.keys()) == ['b', 'c']
    assert list(sd.values()) == [2, 3]
    assert sd['b'] == 2
    assert sd['c'] == 3
    

    sd['a'] = 5
    assert list(sd.keys()) == ['b', 'c', 'a']
    assert sd['a'] == 5
    assert sd['c'] == 3
    