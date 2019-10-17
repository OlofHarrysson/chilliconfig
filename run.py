from chilliconfig import config_class, MasterConfig, setup_config, config_class_old
from dataclasses import dataclass, replace
# from dataclass_copy import dataclass

# from user_config import Olof
# import user_config

# class B:
#     print("B INIT")
#     name: str

#     # def __init__(self, x):
#     #     self.x = x

# @dataclass()
# class C(B):
#     name: str
#     print("C INIT")
#     omg: str = 'sosososooso'
#     omg1: str = 'sosososooso'
#     omg2: str = 'sosososooso'

# print("C")
# c = C('C NAME')
# print(c)
# c.korven = 'asdasdasd'
# print(c)
# qwe
# c1 = replace(c, x=3)
# print(c1)

# @config_class
# def oolof():
#     print("OLI")

# @config_class_old
# class Bajs(MasterConfig):
#     def __init__(self, config_str):
#         super().__init__(config_str)
#         print("Bajs")

# print("BEFORE COOKIE DATACLASS")

# @dataclass()
# class Cookie(MasterConfig):
#     def __init__(self, config_str):
#         super().__init__(config_str)
#         print("COOOKIEEEE")

# print("AFTER COOKIE DATACLASS")


# @config_class(frozen=True)
@config_class_old
class Cookie(MasterConfig):
  # name: str
  # print("COOOKIEEEE")
  # omg: str = 'sosososooso'

  # def __setattr__(self, name, value):
  #     print(name)

  # def hej()

  def __init__(self, name):
    super().__init__(name)
    print("COOOKIEEEE")


# @config_class
# class MasterConfig(chilliconfig.MasterConfig):
#     def __init__(self, config_str):
#         super().__init__(config_str)
#         print("MASTAAA")


def main():
  # c = Cookie('Cookie')
  # print(c)
  # print(type(c))
  # qwe
  config = setup_config(default_config='Cookie')
  # print(dir(config))
  print(vars(config))
  # print(config.__setattr__)
  # config.hej = 123
  # config.hej = 123
  # print(type(config))
  # print(config.frozen)
  config.bajsen = 'koooorven'
  print(config)
  # print(config.name)
  # Cookie('olof')
  print("END OF MAIN")


if __name__ == '__main__':
  print("BEFORE MAIN")
  main()
