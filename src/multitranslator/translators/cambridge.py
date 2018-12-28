from bs4 import BeautifulSoup

from .translator import Translator


class Cambridge(Translator):
    """Download the meaning of WORD from http://dictionary.cambridge.org/dictionary/english/ """

    def __init__(self):
        super().__init__(self)
        self.name = "cambridge"
        self.dict_url = "http://dictionary.cambridge.org/dictionary/english/"

    def parse_data(self):
        if self.data is None:
            return {}
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
            uk_audio = voices[0].attrs['data-src-mp3']
            us_audio = voices[1].attrs['data-src-mp3']
            self.results['uk-voice'] = uk_audio
            self.results['us-voice'] = us_audio
        definition = soup.find_all('b', {'class': 'def'})[0].getText()\
            .replace('  ', ' ').title()
        self.results['Part of speech'] = part_of_speech
        self.results['Pronunciation'] = us_phonetic
        self.results['Definition'] = definition.replace(':', '')
        return self.results
