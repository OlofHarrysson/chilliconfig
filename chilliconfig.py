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
import pickle
from collections import defaultdict

from dill.source import getsource

from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter, TerminalFormatter
from pygments.formatters import get_formatter_for_filename

RECORD_STATE = 0
RECORDED_FUNCTIONS = defaultdict(list)
RECORD_COUNTER = 0

recorded_funcs = dict()


def print_source(func):
  print(func)
  class_name = func.__name__
  err_msg = (f"Can't decorate '{class_name}' of type {type(func)}. "
             "Can only be used for classes")
  assert inspect.isclass(func), err_msg

  def __print_source__(self):
    src = inspect.getsource(self.__class__) + '\n'

    # Get my source. Get my childrens sources
    for key, val in vars(self).items():
      if hasattr(val, '__anyfig_print_source__'):
        src += __print_source__(val)

    return src

  setattr(func, '__anyfig_print_source__', __print_source__)
  return func


class SourceCode():
  def __str__(self):
    src = inspect.getsource(self.__class__) + '\n'

    # Get my source. Get my childrens sources
    for key, val in vars(self).items():
      if issubclass(val.__class__, SourceCode):
        src += str(val)

    return src


def load_config(path):
  print("Loading config")
  with open(path, 'rb') as f:
    return pickle.load(f)


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

  def save(self, path):
    print("Saving config")
    with open(path, 'wb') as f:
      pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)

  def get_parameters(self):
    return OrderedDict(sorted(vars(self).items()))

  def __str__(self):
    ss = ""
    for key, val in vars(self).items():
      if hasattr(val, '__anyfig_print_source__'):
        cls_str = val.__anyfig_print_source__()
        s = f"{{'{key}': \n{cls_str}}}"
      else:
        s = pprint.pformat({key: val})
      ss = f'{ss}{s}\n'

    return ss

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
  # PLUGINS = dict() # TODO at start of file
  # PLUGINS[func.__name__] = func instead of adding it to our module
  # print(inspect.getsource(func))
  # class_def = inspect.getsourcelines(func)
  # for cd in class_def:
  #   print(cd)
  # qew

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


def replace_with_first():
  new = dict()
  for key, val in RECORDED_FUNCTIONS.items():
    first_ele = repr(val[0])
    new[first_ele] = val
  return new


def config_func(func):
  recorded_funcs[repr(func)] = func

  @functools.wraps(func)
  def wrap(*args, **kwargs):
    mod = sys.modules[__name__]

    # Looks in stack and see what line called you
    curframe = inspect.currentframe()
    calframe = inspect.getouterframes(curframe, 1)
    called_line = calframe[1][4][0]

    # Get the attribute name
    called_var_name = called_line.replace('self.', '').split(' = ')[0].strip()
    # Save attribute name + func?
    # print(called_var_name)
    # print(func)
    # print(mod.RECORDED_FUNCTIONS)
    # TODO

    if mod.RECORD_STATE == 0:
      mod.RECORD_COUNTER += 1
    # print(RECORD_STATE)

    mod.RECORD_STATE += 1
    # print(mod.RECORD_STATE)
    # print(func)
    mod.RECORDED_FUNCTIONS[mod.RECORD_COUNTER].append(func)
    value = func(*args, **kwargs)
    mod.RECORD_STATE -= 1
    if mod.RECORD_STATE == 0:
      mod.RECORD_COUNTER += 1

    # print(mod.RECORD_STATE)
    return value

  # for name, obj in inspect.getmembers(sys.modules[__name__]):
  #   print(name)
  # qwe

  return wrap
  # return func


def show_source(func):
  return func