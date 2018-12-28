from abc import ABCMeta, abstractmethod

import requests


class Translator(metaclass=ABCMeta):
    """ Base Translator class """ 
    def __init__(self, params={}, headers={}):
        self.name = ""
        self.base_url = ""
        self.params = params
        self.headers = headers
        self.result = {}

    def tranlsate(self, text):
        self.text = text
        self.initialize_url()
        self.get_data()
        self.parse_data()

    def initialize_url(self):
        self.new_url = self.base_url + self.text

    def get_data(self):
        data = None
        response = requests.get(self.new_url, headers = self.headers)
        if response.status_code == requests.codes.ok:
            data = response.text
        self.data = data

    @abstractmethod
    def parse_data(self):
        pass

    def to_dict(self):
        pass
