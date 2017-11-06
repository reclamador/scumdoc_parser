#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `scumdoc_parser` package."""


import unittest
from datetime import date

from scumdoc_parser.dni import DNIScumParser

DNI_OLD = u'DOCUMENTO NACIONALDE IDENTIDAD.\nESPANA\nPARIER APELD0\nSANCHOZ DE LA BL ANC A\nSEGUNDO APELD\nA PUENT ES\nTo NOORE\nMARIA DEL Sagrario\nSaxo NACIONALIDAD\nFESP\nFECHA DE NAMENTO\nO910 1978\nDESP\nA JX199161\nVADO HASTA\non the\n19 09 2021\nSPM\nDNI NUM .\n56933095F\nLEID\nLUGAR DE NACMIENTO\nMAD RI D\nPROVINCIA/PAIS\nMADRID\nHJOIA DE\nJUAN 1 ANTONIA\nDOMICILIO\nC. R10 T A J 0 1 0 P01 B\nLUGAR DE DOMICILIO\nAL COR CON\nSELLER\nPROVINCIAIPAIS\nEQUIPO\nMADRID , SONNNNNNSSSSSSSS 28031L6D 1\nIDES PA JX1991 61956933095 F<<<<<<\n7810098F2109195ESP<<<<<<<<<<<5\nSANCHOZ<DE<LA<BLANCAKPUENTE<<M\n'

DNI_OLD_NO_BACK = u'DOCUMENTO NACIONALDE IDENTIDAD.\nESPANA\nPARIER APELD0\nSANCHOZ DE LA BL ANC A\nSEGUNDO APELD\nA PUENT ES\nTo NOORE\nMARIA DEL Sagrario\nSaxo NACIONALIDAD\nFESP\nFECHA DE NAMENTO\nO910 1978\nDESP\nA JX199161\nVADO HASTA\non the\n19 09 2021\nSPM\nDNI NUM .\n56933095F\nLEID\n'

DNI_OLD_CAT = u'DOCUMENTO NACIONAL DE IDENTIDAD\nPRIMER APELLIDOI PRIVER COGNOM\nOME NAC COGNOMMW\nNOLDRENOM.\nESPANA TESTAston coach I\nGENARO LUIS ON\nSex SEXE NACIONALIDAD INACIONALITA\nM ESP\nMA\nFECHA DE 0 LACMENTODATA for NAUXEMENT I\nAP N15 4605\nVALDO HASTAVATB Fins\n23 01 2025\nPGG\nDNI NUM.\n52522003R DININNILDINGS\nLUGAR DE NACMIENTOILLoc DE NANXEMENT\nVILANOVA I LA GEL TRU\nPROVINCINPAs I ProvinCIA PAs\nBARCELON A\nHNJOIA DEI FILUA DE\nJOSE LUIS I SANTIAGA\nDOMICILIO DOMICILI\nRBLA:EXPOS ICIO 85 P01 2\nDOMICILIOLLOC DE DOMICIL\nVILANOVA I LA GELTR\nBARCELONAR\nELONASSSSSSSSSSSSSSSSSS 08901L6D1\nIDES PAPN 154605152522003 R<<<<<\n7301 164 M2401232 ESP<<<<<<<<<<<3\nOMENA C<IGLESIAS<GENAR 0<LUIS <\n'
DNI_OLD_NO_BACK_CAT = u'DOCUMENTO NACIONAL DE IDENTIDAD\nPRIMER APELLIDOI PRIVER COGNOM\nOME NAC COGNOMMW\nNOLDRENOM.\nESPANA TESTAston coach I\nGENARO LUIS ON\nSex SEXE NACIONALIDAD INACIONALITA\nM ESP\nMA\nFECHA DE 0 LACMENTODATA for NAUXEMENT I\nAP N15 4605\nVALDO HASTAVATB Fins\n23 01 2025\nPGG\nDNI NUM.\n52522003R DININNILDINGS\n'

DNI_NEW = u'ESPANA O DocuMENTO NACIONAL DE IDENTIDAD\nthe\nAn OAS\nAPELDOs\nALVAREZ\nDORADO\nNOMBAE\nRAMON\nSEXO\nNACONALDAD\nESP\nFECHA DE NACORIENTO\n17 11 1983\n12046\nNUN SOPORT VALDEZ\nBBH110745 12 04 2026\na\n571200\nTV\nDN 04900073D\nc. COMANDANTE FRANCO 1 P01\nMORA ,\nTOLEDO\nas to the\n8\nH\nH TOLEDO\nH TOLEDO ,\nLa\nOADE\nFRANCISCO 1N FRANCIS MI\nID ES P BBH 11 0745 0490 0073D <<<<<<\n8311178 M2604 125E SP<<<<<<<<<<<7\nALVAREZ<DOR AD0<<RAMON<<<<<<<<\n'

DNI_NEW_NO_BACK = u'ESPANA O DocuMENTO NACIONAL DE IDENTIDAD\nthe\nAn OAS\nAPELDOs\nALVAREZ\nDORADO\nNOMBAE\nRAMON\nSEXO\nNACONALDAD\nESP\nFECHA DE NACORIENTO\n17 11 1983\n12046\nNUN SOPORT VALDEZ\nBBH110745 12 04 2026\na\n571200\nTV\nDN 04900073D\n'


DNI_OLD_FIRST_BACK = u'SEOUVEVAUEVASONVAEBECEIPEIVIBABE\nESPANA\nLUGAR DE NACIMIENTO LLC DE NAIXEMENT\nBARCELONA\nPROVINCIAPAIs PROviNCIA-PAis\nBARCELONA\nHIOIA DEI FILLIA DE\nS AND ALI 0 1 ANTONIA\nDOMICILIO IDOMICII\nC. PADILL A 289 P05 1\nLUCAR DE DOMICILIO LLoC DE DOMICIL\nBARCELONA\nPRISER APELLDO PRIMER coGHOR\nMARTINEZ\nSEGUN90 APELL00 sEGON coGMOs\nGAGO\nNOABRE NON\nPEPA ESTHER\nSEXO / SEXENACIONALIDAD INACIONALITAT\nESP\nFECHA DE NACIMENTO DATA DE MAIXEMENT\n19 06 1969\nPROVINCIAPA is I PROVINCIA-PAis\nEQUIPOIEQUIP\nnews.\n0805516D1\nent\nAP 112552\nVALDO HASTA/VALID FINS\n10 06 2021\nID ESPA J P1125 5265368604 1 W<<<<<<\n6906197 F21 06102ESP<<<<<<<<<<<4\nMARTINEZ <GAG0<<PEPA <ESTHER <<\nrun on DC\n53686041 W\nDNI N\xfaM.\n'

class TestDNIScumdocParser(unittest.TestCase):
    """Tests for `scumdoc_parser` package."""

    keywords = {'nombre': True,  'sexo nacionalidad': True, "domicilio": True, "hijo/a de": True,
                'fecha de nacimiento': True, 'lugar de nacimiento': True,
                # new keywords
                "espana o documento nacional de identidad": True,
                "apellidos": True, "num soport validez": True, 'dni': True,
                # old keywords
                'documento nacional de identidad': True, "idesp": True,
                "primer apellido": True, "segundo apellido": True, "valido hasta": True, "dni num": True,
                "provincia/pais":  True,  "lugar de domicilio": True,
                "equipo": True}

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def assertResult(self, result, dates, keywords, ocrs):
        if 'dates' in result:
            for date in result['dates']:
                self.assertIn(date, dates)
        for key, value in result['keywords'].items():
            self.assertEqual(keywords[key], value, '%s not %s' % (key, value))
        if 'ocr' in result:
            for key, value in result['ocr'].items():
                self.assertEqual(ocrs[key], value, '%s not %s' % (key, value))

    def test_dni_old(self):
        keywords = dict(self.keywords)
        keywords['dni'] = False
        keywords['nombre'] = False
        keywords['apellidos'] = False
        keywords['num soport validez'] = False
        ocrs = {'date_expires': '210919',
                'date_birth': '781009',
                'nat': 'esp',
                'country': 'esp',
                'dni': '56933095f',
                'sex': 'f',
                'surnames': 'sanchoz<de<la<blancakpuente<', 'names': 'm'}
        parser = DNIScumParser(DNI_OLD)
        result = parser.parse()
        print result
        self.assertResult(result, [date(year=2021, month=9, day=19)], keywords, ocrs)

    def test_dni_old_no_back(self):
        keywords = dict(self.keywords)
        keywords['equipo'] = False
        keywords['lugar de nacimiento'] = False
        keywords['lugar de domicilio'] = False
        keywords['dni'] = False
        keywords['provincia/pais'] = False
        keywords['nombre'] = False
        keywords['apellidos'] = False
        keywords['hijo/a de'] = False
        keywords['num soport validez'] = False
        keywords['domicilio'] = False
        ocrs = {}
        parser = DNIScumParser(DNI_OLD_NO_BACK)
        result = parser.parse()
        print result
        self.assertResult(result, [date(year=2021, month=9, day=19)], keywords, ocrs)


    def test_dni_old_cat(self):
        keywords = self.keywords.copy()
        keywords['segundo apellido'] = False
        keywords['equipo'] = False
        keywords['lugar de domicilio'] = False
        keywords['dni'] = False
        keywords['provincia/pais'] = False
        keywords["apellidos"] =  False
        keywords["num soport validez"] = False
        keywords["fecha de nacimiento"] = False
        keywords["sexo nacionalidad"] = False
        keywords["valido hasta"] = False
        keywords["domicilio"] = False
        keywords["idesp"] = False
        keywords["hijo/a de"] = False
        keywords["lugar de nacimiento"] = False
        keywords['nombre'] = False
        keywords['primer apellido'] = False
        ocrs = {'date_expires': u'240123', 'date_birth': u'730116', 'nat': u'esp', 'country': u'esp', 'dni': u'52522003r', 'sex': u'm'}
        parser = DNIScumParser(DNI_OLD_CAT)
        result = parser.parse()
        print result
        self.assertResult(result, [date(year=2025, month=1, day=23)], keywords, ocrs)

    def test_dni_old_no_back_cat(self):
        keywords = self.keywords.copy()
        keywords['segundo apellido'] = False
        keywords['equipo'] = False
        keywords['lugar de domicilio'] = False
        keywords['dni'] = False
        keywords['provincia/pais'] = False
        keywords["apellidos"] =  False
        keywords["num soport validez"] = False
        keywords["fecha de nacimiento"] = False
        keywords["sexo nacionalidad"] = False
        keywords["valido hasta"] = False
        keywords["domicilio"] = False
        keywords["idesp"] = False
        keywords["hijo/a de"] = False
        keywords["lugar de nacimiento"] = False
        keywords['nombre'] = False
        keywords['primer apellido'] = False
        ocrs = {}
        parser = DNIScumParser(DNI_OLD_NO_BACK_CAT)
        result = parser.parse()
        print result
        self.assertResult(result, [date(year=2025, month=1, day=23)], keywords, ocrs)

    def test_dni_new(self):
        keywords = dict(self.keywords)
        keywords['domicilio'] = False
        keywords['primer apellido'] = False
        keywords['segundo apellido'] = False
        keywords['dni num'] = False
        keywords['valido hasta'] = False
        keywords['lugar de domicilio'] = False
        keywords['hijo/a de'] = False
        keywords['equipo'] = False
        keywords['lugar de nacimiento'] = False
        keywords['lugar de domicilio'] = False
        keywords['dni'] = False
        keywords['provincia/pais'] = False
        ocrs = {'date_expires': u'260412', 'surnames': u'alvarez<dorad0<', 'date_birth': u'831117',
                     'names': u'ramon', 'nat': u'esp', 'country': u'esp', 'dni': u'04900073d', 'sex': u'm'}
        parser = DNIScumParser(DNI_NEW)
        result = parser.parse()
        print result
        self.assertResult(result, [date(year=1983, month=11, day=17), date(year=2026, month=4, day=12)], keywords, ocrs)

    def test_dni_new_no_back(self):
        keywords = dict(self.keywords)
        keywords['domicilio'] = False
        keywords['primer apellido'] = False
        keywords['segundo apellido'] = False
        keywords['dni num'] = False
        keywords['valido hasta'] = False
        keywords['lugar de domicilio'] = False
        keywords['hijo/a de'] = False
        keywords['equipo'] = False
        keywords['lugar de nacimiento'] = False
        keywords['lugar de domicilio'] = False
        keywords['dni'] = False
        keywords['provincia/pais'] = False
        ocrs = {}
        parser = DNIScumParser(DNI_NEW_NO_BACK)
        result = parser.parse()
        print result
        self.assertResult(result, [date(year=1983, month=11, day=17), date(year=2026, month=4, day=12)], keywords, ocrs)

    def test_dni_old_first_back_in_same_level(self):
        keywords = dict(self.keywords)
        keywords = {key:False for key, value in self.keywords.items()}
        keywords["idesp"] = True
        keywords['dni num'] = True
        parser = DNIScumParser(DNI_OLD_FIRST_BACK)
        result = parser.parse()
        ocrs = {'date_expires': u'210610', 'surnames': u'martinez<gag0<', 'date_birth': u'690619',
                'names': u'pepa', 'nat': u'esp', 'country': u'esp', 'dni': u'53686041w', 'sex': u'f'}
        self.assertResult(result, [date(year=1969, month=6, day=19), date(year=2021, month=6, day=10)], keywords, ocrs)

    def test_dni_search_found(self):
        parser = DNIScumParser(DNI_OLD)
        result = parser.search(['maria del sagrario'])
        print result
        self.assertResult(result, [], {'maria del sagrario': True}, {})

    def test_dni_search_not_found(self):
        parser = DNIScumParser(DNI_OLD)
        result = parser.search(['ojete'])
        print result
        self.assertResult(result, [], {'ojete': False}, {})
