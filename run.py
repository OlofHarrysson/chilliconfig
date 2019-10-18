from chilliconfig import config_class, MasterConfig, setup_config
# from user_config import OlofConfig
import time
from dataclasses import dataclass


@config_class
class MainConfig(MasterConfig):
    def __init__(self, name):
        super().__init__(name)
        self.start_time = time.time()
        self.img_size = 100
        self.classes = ['car', 'dog']
        self.freeze_config = False


@dataclass
@config_class
class Train(MainConfig):
    def __init__(self, name):
        super().__init__(name)
        self.img_size: int = 350

    img_size: int = 50
    #     self.img_size = 50


@config_class
class Inference(MainConfig):
    def __init__(self, name):
        super().__init__(name)
        self.classes = ['car']

        # self.complex_data_structure = read_file()


def main():
    # config = setup_config()
    config = setup_config(default_config='Train')
    print(config)
    # config.name = 'New name'
    # print(config)


if __name__ == '__main__':
    # print("BEFORE MAIN")
    main()
