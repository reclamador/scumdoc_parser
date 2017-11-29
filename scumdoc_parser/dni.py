from datetime import datetime
from scumdoc_parser import BaseScumDocParser, FuzzySearch, RegexSearch


class DNIScumParser(BaseScumDocParser):
    KEYWORDS = ['nombre', 'sexo nacionalidad', "domicilio", "hijo/a de",
                'fecha de nacimiento', 'lugar de nacimiento', "idesp",
                # new keywords
                "espana o documento nacional de identidad",
                "apellidos", "num soport validez", 'dni',
                # old keywords
                'documento nacional de identidad',
                "primer apellido", "segundo apellido", "valido hasta", "dni num",
                "provincia/pais",  "lugar de domicilio",
                "equipo"]

    OCR = {'mr_1': 'id(?P<country>[a-z]{3})[a-z]{3}[0-9]{7}(?P<dni>[0-9]{8}[a-z])<+',
           'mr_2': '(?P<date_birth>[0-9]{6})[0-9](?P<sex>m|f)(?P<date_expires>[0-9]{6})[0-9](?P<nat>[a-z]{3})<+[0-9]',
           'mr_3': '(?P<surnames>([a-z0]+<)+)<(?P<names>[a-z0]+)<*'}

    def post_process_keyword(self, content):
        if content:
            return content
        return None

    def post_process_date(self, content):
        if content:
            return datetime.strptime('%s-%s-%s' % content.groups(), '%d-%m-%Y').date().isoformat()
        return content

    def pre_process_ocr(self, content):
        return content.replace(' ', '')

    def post_process_ocr(self, content):
        if content:
            return content.groupdict()
        return content

    def __init__(self, text):
        searches = []
        searches.append(RegexSearch('dates', regex='(\d{2})\s(\d{2})\s(\d{4})', post_process=self.post_process_date,
                        multiple=True))
        for keyword in self.KEYWORDS:
            searches.append(FuzzySearch(keyword, keyword, 0.7, group='keywords',
                                        post_process=FuzzySearch.process_only_true))
        for key, value in self.OCR.items():
            searches.append(RegexSearch(key, regex=value, group="ocr", pre_process=self.pre_process_ocr,
                                        post_process=self.post_process_ocr))
        super(DNIScumParser, self).__init__(text, searches)
