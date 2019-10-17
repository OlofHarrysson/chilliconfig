from chilliconfig import config_class, MasterConfig, setup_config


@config_class
class Olof(MasterConfig):
    def __init__(self, config_str):
        super().__init__(config_str)
        print("WOOOLOLOLOLOF")
