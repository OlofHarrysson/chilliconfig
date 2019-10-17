import pconfig
from pconfig import mark


@mark
class Olof(pconfig.MasterConfig):
  def __init__(self, config_str):
    super().__init__(config_str)
    print("WOOOLOLOLOLOF")