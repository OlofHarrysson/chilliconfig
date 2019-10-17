import pconfig
from pconfig import mark
# from user_config import Olof
# import user_config


@mark
class Cookie(pconfig.MasterConfig):
  def __init__(self, config_str):
    super().__init__(config_str)
    print("COOOKIEEEE")


def main():
  config = pconfig.setup(default_config='Cookie')
  print(config)
  # Cookie('olof')
  print("END OF MAIN")


if __name__ == '__main__':
  print("BEFORE MAIN")
  main()