# -*- coding: utf-8 -*-
import re
from datetime import datetime
from difflib import get_close_matches

"""Top-level package for ScumDoc Parser."""

__author__ = """Juan Madurga"""
__email__ = 'jlmadurga@gmail.com'
__version__ = '0.1.0'


class BaseScumDocParser(object):
    """
    Base class to handle extraction of not human documents. Ids, passports, recipies, boardingpass
    """
    KEYWORDS = {}
    OCR = []

    def __init__(self, raw_text):
        self.text = self._normalize(raw_text)
        self._dates = []
        self._keywords = dict(self.KEYWORDS)
        self._ocrs = self.OCR
        self._ocr_results = {}

    def _normalize(self, raw_text):
        return [line.strip().lower() for line in raw_text.splitlines() if line.strip()]

    def _fuzzy_search(self, keyword, accuracy=0.7):
        found = get_close_matches(keyword, self.text, 1, accuracy)
        if found:
            return found[0]
        return None


    def _search_dates(self, line):
        found = re.search('(\d{2})\s(\d{2})\s(\d{4})', line)
        if found:
            self._dates.append(datetime.strptime('%s-%s-%s' % found.groups(), '%d-%m-%Y').date())

    def _search_keywords(self, keywords=None, result=None):
        if not keywords:
            keywords = self._keywords
        if not result:
            result = self._keywords
        for keyword in keywords:
            found = self._fuzzy_search(keyword)
            if found:
                result[keyword] = True
        return result

    def _extract_ocr(self, line):
        line_normalized = line.replace(' ','')
        for ocr in self._ocrs:
            match = re.match(ocr, line_normalized)
            if match:
                self._ocr_results.update(match.groupdict())
                break


    def _result(self):
        result = {}
        result.update({'keywords': self._keywords})
        result.update({'dates': self._dates})
        result.update({'ocr': self._ocr_results})
        return result

    def parse(self):
        """
        Parse doc text
        :return:
        """
        for line in self.text:
            self._search_dates(line)
            self._extract_ocr(line)
        self._keywords = self._search_keywords()
        return self._result()

    def search(self, keywords):
        result = dict((keyword, False) for keyword in keywords)
        self._keywords = self._search_keywords(keywords, result)
        return {'keywords': result}

