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


@dataclass
class MasterConfig(ABC):
  # The config name
  config: str

  # Freezes the config after setup, turning it immutable
  freeze_config: bool = True


  def get_parameters(self):
    return OrderedDict(sorted(vars(self).items()))

  def __str__(self):
    return pprint.pformat(dict(self.get_parameters()))

  def freeze(self):
    ''' Freezes object, making it immutable '''
    def handler(self, name, value):
      err_msg = f"Cannot assign to field '{name}'. Config object is frozen. Change 'freeze_config' to False if you want a mutable config object"
      raise FrozenInstanceError(err_msg)

    setattr(MasterConfig, '__setattr__', handler)


def setup(default_config=None): # TODO: Handle None
  config_str = parse_args(default_config)
  config = choose_config(config_str)
  print(config)

def parse_args(default_config):
  p = argparse.ArgumentParser()

  p.add_argument('--config',
                 type=str,
                 default=default_config,
                 help='What config class to choose')

  args, unknown = p.parse_known_args()
  return args.config

def choose_config(config_str):
  # Create config object
  available_configs = get_available_configs()
  try:
    config_class = available_configs[config_str]
    config_obj = config_class(config_str)
  except KeyError as e:
    err_msg = f"Config class '{config_str}' wasn't found. Feel free to create it as a new config class or use one of the existing ones -> {set(available_configs)}"
    raise KeyError(err_msg) from e

  # Overwrite parameters via optional input flags
  # config_obj = overwrite(config_obj)

  # Freezes config
  # if config_obj.freeze_config:
  #   config_obj.freeze()
  print("BEFORE RETURN")
  # print(config_obj)
  return config_obj


def get_available_configs():
  print("AVAILABLE CONFIGS-------")
  available_configs = {}
  for name, obj in inspect.getmembers(sys.modules[__name__]):
    print(name)
    if inspect.isclass(obj) and issubclass(obj, MasterConfig):
      available_configs[name] = obj
  # available_configs.pop('MasterConfig')

  print(available_configs)
  # qew
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


def mark(func):
  print("IN DECORATOR")
  aa = sys.modules[__name__]
  print(aa)
  setattr(sys.modules[__name__], 'Cookie', func)
  print(func)
  print(type(func))
  # qwe
  @functools.wraps(func)
  def wrapper_timer(*args, **kwargs):
    print("Something is happening before the function is called.")
    value = func(*args, **kwargs)
    print("Something is happening after the function is called.")
    # return value

  return wrapper_timer