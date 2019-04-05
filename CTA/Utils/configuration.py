import configparser
import os

class config(object):

    def setup(self):
        self.conf = configparser.ConfigParser()
        script_path = os.path.join(os.path.realpath(__file__))
        ini_path = os.path.join("\\".join(script_path.split("\\")[0:-1]), 'config.ini')
        self.conf.read(ini_path)
        return self.conf
