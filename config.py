import yaml

class Config():

    def __init__(self, config_file="./config.yaml"):
        """
        Initialize this config from a YAML file.

        :param config_file - Input YAML file.
        """

        with open(config_file, 'r') as stream:
            self.config = yaml.safe_load(stream)
