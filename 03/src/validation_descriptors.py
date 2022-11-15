# The Validator abstract class is taken from the official docs
# https://docs.python.org/3/howto/descriptor.html

import string
from abc import ABC, abstractmethod


class Validator(ABC):
    def __set_name__(self, owner, name):
        self.private_name = '_' + name

    def __get__(self, obj, objtype=None):
        return getattr(obj, self.private_name)

    def __set__(self, obj, value):
        self.validate(value)
        setattr(obj, self.private_name, value)

    @abstractmethod
    def validate(self, value):
        pass


class Integer(Validator):
    def __init__(self):
        pass

    def validate(self, value):
        if not isinstance(value, int):
            raise TypeError(f'Expected an int, got {type(value)}.')


class String(Validator):
    def __init__(self, min_len=None, max_len=None):
        self.min_len = min_len
        self.max_len = max_len

    def validate(self, value):
        if not isinstance(value, str):
            raise TypeError(f'Expected a string, got {type(value)}.')
        if self.min_len and (len(value) < self.min_len):
            raise ValueError(
                f'String {value} is too small.'
                ' Minimum length is {self.min_len}.'
            )
        if self.max_len and (len(value) > self.max_len):
            raise ValueError(
                f'String {value} is too big.'
                ' Maximum length is {self.max_len}.'
            )


class PositiveInteger(Validator):
    def __init__(self):
        pass

    def validate(self, value):
        if not isinstance(value, int):
            raise TypeError(f'Expected an int, got {type(value)}.')
        if value <= 0:
            raise ValueError(f'Expected positive integer, got {value}.')


class Login(String):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def validate(self, value):
        super().validate(value)
        if not (value.isalnum() and value[0].isalpha()):
            raise ValueError(
                'Incorrect login. Login must contain only digits '
                'and english letters. First symbol must be a letter.'
            )


class Password(String):
    alphabet_lowercase = set(string.ascii_lowercase)
    alphabet_uppercase = set(string.ascii_uppercase)
    digits = set(string.digits)
    special_chars = set('!@#$%^&*-+=<>?')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def validate(self, value):
        super().validate(value)
        is_lower = any(char in value for char in Password.alphabet_lowercase)
        is_upper = any(char in value for char in Password.alphabet_uppercase)
        is_digit = any(char in value for char in Password.digits)
        is_special = any(char in value for char in Password.special_chars)
        if not all([is_lower, is_upper, is_digit, is_special]):
            raise ValueError(
                'Password must contain at least 1 lower case, '
                'upper case, numeric, and special character'
            )
