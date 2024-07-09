import configparser
import os


class Config:

    environment = 'local'
    project_name = os.path.basename(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    def __init__(self, environment=None):

        self.config_parser = configparser.RawConfigParser()

        if environment:
            self.environment = environment

    def get(self, section_name, attribute_name):

        try:

            self.config_parser.read('%s/config/%s.env' % (self.project_name, self.environment))

            return self.config_parser[section_name][attribute_name]

        except Exception as e:

            raise e
