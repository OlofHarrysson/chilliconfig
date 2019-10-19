from dataclasses import dataclass, FrozenInstanceError, replace
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


def load_config(path):
  # TODO: Add checks so that object is config
  print("Loading config")
  with open(path, 'rb') as f:
    return pickle.load(f)


def save_config(config_obj, path):
  # TODO: Add checks so that object is config
  print(f"Saving config @ {path}")
  with open(path, 'wb') as f:
    pickle.dump(config_obj, f, pickle.HIGHEST_PROTOCOL)

  with open(path + '.txt', 'w') as f:
    f.write(str(config_obj))


@dataclass
class MasterConfig(ABC):
  def __init__(self):
    self._frozen: bool = False
    self.config_class = type(self).__name__

  def frozen(self, freeze=True):
    self._frozen = freeze

  def get_parameters(self):
    return OrderedDict(sorted(vars(self).items()))

  def __str__(self):
    str_ = ""
    params = vars(self)
    params.pop('_frozen')  # Dont print frozen
    for key, val in params.items():
      if hasattr(val, '__anyfig_print_source__'):
        cls_str = val.__anyfig_print_source__()
        s = f"'{key}':\n{cls_str}"
      else:
        s = pprint.pformat({key: val})

        # Prettyprint adds some extra wings that I dont like
        s = s.lstrip('{').rstrip('}').replace('\n ', '\n')
      str_ += s + '\n'

    return str_

  def __setattr__(self, name, value):
    # Raise error if frozen unless we're trying to unfreeze the config
    if hasattr(self, '_frozen'):
      if name == '_frozen':
        pass
      elif self._frozen:
        err_msg = (f"Cannot set attribute '{name}'. Config object is frozen. "
                   "Unfreeze the config for a mutable config object")
        raise FrozenInstanceError(err_msg)

    # Check for reserved names
    name_taken_msg = f"The attribute '{name}' can't be assigned to config '{type(self).__name__}' since it already has a method by that name"

    def assert_name(name, method_name):
      assert name != method_name, name_taken_msg

    methods = inspect.getmembers(self, predicate=inspect.ismethod)
    [assert_name(name, m[0]) for m in methods]
    object.__setattr__(self, name, value)


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
    config_obj = config_class_()
  except KeyError as e:
    err_msg = f"Config class '{config_str}' wasn't found. Feel free to create it as a new config class or use one of the existing ones marked as '@config_class' -> {set(available_configs)}"
    raise KeyError(err_msg) from e

  # Overwrite parameters via optional input flags
  config_obj = overwrite(config_obj)

  # Freezes config
  config_obj.frozen(freeze=True)
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


def print_source(func):
  class_name = func.__name__
  err_msg = (f"Can't decorate '{class_name}' of type {type(func)}. "
             "Can only be used for classes")

  assert inspect.isclass(func), err_msg

  def __print_source__(self):
    ''' Get my source. Get my childrens sources '''

    # Newline makes indention better
    src = '\n' + inspect.getsource(self.__class__)

    unique_classes = {v.__class__: v for k, v in vars(self).items()}
    for key, val in unique_classes.items():
      if hasattr(val, '__anyfig_print_source__'):
        src += __print_source__(val)

    # TODO: Source code can have different indention than \t
    # Make it a config to anyfig?
    # Adds one indention
    src = src.replace('\n', '\n  ')
    return src

  setattr(func, '__anyfig_print_source__', __print_source__)
  return func