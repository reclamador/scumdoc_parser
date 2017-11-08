# -*- coding: utf-8 -*-
import re
from datetime import datetime
from difflib import get_close_matches, SequenceMatcher

"""Top-level package for ScumDoc Parser."""

__author__ = """Juan Madurga"""
__email__ = 'jlmadurga@gmail.com'
__version__ = '0.1.0'



class BaseSearch(object):

    def __init__(self, name, pre_process=None, post_process=None, group=None):
        self.name = name
        self.pre_process = pre_process
        self.post_process = post_process
        self.group = group

    def _search(self, line):
        raise NotImplementedError

    def search(self, line):
        return self.post_process(self._search(self.pre_process(line)))


class RegexSearch(BaseSearch):

    def __init__(self, name, regex, pre_process=None, post_process=None, group=None):
        super(RegexSearch, self).__init__(name, regex, pre_process, post_process, group)
        self.regex = regex

    def _search(self, line):
        return re.search(self.regex, line)

class FuzzySearch(BaseSearch):

    def __init__(self, name, keyword, ratio, pre_process=None, group=None):
        super(FuzzySearch, self).__init__(name, pre_process, self._post_process, group)
        self.ratio = ratio
        self.keyword = keyword

    def _post_process(self, search):
        return search

    def _search(self, line):
        return SequenceMatcher(a=self.keyword, b=line).ratio() >= self.ratio


class BaseScumDocParser(object):
    """
    Base class to handle extraction of not human documents. Ids, passports, recipies, boardingpass
    """
    KEYWORDS = {}
    OCR = []

    def __init__(self, raw_text):
        self.text = self._normalize(raw_text)
        self._keywords = dict(self.KEYWORDS)
        self._ocrs = self.OCR

    def _normalize(self, raw_text):
        return [line.strip().lower() for line in raw_text.splitlines() if line.strip()]

    def _fuzzy_search(self, keyword, accuracy=0.7):
        found = get_close_matches(keyword, self.text, 1, accuracy)
        if found:
            return found[0]
        return None


    def _search_dates(self, line, dates_results):
        found = re.search('(\d{2})\s(\d{2})\s(\d{4})', line)
        if found:
            dates_results.append(datetime.strptime('%s-%s-%s' % found.groups(), '%d-%m-%Y').date())

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

    def _extract_ocr(self, line, ocr_results):
        line_normalized = line.replace(' ','')
        for ocr in self._ocrs:
            match = re.match(ocr, line_normalized)
            if match:
                ocr_results.update(match.groupdict())

    def _extract_keywords(self, line, results):
        for keyword in self._keywords:
            if SequenceMatcher(a=keyword, b=line).ratio() >= 0.7:
                results[keyword] = True

    def parse(self):
        """
        Parse doc text
        :return:
        """
        keyword_results = dict((keyword, False) for keyword in self._keywords)
        dates_results = []
        ocr_results = {}
        for line in self.text:
            self._search_dates(line, dates_results)
            self._extract_ocr(line, ocr_results)
            self._extract_keywords(line, keyword_results)
        return {'keywords': keyword_results, 'dates': dates_results, 'ocr': ocr_results}

    def search(self, keywords):
        result = dict((keyword, False) for keyword in keywords)
        self._keywords = self._search_keywords(keywords, result)
        return {'keywords': result}

