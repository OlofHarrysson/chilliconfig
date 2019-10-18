from dataclasses import dataclass, FrozenInstanceError
from collections import OrderedDict
from abc import ABC
import pprint
import json

import sys
from io import StringIO
import fire
import inspect
import argparse
import functools

from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter, TerminalFormatter
from pygments.formatters import get_formatter_for_filename


@dataclass
class MasterConfig(ABC):
  # def __init__(self, config):
  #   self.config = config
  #   self.freeze_config = True
  #   print("MASTER FONCIFG INIIIIT")

  print("I AM MASTERCONFIG")
  config: str

  # _frozen: bool = True
  freeze_config: bool = True

  def get_parameters(self):
    params = vars(self)
    # print(params)
    # qweeeee
    # frozen = params.pop('_frozen')
    return OrderedDict(sorted(params.items()))

  def __str__(self):
    params = self.get_parameters()
    params = dict(self.get_parameters())
    ss = ""
    for key, val in params.items():
      # print(key)
      # print(val)
      if isinstance(val, str) and '\n' in val:
        # print(val)
        # qweeeeee
        val = highlight(val, PythonLexer(), TerminalFormatter())
        s = f"{{'{key}': \n{val}}}"
      else:
        # s = f'{key}={val}\n'
        s = pprint.pformat({key: val})
      ss = f'{ss}{s}\n'

    # return ss
    print(ss)
    qwe
    # return ss
    # print(params)
    # return "{" + "\n".join("{!r}: {!r},".format(k, v)
    #                        for k, v in params.items()) + "}"
    # return params
    return pprint.pformat(params)

  def freeze(self):
    ''' Freezes object, making it immutable '''
    def handler(self, name, value):
      err_msg = (
        f"Cannot assign to field '{name}'. Config object is frozen. "
        "Change 'freeze_config' to False if you want a mutable config object")
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
  if config_obj.freeze_config:
    config_obj.freeze()
  return config_obj


def get_available_configs():
  available_configs = {}
  for name, obj in inspect.getmembers(sys.modules[__name__]):
    if inspect.isclass(obj) and issubclass(obj, MasterConfig):
      available_configs[name] = obj
  # print(available_configs)
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


def config_class(func):
  class_name = func.__name__
  err_msg = (f"Can't decorate '{class_name}' of type {type(func)}. "
             "Can only be used for classes")
  assert inspect.isclass(func), err_msg
  err_msg = (f"Can't decorate '{class_name}' since it's not a sublass of "
             "'chilliconfig.MasterConfig'")
  assert issubclass(func, MasterConfig), err_msg
  setattr(sys.modules[__name__], class_name, func)
  return func


def config_class(func):
  class_name = func.__name__
  err_msg = (f"Can't decorate '{class_name}' of type {type(func)}. "
             "Can only be used for classes")
  assert inspect.isclass(func), err_msg
  err_msg = (f"Can't decorate '{class_name}' since it's not a sublass of "
             "'chilliconfig.MasterConfig'")
  assert issubclass(func, MasterConfig), err_msg
  setattr(sys.modules[__name__], class_name, func)

  return dataclass(func,
                   init=True,
                   repr=False,
                   eq=False,
                   order=False,
                   unsafe_hash=False,
                   frozen=False)
