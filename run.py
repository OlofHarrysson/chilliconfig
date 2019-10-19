from user_config import OlofConfig, user_muli
from chilliconfig import config_class, MasterConfig, setup_config, print_source
import chilliconfig
import time
from dataclasses import dataclass
from typing import Callable, Iterator, Union, Optional, List
# import imgaug as ia
# import imgaug.augmenters as iaa
import inspect
import pickle
import numpy as np


@print_source
class Noise():
  def __init__(self, x, y):
    self.x = x
    self.y = y


@print_source
class Flip():
  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.noise3 = Noise(1, 2)


@print_source
class Transformer():
  def __init__(self, x):
    # self.noise1 = Noise(x, x)
    # self.flip = Flip(4, 0)
    # self.noise2 = Noise(4, 0)
    self.primitive = x


# @config_class
# class MainConfig(MasterConfig):
#   def __init__(self):
#     print("MAIN CONFIG SUPER")
#     self.start_time = time.time()
#     self.img_size = 100
#     self.classes = ['car', 'dog']
#     self.freeze_config = False


@config_class
class Train(MasterConfig):
  def __init__(self):
    super().__init__()
    self.name = 'oldname'
    self.transforms111 = Transformer(100)
    # self.freeze_config = False
    # self.frozen = 123


def main():
  # config = setup_config()
  config = setup_config(default_config='Train')

  # config.frozen()
  # config.frozen(freeze=False)
  config.name = '123123'

  print(config)
  # print(config.name)


if __name__ == '__main__':
  print("BEFORE MAIN")
  main()
