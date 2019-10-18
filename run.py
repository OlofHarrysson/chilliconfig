# from user_config import OlofConfig
from chilliconfig import config_class, MasterConfig, setup_config
import chilliconfig
import time
from dataclasses import dataclass
from typing import Callable, Iterator, Union, Optional, List
import imgaug as ia
import imgaug.augmenters as iaa
import inspect
import pickle
import numpy as np


class Transformer():
  def __init__(self):
    self.seq = iaa.Resize({"height": 64, "width": 64})

  def __call__(self, im):
    augmented_im = self.seq.augment_image(np.array(im))
    return Image.fromarray(augmented_im)

  def __repr__(self):
    # return repr(self.seq)
    return str(self.seq)


@config_class
class MainConfig(MasterConfig):
  def __init__(self, name):
    super().__init__(name)
    print("MAIN CONFIG SUPER")
    self.start_time = time.time()
    self.img_size = 100
    self.classes = ['car', 'dog']
    self.freeze_config = False


# @dataclass
class MyClass():
  # bajs = 100
  # korv: int = bajs * 2
  def __init__(self):
    self.bsize = 100


def transforms():
  return iaa.Sequential([
    iaa.Crop(px=(0, 16)),
    iaa.Fliplr(
      0.5
    ),  # JUST COMMEENT TO MAKE THIS LINE REALLY LONG GOT DAMNIT WOWOOWOWOWOWOWOWOWOWOOWWOOWOWWOWOWOWOOWOWOW
    iaa.GaussianBlur(sigma=(0, 3.0))
  ])


@config_class
class Train(MainConfig):
  def __init__(self, name):
    super().__init__(name)
    self.classes = ['dog']
    # self.class_obj = MyClass()
    # self.transforms = Transformer()
    self.func_transforms = transforms()
    # self.func_transforms = inspect.getsource(transforms)
    # print(self.func_transforms)
    # print(type(self.func_transforms))
    # qwe


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
  # print(config)
  test_config(config)
  pth = 'config.cfg'
  config.save(pth)
  config2 = chilliconfig.load_config(pth)
  print(config2)
  test_config(config2)
  # print("\n\n")
  # print(repr(config))
  # config.name = 'New name'
  # print(config)


if __name__ == '__main__':
  print("BEFORE MAIN")
  main()
