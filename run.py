from user_config import OlofConfig, user_muli
from chilliconfig import config_class, MasterConfig, setup_config, SourceCode
import chilliconfig
import time
from dataclasses import dataclass
from typing import Callable, Iterator, Union, Optional, List
import imgaug as ia
import imgaug.augmenters as iaa
import inspect
import pickle
import numpy as np

# Source_code class. When printed, it returns the source code.
# Can I have a list of classes or something? I want to have chains
# List of classes in config?

# Transformer has all transform classes. Should be able to print them


class Noise(SourceCode):
  def __init__(self, x, y):
    super().__init__()
    self.x = x
    self.y = y

  def __call__(self):
    x = 1 + 3
    y = x + 5
    z = muli(x, y)
    return z

  # def __repr__(self):
  #   return f'Noise(x={self.x},y={self.y})'


# @source_code
class Transformer(SourceCode):
  def __init__(self):
    super().__init__()

    self.add_membs(Noise(1, 2))
    self.add_membs(Noise(3, 0))

  # Make this in parent? Call classes in order of appearance
  def __call__(self):
    self.noise()
    x = 1 + 3
    y = x + 5
    z = muli(x, y)
    return z

  # def __repr__(self):
  # return super(repr())

  # def __str__(self):
  # return super().__str__()
  # return "I AM TRANSFORMER"

  # return repr(self.seq)
  # return "I AM TRANSFORMER"

  # return str(self.seq)


# @config_class
# class MainConfig(MasterConfig):
#   def __init__(self, name):
#     super().__init__(name)
#     print("MAIN CONFIG SUPER")
#     self.start_time = time.time()
#     self.img_size = 100
#     self.classes = ['car', 'dog']
#     self.freeze_config = False


# @dataclass
class MyClass():
  # bajs = 100
  # korv: int = bajs * 2
  def __init__(self):
    self.bsize = 100


# @chilliconfig.config_func
# def transforms():
#   mm(1)
#   return iaa.Sequential([
#     iaa.Crop(px=(0, 16)),
#     iaa.Fliplr(
#       0.5
#     ),  # JUST COMMEENT TO MAKE THIS LINE REALLY LONG GOT DAMNIT WOWOOWOWOWOWOWOWOWOWOOWWOOWOWWOWOWOWOOWOWOW
#     iaa.GaussianBlur(sigma=(0, 3.0))
#   ])


# @chilliconfig.config_func
def mm(x):
  return x


@chilliconfig.config_func
def muli(x, y):
  mm(x)
  return x * y


@chilliconfig.config_func
class MyTrans():
  def __init__(self):
    pass

  # hook into call
  def __call__(self):
    x = y + 1
    return muli(1, 2)


@chilliconfig.config_func
def transforms():
  x = 1 + 3
  y = x + 5
  z = muli(x, y)
  return z


# Fall 1 - när man sparar kod så måste man se source code. Also print source


@config_class
class Train(MasterConfig):
  def __init__(self, name):
    super().__init__(name)
    self.classes = ['dog']
    self.img_size = 10
    # self.class_obj = MyClass()
    self.transforms111 = Transformer()
    # self.transforms111 = [Noise(3,4), FlipLR(12)]
    # self.transforms111 = [add_noise(5, 7), fliplr(12)]
    print("BEFORE TRANSFORM")

    # @chilliconfig.show_source
    # self.func_transforms = transforms()
    # self.func_transforms = transforms()
    print("AFTER TRANSFORM")
    # self.mulikorv = lambda: user_muli(1, 2)

    # self.milikorv = MyTrans()

    # self.f_trans = self.init_trans()

    # a = chilliconfig.RECORDED_FUNCTIONS
    # print(a)
    # self.func_transforms = inspect.getsource(transforms)
    # print(self.func_transforms)
    # print(type(self.func_transforms))
    # qwe

  @chilliconfig.config_func
  def init_trans(self):
    return transforms()


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
