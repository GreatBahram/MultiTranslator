#!/usr/bin/env python3
import json
import os
from abc import ABCMeta, abstractmethod

import requests

from bs4 import BeautifulSoup

__all__ = [
    'Cambridge',
    'FastDic',
    'MultiTranslator',
]


class Translator(metaclass=ABCMeta):
    """ Base Translator class """ 
    def __init__(self, src=None, dst=None, headers={}):
        self.name = ""
        self.url = ""
        self.src = src
        self.dst = dst
        self.headers = headers

    def tranlsate(self, word):
        self.text = text
        self._get_data()
        self._parse_data()

    @abstractmethod
    def _get_data(self, word):
        URL = self.URL
        new_url = URL + self.word
        response = requests.get(new_url, headers = self.headers)
        if response.status_code == requests.codes.ok:
            return response.text
        pass

    @abstractmethod
    def _parse_data(self):
        pass

    def to_dict(self, filename, link):
        pass


class Cambridge(Translator):
    """Download the meaning of WORD from http://dictionary.cambridge.org/dictionary/english/ """
    def __init__(self):
        super().__init__(self, word)
        self.name = "cambridge"
        self.url = "http://dictionary.cambridge.org/dictionary/english/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0",
        }
        self.results = {
                'Pronunciation': '', 'Definition': 'Not Found',
                'Part of speech': 'Not Found',
                }

    def parse_data(self, word):
        response = self._get_data(word)
        if response:
            soup = BeautifulSoup(response, 'lxml')

            part_of_speech = soup.find_all('span', {'class': 'pos'})[0].getText()
            if part_of_speech == 'idiom':
                # idiom means cambridge can't translate this word
                return {}

            elif part_of_speech == 'noun':
                countable = soup.find_all('span', {'class': 'gcs'})
                #part_of_speech = ""
                if countable:
                    part_of_speech += ' [%s]' % (countable[0].getText())

            uk_phonetic = soup.find_all('span', {'class': 'pron'})[0].getText()  # extract pronunciation
            us_phonetic = soup.find_all('span', {'class': 'pron'})[1].getText()  # extract pronunciation
            voices = soup.select('span[data-src-mp3]')  # get voice of us and uk accent

            if voices:
                #uk_audio = voices[0].attrs['data-src-mp3']
                us_audio = voices[1].attrs['data-src-mp3']
                #uk_voice =  self._save_binaries(uk_audio)
                us_voice =  self._save_binaries(word + '.mp3', us_audio)
                #self.results['uk-voice'] = uk_voice
            definition = soup.find_all('b', {'class': 'def'})[0].getText()\
                .replace('  ', ' ').title()
            self.results['Part of speech'] = part_of_speech
            self.results['Pronunciation'] = us_phonetic
            self.results['Definition'] = definition.replace(':', '')
            return self.results
        return {}
    

class FastDic(Translator):
    """Download the meaning of WORD from http://fastdic.com/word"""
    def __init__(self, word):
        super().__init__(self, word)
        self.name = "FastDic"
        self.url = "https://fastdic.com/word/"

    def parse_data(self, word):
        response = self._get_data(word)
        if response:
            soup = BeautifulSoup(response, 'lxml')
            meaning = soup.find_all('ul', {'class': ['result', 'js-result']})
            if meaning:
                meaning = BeautifulSoup(str(meaning), 'lxml')
                for span in meaning.find_all('span'):
                    span.extract()
                meaning = meaning.select('li')[0].getText()
                meaning = str(meaning).strip().split('\n')
                mean = str(meaning[0]).split('،')
                return {'Persian_Mean': mean}
        return {}


class MultiTranslator:
    def __init__(self, word):
        self.dictionaries = [
            Cambridge,
            FastDic,
        ]

    def search(self, word):
        word = word.lower()
        data_from_db = db_api.load_form_db(word)
        if data_from_db:
            results = json.loads(data_from_db[2])
        else:
            results = {}
            for dictionary in self.dictionaries:
                results = self._translate(dictionary, word, results) 
            db_api.save_to_db(word, json.dumps(results))
        return results

    def _translate(self, dictionary, word, results):
        results[my_dict.name] = my_dict.parse_data(word)
        return results
