from user_config import OlofConfig, user_muli
from chilliconfig import config_class, MasterConfig, setup_config, print_source
import chilliconfig
import time
from dataclasses import dataclass
from typing import Callable, Iterator, Union, Optional, List
import imgaug as ia
import imgaug.augmenters as iaa
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
    self.noise1 = Noise(3, 0)
    self.flip = Flip(4, 0)
    self.noise2 = Noise(4, 0)
    self.primitive = 12
    self.prim2 = 1


# @config_class
# class MainConfig(MasterConfig):
#   def __init__(self, name):
#     super().__init__(name)
#     print("MAIN CONFIG SUPER")
#     self.start_time = time.time()
#     self.img_size = 100
#     self.classes = ['car', 'dog']
#     self.freeze_config = False


# @print_source
# @config_class(print_source=True)
@config_class
class Train(MasterConfig):
  def __init__(self, name):
    super().__init__(name)
    self.classes = ['dog']
    self.mydict = {
      '0': '2',
      '1': '2',
      '2': '2',
      '3': '2',
      '4': '2',
      '4asdasd': '2',
      '4qweqweqwe': '2',
      'qweqweqwesd4': '2',
      '4asdasdd': '2',
      '4ertert': '2',
    }
    self.transforms111 = Transformer(100)
    self.img_size = 10
    self.save = 123


def test_config(cfg):
  transforms = cfg.func_transforms
  images = np.array([ia.quokka(size=(64, 64)) for _ in range(32)],
                    dtype=np.uint8)
  print(type(transforms))
  print(transforms)
  images_aug = transforms(images=images)
  print(images_aug.shape)


def main():
  # config = setup_config()
  config = setup_config(default_config='Train')
  print(config)
  # test_config(config)
  # pth = 'config.cfg'
  # config.save(pth)
  # config2 = chilliconfig.load_config(pth)
  # print(config2)
  # test_config(config2)
  # print("\n\n")
  # print(repr(config))
  # config.name = 'New name'
  # print(config)


if __name__ == '__main__':
  print("BEFORE MAIN")
  main()
