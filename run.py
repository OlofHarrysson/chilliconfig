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


# @config_class(print_source=True)
# @print_source
@config_class
class Train(MasterConfig):
  def __init__(self):
    super().__init__()
    self.name = 'oldname'
    self.transforms111 = Transformer(100)
    # self.freeze_config = False


def test_config(cfg):
  transforms = cfg.transforms111
  print(transforms)
  qwe
  images = np.array([ia.quokka(size=(64, 64)) for _ in range(32)],
                    dtype=np.uint8)
  print(type(transforms))
  print(transforms)
  images_aug = transforms(images=images)
  print(images_aug.shape)


def main():
  # config = setup_config()
  config = setup_config(default_config='Train')
  # config2 = setup_config(default_config='MainConfig')
  # print(config)
  # print(dir(config).__setattr__)
  # chilliconfig.freeze(config)
  # print(config.__setattr__)
  config.frozen(True)
  config.frozen(False)
  config.name = '123123'
  # print(config2)
  # cc = Train()
  # chilliconfig.unfreeze(config)
  # print(dir(config))

  print(config)
  # print(config.name)

  qwe

  # test_config(config)
  # pth = 'config.cfg'
  # chilliconfig.save_config(config, pth)
  # config2 = chilliconfig.load_config(pth)
  # print(config2)
  # test_config(config2)
  # print("\n\n")
  # print(repr(config))
  # config2.name = 'New name'

  # config2.transforms111 = Transformer(100)
  # config2.transforms111 = 12123
  # print(config2)
  # config2.transforms111 = Transformer(300)
  # print(config2)


if __name__ == '__main__':
  print("BEFORE MAIN")
  main()
