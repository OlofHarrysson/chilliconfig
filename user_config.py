from chilliconfig import config_class, MasterConfig


@config_class
class OlofConfig(MasterConfig):
  def __init__(self, config_str):
    super().__init__(config_str)
    print("WOOOLOLOLOLOF")


def user_muli(x, y):
  return x * y