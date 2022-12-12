import pytest
from attribute_modifier_metaclass import CustomMeta


def test_custom_metaclass():
    class CustomClass(metaclass=CustomMeta):
        x = 50

        def __init__(self, val=99):
            self.val = val

        def line(self):
            return 100

        def __str__(self):
            return "Custom_by_metaclass"

    inst = CustomClass()

    assert inst.custom_x == 50
    assert inst.custom_val == 99
    assert inst.custom_line() == 100
    assert CustomClass.custom_x == 50
    assert str(inst) == "Custom_by_metaclass"

    inst.dynamic = "added later"
    assert inst.custom_dynamic == "added later"

    with pytest.raises(AttributeError):
        inst.dynamic
    with pytest.raises(AttributeError):
        inst.x
    with pytest.raises(AttributeError):
        inst.line()
    with pytest.raises(AttributeError):
        inst.yyy
    with pytest.raises(AttributeError):
        CustomClass.x
