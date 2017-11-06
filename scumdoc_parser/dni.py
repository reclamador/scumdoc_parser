from scumdoc_parser import BaseScumDocParser

class DNIScumParser(BaseScumDocParser):
    KEYWORDS = {'nombre': False,  'sexo nacionalidad': False, "domicilio": False, "hijo/a de": False,
                'fecha de nacimiento': False, 'lugar de nacimiento': False, "idesp": False,
                # new keywords
                "espana o documento nacional de identidad": False,
                "apellidos": False, "num soport validez": False, 'dni': False,
                # old keywords
                'documento nacional de identidad': False,
                "primer apellido": False, "segundo apellido": False, "valido hasta": False, "dni num": False,
                 "provincia/pais":  False,  "lugar de domicilio": False,
                "equipo": False, }

    OCR = ['id(?P<country>[a-z]{3})[a-z]{3}[0-9]{7}(?P<dni>[0-9]{8}[a-z])<+',
           '(?P<date_birth>[0-9]{6})[0-9](?P<sex>m|f)(?P<date_expires>[0-9]{6})[0-9](?P<nat>[a-z]{3})<+[0-9]',
           '(?P<surnames>([a-z0]+<)+)<(?P<names>[a-z0]+)<*']




