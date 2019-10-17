from dataclasses import dataclass, FrozenInstanceError
from collections import OrderedDict
from abc import ABC
import pprint

import sys
from io import StringIO
import fire
import inspect
import argparse
import functools


# @dataclass
class MasterConfig(ABC):
    # The config name
    name: str

    # self.config = config

    # Freezes the config after setup, turning it immutable
    # freeze_config: bool = True

    def get_parameters(self):
        return OrderedDict(sorted(vars(self).items()))

    # def __str__(self):
    #     return pprint.pformat(dict(self.get_parameters()))

    def freeze(self):
        ''' Freezes object, making it immutable '''
        def handler(self, name, value):
            err_msg = (
                f"Cannot assign to field '{name}'. Config object is frozen. "
                "Change 'freeze_config' to False if you want a mutable config object"
            )
            raise FrozenInstanceError(err_msg)

        setattr(MasterConfig, '__setattr__', handler)


def setup_config(default_config=None):  # TODO: Handle None
    config_str = parse_args(default_config)
    config = choose_config(config_str)
    return config


def parse_args(default_config):
    p = argparse.ArgumentParser()

    p.add_argument('--config',
                   type=str,
                   default=default_config,
                   help='What config class to choose')

    args, _ = p.parse_known_args()
    return args.config


def choose_config(config_str):
    # Create config object
    available_configs = get_available_configs()
    try:
        config_class_ = available_configs[config_str]
        config_obj = config_class_(config_str)
    except KeyError as e:
        err_msg = f"Config class '{config_str}' wasn't found. Feel free to create it as a new config class or use one of the existing ones -> {set(available_configs)}"
        raise KeyError(err_msg) from e

    # Overwrite parameters via optional input flags
    config_obj = overwrite(config_obj)

    # # Freezes config
    # if config_obj.freeze_config:
    #     config_obj.freeze()
    return config_obj


def get_available_configs():
    available_configs = {}
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(obj) and issubclass(obj, MasterConfig):
            available_configs[name] = obj
    print(available_configs)
    available_configs.pop('MasterConfig')
    return available_configs


def overwrite(config_obj):
    ''' Overwrites parameters with input flags. Function is needed for the
  convenience of specifying parameters via a combination of the config classes
  and input flags. '''
    class NullIO(StringIO):
        def write(self, txt):
            pass

    def parse_unknown_flags(**kwargs):
        return kwargs

    sys.stdout = NullIO()
    extra_arguments = fire.Fire(parse_unknown_flags)
    sys.stdout = sys.__stdout__

    for key, val in extra_arguments.items():
        if key not in vars(config_obj):
            err_str = f"The input parameter '{key}' isn't allowed. It's only possible to overwrite attributes that exist in the DefaultConfig class. Add your input parameter to the default class or catch it before this message"
            raise NotImplementedError(err_str)
        setattr(config_obj, key, val)

    return config_obj


def config_class_old(func):
    print("WOOW")
    print(func)
    qwe
    class_name = func.__name__
    err_msg = (f"Can't decorate '{class_name}' of type {type(func)}. "
               "Can only be used for classes")
    assert inspect.isclass(func), err_msg
    err_msg = (f"Can't decorate '{class_name}' since it's not a sublass of "
               "'chilliconfig.MasterConfig'")
    assert issubclass(func, MasterConfig), err_msg
    setattr(sys.modules[__name__], class_name, func)


# @dataclass
# def config_class(_cls=None,
#                  *,
#                  init=True,
#                  repr=True,
#                  eq=True,
#                  order=False,
#                  unsafe_hash=False,
#                  frozen=False):


def config_class(_cls=None,
                 *,
                 init=True,
                 repr=True,
                 eq=True,
                 order=False,
                 unsafe_hash=False,
                 frozen=False):
    print(f'Class: {_cls}')
    print(frozen)
    d = dataclass(_cls,
                  init=init,
                  repr=repr,
                  eq=eq,
                  order=order,
                  unsafe_hash=unsafe_hash,
                  frozen=frozen)

    def my_return(func):  # becomes cookie
        print("MY RETURN")
        print(func)
        # qwe

        @functools.wraps(func)
        def my_wrap(f):
            print("MY WRAP")
            print(f)
            print(func)

            func1 = func(f)
            class_name = func1.__name__
            err_msg = (f"Can't decorate '{class_name}' of type {type(func1)}. "
                       "Can only be used for classes")
            assert inspect.isclass(func1), err_msg
            err_msg = (
                f"Can't decorate '{class_name}' since it's not a sublass of "
                "'chilliconfig.MasterConfig'")
            assert issubclass(func1, MasterConfig), err_msg
            setattr(sys.modules[__name__], class_name, func1)
            # print(func1(f))
            return func

        # print(func.__name__)

        return my_wrap

    return my_return(d)

    # return my_return

    def wrap(cls):
        return _process_class(cls, init, repr, eq, order, unsafe_hash, frozen)

    # See if we're being called as @dataclass or @dataclass().
    if _cls is None:
        # We're called with parens.
        return wrap

    # We're called as @dataclass without parens.
    return wrap(_cls)
