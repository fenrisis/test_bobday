from configparser import ConfigParser


def get_config(filename='config.ini'):
    config = ConfigParser()
    config.read(filename)
    return config


BASE_URL = "https://python.test.bobdaytech.ru"
