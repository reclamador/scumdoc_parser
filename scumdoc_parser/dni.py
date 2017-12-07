from datetime import datetime
import unicodedata
from scumdoc_parser import BaseScumDocParser, FuzzySearch, RegexSearch


class DNIScumParser(BaseScumDocParser):

    VALID = u'Valid DNI'
    NOT_VALID = u'Not valid DNI'
    EXPIRED = u'Expired'
    NOT_VALID_PERSON = u'Person not found'
    FRONT = u'Front side'
    BACK = u'Back side'

    KEYWORDS = ['nombre', 'sexo nacionalidad', "domicilio", "domicilio / domicili", "hijo/a de",
                'fecha de nacimiento', 'lugar de nacimiento', "lugar de nacimiento/ lloc de naixement", "idesp",
                # new keywords
                "espana o documento nacional de identidad",
                "apellidos", "num soport validez", 'dni',
                # old keywords
                'documento nacional de identidad',
                "primer apellido", "segundo apellido", "valido hasta", "dni num",
                "provincia/pais",  "lugar de domicilio",
                "equipo", "equipo / equip"]

    OCR = {'mr_1': 'id(?P<country>[a-z]{3})[a-z]{3}[0-9]{7}(?P<dni>[0-9]{8}[a-z])<+',
           'mr_2': '(?P<date_birth>[0-9]{6})[0-9](?P<sex>m|f)(?P<date_expires>[0-9]{6})[0-9](?P<nat>[a-z]{3})<+[0-9]',
           'mr_3': '(?P<surnames>([a-z0]+<)+)<(?P<names>([a-z0]+<*)+)'}

    def post_process_date(self, content):
        if content:
            return datetime.strptime('%s-%s-%s' % content.groups(), '%d-%m-%Y').date()
        return content

    def pre_process_ocr(self, content):
        return content.replace(' ', '').replace('&', '<')

    def post_process_ocr(self, content):
        if content:
            content_dict = {}
            for key, value in content.groupdict().items():
                if key in ['name', 'surnames']:
                    content_dict[key] = value.replace('<', ' ').replace('0', 'o').strip()
                else:
                    content_dict[key] = value.replace('<', ' ').strip()
            return content_dict
        return content

    def __init__(self, text, keywords_ratio=0.7, client_ratio=0.7, id_ratio=0.8):
        self.keywords_ratio = 0.7
        self.client_ratio = 0.7
        self.id_ratio = 0.8
        searches = []
        searches.append(RegexSearch('dates', regex='(\d{2})\s(\d{2})\s(\d{4})', post_process=self.post_process_date,
                        multiple=True))
        for keyword in self.KEYWORDS:
            searches.append(FuzzySearch(keyword, keyword, self.keywords_ratio, group='keywords',
                                        post_process=FuzzySearch.process_only_true))
        for key, value in self.OCR.items():
            searches.append(RegexSearch(key, regex=value, group="ocr", pre_process=self.pre_process_ocr,
                                        post_process=self.post_process_ocr))
        super(DNIScumParser, self).__init__(text, searches)

    def _attribute(self, keys):
        if self._parsed:
            try:
                d = self._parsed
                for key in keys:
                    d = d[key]
                return d
            except KeyError:
                return None
        return None

    @property
    def number(self):
        return self._attribute(['ocr', 'mr_1', 'dni'])

    @property
    def expired_date(self):
        try:
            return datetime.strptime(self._attribute(['ocr', 'mr_2', 'date_expires']), '%y%m%d').date()
        except TypeError:
            return None

    @property
    def name(self):
        return self._attribute(['ocr', 'mr_3', 'names'])

    @property
    def surnames(self):
        try:
            return self._attribute((['ocr', 'mr_3', 'surnames']))
        except AttributeError:
            return None

    def is_invalid(self):
        """
        Document is considered invalid if no keywords is found
        :return:
        """
        if not self._parsed or 'keywords' not in self._parsed:
            return True
        for key, value in self._parsed['keywords'].items():
            if value:
                return False
        return True

    def is_expired(self, reference_date):
        """
        Only can be considered as expired when:
            - date_expired field in machine readable field is previous to reference date
            - two dates found and both previous to reference date
        :param reference_date:
        :return:
        """
        if self.expired_date and self.expired_date < reference_date:
            return True

        if 'dates' in self._parsed and len(self._parsed['dates']) == 2:
            for date in self._parsed['dates']:
                if date > reference_date:
                    return False
            return True
        return False

    def is_front(self):
        """
        Is considered as front if it has the name of the document
        :return:
        """
        try:
            return self._parsed['keywords']['documento nacional de identidad'] or \
                   self._parsed['keywords']["espana o documento nacional de identidad"]
        except KeyError:
            return False

    def is_back(self):
        """
        Is considered as back if it has machine readable data
        :return:
        """
        try:
            return 'mr_1' in self._parsed['ocr'] or 'mr_2' in self._parsed['ocr'] or 'mr_3' in self._parsed['ocr']
        except KeyError:
            return False

    def check_id(self, id):
        """
        Check if id is found in the document.
        It is allowed to differ by one digit, 0.8
        :param id:
        :return:
        """
        if self.number == id.lower():
            return True
        for key, value in self.search([id.lower()], self.id_ratio)['keywords'].items():
            if value:
                return True
        return False

    def check_person(self, person):
        """
        Check if person is found in the document
        :param person: {'name', 'surnames', 'id}
        :return:
        """
        found = True
        if 'id' in person and person['id']:
            return self.check_id(person['id'])
        if self.name == person['name'] and self.surnames == person['surnames']:
            return True if 'id' not in person or not person['id'] else self.check_id(person['id'])
        for key, value in self.search([person['name'],
                                       person['surnames']], self.client_ratio)['keywords'].items():
            if not value:
                found = False
                break
        if not found:
            return False
        return True if 'id' not in person or not person['id'] else self.check_id(person['id'])

    def analysis(self, person=None, reference_date=None):
        """
        Analyze dni
        :param person: dictionary {'name', 'surnames', 'id'}
        :param reference_date:
        :return:
        """
        if person:
            for key, value in person.items():
                person[key] = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').lower() if value else value
        results = []
        if self.is_invalid():
            return [self.NOT_VALID]
        reference_date = datetime.now().date() if not reference_date else reference_date
        if (self.is_front() or self.is_back()) and self.is_expired(reference_date):
            results.append(self.EXPIRED)
        if person and not self.check_person(person):
            results.append(self.NOT_VALID_PERSON)
        if not results and self.is_front() and self.is_back():
            results.append(self.VALID)
        else:
            if self.is_front():
                results.append(self.FRONT)
            if self.is_back():
                results.append(self.BACK)
        return results
