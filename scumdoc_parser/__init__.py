# -*- coding: utf-8 -*-
import re
from difflib import SequenceMatcher
import logging


class BaseSearch(object):

    def __init__(self, name, pre_process=None, post_process=None, group=None, multiple=False):
        """
        Abstract Search
        :param name: name of the search, used to organize returned result
        :param pre_process: function for processing the text before performing search
        :param post_process: function for processing the text after performing the search
        :param group: name of the group of searches. Usefull to organize results
        :param multiple: search might apply several times
        """
        self.name = name
        self.pre_process = pre_process if pre_process else self.dummy_process
        self.post_process = post_process if post_process else self.dummy_process
        self.group = group
        self.multiple = multiple

    @classmethod
    def dummy_process(cls, content):
        return content

    @classmethod
    def process_only_true(cls, content):
        if content:
            return content
        return None

    @classmethod
    def process_regex_only_true(cls, content):
        if content:
            return True
        return None

    def _search(self, line):
        """
        Implement this method for performing the real search
        :param line:
        :return:
        """
        raise NotImplementedError

    def _create_key_result(self, key, result, group=False):
        if key not in result:
            result[key] = [] if not group and self.multiple else {}

    def search(self, line, result):
        try:
            content = self.post_process(self._search(self.pre_process(line)))
        except Exception:
            logging.exception("Exception searching '%s' in line '%s'" % (self.name, line))
            content = None
        if content is not None:
            if self.group:
                self._create_key_result(self.group, result, True)
                self._create_key_result(self.name, result[self.group])
                if self.multiple:
                    result[self.group][self.name].append(content)
                else:
                    result[self.group][self.name] = content
            else:
                self._create_key_result(self.name, result)
                if self.multiple:
                    result[self.name].append(content)
                else:
                    result[self.name] = content


class RegexSearch(BaseSearch):

    def __init__(self, name, regex, pre_process=None, post_process=None, group=None, multiple=None):
        """
        Search using a regular expression
        :param name:
        :param regex:
        :param pre_process:
        :param post_process:
        :param group:
        :param multiple:
        """
        super(RegexSearch, self).__init__(name, pre_process, post_process, group, multiple)
        self.regex = regex

    def _search(self, line):
        return re.search(self.regex, line)


class FuzzySearch(BaseSearch):

    def __init__(self, name, keyword, ratio, pre_process=None, post_process=None, group=None):
        """
        Search ussing fuzzy search using a ratio to set as valid
        :param name:
        :param keyword:
        :param ratio:
        :param pre_process:
        :param post_process:
        :param group:
        """
        super(FuzzySearch, self).__init__(name, pre_process, post_process, group)
        self.ratio = ratio
        self.keyword = keyword

    def _search(self, line):
        return SequenceMatcher(a=self.keyword, b=line).ratio() >= self.ratio


class BaseScumDocParser(object):

    def __init__(self, raw_text, searches):
        """
        Base class to handle extraction of not human documents. Ids, passports, recipies, boardingpass
        :param raw_text:
        :param searches:
        """
        self.text = self._normalize(raw_text)
        self.searches = searches
        self._parsed = self.parse()

    def _normalize(self, raw_text):
        return [line.strip().lower() for line in raw_text.splitlines() if line.strip()]

    def parse(self):
        """
        Parse the text performing all searches and returning the results
        :return: dictionary of results
        """
        result = {}
        for line in self.text:
            for search in self.searches:
                search.search(line, result)
        return result

    def search(self, keywords, ratio=0.7, regex=False):
        """
        Search some keywords
        :param keywords:
        :param ratio:
        :param regex:
        :return:
        """
        result = {'keywords': {keyword: False for keyword in keywords}}
        searches = []
        for keyword in keywords:
            if regex:
                searches.append(RegexSearch(keyword, regex=keyword, group="keywords",
                                            post_process=RegexSearch.process_regex_only_true))
            else:
                searches.append(FuzzySearch(keyword, keyword, ratio, group='keywords',
                                            post_process=FuzzySearch.process_only_true))
        for line in self.text:
            for search in searches:
                search.search(line, result)
        return result
