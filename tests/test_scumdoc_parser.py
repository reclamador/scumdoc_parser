#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `scumdoc_parser` package."""
from __future__ import unicode_literals
import mock
from datetime import datetime, date
import unittest
from datetime import date

from scumdoc_parser.dni import DNIScumParser
from scumdoc_parser import FuzzySearch, RegexSearch, BaseScumDocParser

DNI_OLD = u'DOCUMENTO NACIONALDE IDENTIDAD.\nESPANA\nPARIER APELD0\nSANCHOZ DE LA BL ANC A\nSEGUNDO APELD\nA PUENT ES\nTo NOORE\nMARIA DEL Sagrario\nSaxo NACIONALIDAD\nFESP\nFECHA DE NAMENTO\nO910 1978\nDESP\nA JX199161\nVADO HASTA\non the\n19 09 2021\nSPM\nDNI NUM .\n56933095F\nLEID\nLUGAR DE NACMIENTO\nMAD RI D\nPROVINCIA/PAIS\nMADRID\nHJOIA DE\nJUAN 1 ANTONIA\nDOMICILIO\nC. R10 T A J 0 1 0 P01 B\nLUGAR DE DOMICILIO\nAL COR CON\nSELLER\nPROVINCIAIPAIS\nEQUIPO\nMADRID , SONNNNNNSSSSSSSS 28031L6D 1\nIDES PA JX1991 61956933095 F<<<<<<\n7810098F2109195ESP<<<<<<<<<<<5\nSANCHOZ<DE<LA<BLANCAKPUENTE<<M\n'

DNI_OLD_NO_BACK = u'DOCUMENTO NACIONALDE IDENTIDAD.\nESPANA\nPARIER APELD0\nSANCHOZ DE LA BL ANC A\nSEGUNDO APELD\nA PUENT ES\nTo NOORE\nMARIA DEL Sagrario\nSaxo NACIONALIDAD\nFESP\nFECHA DE NAMENTO\nO910 1978\nDESP\nA JX199161\nVADO HASTA\non the\n19 09 2021\nSPM\nDNI NUM .\n56933095F\nLEID\n'

DNI_OLD_ONLY_BACK = U'LUGAR DE NACMIENTO\nMAD RI D\nPROVINCIA/PAIS\nMADRID\nHJOIA DE\nJUAN 1 ANTONIA\nDOMICILIO\nC. R10 T A J 0 1 0 P01 B\nLUGAR DE DOMICILIO\nAL COR CON\nSELLER\nPROVINCIAIPAIS\nEQUIPO\nMADRID , SONNNNNNSSSSSSSS 28031L6D 1\nIDES PA JX1991 61956933095 F<<<<<<\n7810098F2109195ESP<<<<<<<<<<<5\nSANCHOZ<DE<LA<BLANCAKPUENTE<<M\n'
DNI_OLD_CAT = u'DOCUMENTO NACIONAL DE IDENTIDAD\nPRIMER APELLIDOI PRIVER COGNOM\nOME NAC COGNOMMW\nNOLDRENOM.\nESPANA TESTAston coach I\nGENARO LUIS ON\nSex SEXE NACIONALIDAD INACIONALITA\nM ESP\nMA\nFECHA DE 0 LACMENTODATA for NAUXEMENT I\nAP N15 4605\nVALDO HASTAVATB Fins\n23 01 2025\nPGG\nDNI NUM.\n52522003R DININNILDINGS\nLUGAR DE NACMIENTOILLoc DE NANXEMENT\nVILANOVA I LA GEL TRU\nPROVINCINPAs I ProvinCIA PAs\nBARCELON A\nHNJOIA DEI FILUA DE\nJOSE LUIS I SANTIAGA\nDOMICILIO DOMICILI\nRBLA:EXPOS ICIO 85 P01 2\nDOMICILIOLLOC DE DOMICIL\nVILANOVA I LA GELTR\nBARCELONAR\nELONASSSSSSSSSSSSSSSSSS 08901L6D1\nIDES PAPN 154605152522003 R<<<<<\n7301 164 M2401232 ESP<<<<<<<<<<<3\nOMENA C<IGLESIAS<GENAR 0<LUIS <\n'
DNI_OLD_NO_BACK_CAT = u'DOCUMENTO NACIONAL DE IDENTIDAD\nPRIMER APELLIDOI PRIVER COGNOM\nOME NAC COGNOMMW\nNOLDRENOM.\nESPANA TESTAston coach I\nGENARO LUIS ON\nSex SEXE NACIONALIDAD INACIONALITA\nM ESP\nMA\nFECHA DE 0 LACMENTODATA for NAUXEMENT I\nAP N15 4605\nVALDO HASTAVATB Fins\n23 01 2025\nPGG\nDNI NUM.\n52522003R DININNILDINGS\n'

DNI_NEW = u'ESPANA O DocuMENTO NACIONAL DE IDENTIDAD\nthe\nAn OAS\nAPELDOs\nALVAREZ\nDORADO\nNOMBAE\nRAMON\nSEXO\nNACONALDAD\nESP\nFECHA DE NACORIENTO\n17 11 1983\n12046\nNUN SOPORT VALDEZ\nBBH110745 12 04 2026\na\n571200\nTV\nDN 04900073D\nc. COMANDANTE FRANCO 1 P01\nMORA ,\nTOLEDO\nas to the\n8\nH\nH TOLEDO\nH TOLEDO ,\nLa\nOADE\nFRANCISCO 1N FRANCIS MI\nID ES P BBH 11 0745 0490 0073D <<<<<<\n8311178 M2604 125E SP<<<<<<<<<<<7\nALVAREZ<DOR AD0<<RAMON<<<<<<<<\n'

DNI_NEW_NO_BACK = u'ESPANA O DocuMENTO NACIONAL DE IDENTIDAD\nthe\nAn OAS\nAPELDOs\nALVAREZ\nDORADO\nNOMBAE\nRAMON\nSEXO\nNACONALDAD\nESP\nFECHA DE NACORIENTO\n17 11 1983\n12046\nNUN SOPORT VALDEZ\nBBH110745 12 04 2026\na\n571200\nTV\nDN 04900073D\n'

DNI_NEW_NO_BACK_ERROR_DATES = u'ESPANA O DocuMENTO NACIONAL DE IDENTIDAD\nthe\nAn OAS\nAPELDOs\nALVAREZ\nDORADO\nNOMBAE\nRAMON\nSEXO\nNACONALDAD\nESP\nFECHA DE NACORIENTO\n37 11 1983\n12046\nNUN SOPORT VALDEZ\nBBH110745 12 13 2026\na\n571200\nTV\nDN 04900073D\n'


DNI_ONLY_BACK = u'c. COMANDANTE FRANCO 1 P01\nMORA ,\nTOLEDO\nas to the\n8\nH\nH TOLEDO\nH TOLEDO ,\nLa\nOADE\nFRANCISCO 1N FRANCIS MI\nID ES P BBH 11 0745 0490 0073D <<<<<<\n8311178 M2604 125E SP<<<<<<<<<<<7\nALVAREZ<DOR AD0<<RAMON<<<<<<<<\n'

DNI_OLD_FIRST_BACK = u'SEOUVEVAUEVASONVAEBECEIPEIVIBABE\nESPANA\nLUGAR DE NACIMIENTO LLC DE NAIXEMENT\nBARCELONA\nPROVINCIAPAIs PROviNCIA-PAis\nBARCELONA\nHIOIA DEI FILLIA DE\nS AND ALI 0 1 ANTONIA\nDOMICILIO IDOMICII\nC. PADILL A 289 P05 1\nLUCAR DE DOMICILIO LLoC DE DOMICIL\nBARCELONA\nPRISER APELLDO PRIMER coGHOR\nMARTINEZ\nSEGUN90 APELL00 sEGON coGMOs\nGAGO\nNOABRE NON\nPEPA ESTHER\nSEXO / SEXENACIONALIDAD INACIONALITAT\nESP\nFECHA DE NACIMENTO DATA DE MAIXEMENT\n19 06 1969\nPROVINCIAPA is I PROVINCIA-PAis\nEQUIPOIEQUIP\nnews.\n0805516D1\nent\nAP 112552\nVALDO HASTA/VALID FINS\n10 06 2021\nID ESPA J P1125 5265368604 1 W<<<<<<\n6906197 F21 06102ESP<<<<<<<<<<<4\nMARTINEZ <GAG0<<PEPA <ESTHER <<\nrun on DC\n53686041 W\nDNI N\xfaM.\n'

DNI_NOT_VALID = U'OJETE CALOR'

DNI_NO_DATES = u'LUGAR DE NACIMIENTO\nSANTOÑA\nPROVINCIA/PAIS\nCANTABRIA\nRUOIA DE\nLORENZO / BEGOÑA\nDOMICILIO\nBARO. ORIÑON 65 002 0006\nLUGAR DE DOMICILIO\nORI NON\nCASTRO - URDIALES\nPROVINCIA/PAIS\nCANTABRIANS\nEQUIPO\n39676 A6DV\nIDESPADL1941614 25748789R&&\n6302197F1911105 ESP<<<<<<<\nSANZ <PEREZ<<BEGONA <<'

DNI_NO_KEYWORDS = u'DOMICILIO / DOMICILI\nCRER. SANT ANTONI MARIA CLARET 48 P05 0001\nESPLUGUES DE LLOBREGAT\nBARCELONA\nEQUIPO / EQUIP\n08055D6D1\nLUGAR DE NACIMIENTO / LLOC DE NAIXEMENT//\nBARCELONA\nBARCELONA\nHIJOIA DE / FILLUA DE\nROBERTO I AI\nIDES PBDP14712 0016925657P<<<<<<\n8905086M2204042 ESP<<<<<<<<<<<7\nMARTINEZ<PEREZ<<MANUEL<<<<<<<\n'

DNI_OLD_ALL = u'\x0cDOCUMENTO NACIONAL DE IDENTIDAD\nNAMNEMOTOMODELACROMIOON OTOMOTION\nESPA\xd1A\nPRIMER APELLIDO I PRIMER COGNOM\nABAD\nSEGUNDO APELLIDO / SEGON COGNOM\nSANZ\nNOMBRE I NOM\nCLARA\nSEXO / SEXE NACIONALIDAD / NACIONALITAT\nF ESP\nFECHA DE NACIMIENTO / DATA DE NAIXEMENT\n12 10 1980\nIDESP\nAJL180334\nV\xc1LIDO HASTA / VALID FINS\n17 06 2021\n! :: Rii::\nBia\n170611\nAaro\nDNI N\xdaM.\n63423963V\n\x0ci\nPasies LUGAR DE NACIMIENTO / LLOC DE NAIXEMENT\nVILANOVA I LA GELTR\xda\n| PROVINCIA/PAIS / PROVINCIA -PAIS\nBARCELONA\nHIJOJA DE FILLIA DE\nJOSE / ANA JOSE\nDOMICILIO / DOMICILI\nCRER. SOGUES 8 002 0001\nLUGAR DE DOMICILIO / LLOC DE DOMICILI\nVILANOVA I LA GELTR\xda\nPROVINCIA/PAIS (PROVINCIA PARANN\nBARCELONA\nEquipo / EQUIP\n08901L6D1\nIDES PAJL180334363423963V<<<<<<\n8010122F2106179 ESP<<<<<<<<<<<3\nABAD<SANZ<<CLARA<<<<<<<<<<<\n'

DNI_OLD_COMPLETE_SURNAMES = u'\x0cthe onweersingkirkeolvier\nentstarctium III II TIITLIT T\xedTILDTUIC TITICE DIN\nHIGHER EVERHAVERBER\nJ = DOCUMENTO NACIONAL DE IDENTIDAD\nPRIMER APELLIDO\nCORTES\nSEGUNDO APELIDO\nSANZ\nNOMBRE\nJOSE CARLOS\nSEXO NACIONALIDAD\nESP\nFECHA DE NACIMIENTO\n29 03 1984\nIDESP\nAPP147129.\nV\xc1LIDO HASTA\n11 02 2019\nMINISTRO\nownini DNI N\xdaM.\n59969177S\n\x0cLUGAR DE NACIMIENTO\nC\xc1DIZ\nPROVINCIA/PAIS\nC\xc1DIZ\nHJOIA DE\nPEPE / SAGRARIO\nDOMICILIO\nCMNO. CAMINO DEL\nLLOBREGAT ( 15 B\nLUGAR DE DOMICILIO\nCHICLANA DE LA FRONTERA\nPROVINCIA/PAIS\nEQUIPO\n11691L6D1\nsett er en private\nme\nviewizerritoris\nIDES PAPP147129859969177s<<<<<<\n8403294M1902112 ESP<<<<<<<<<<<7\nCORTES<SAN Z<<JOSE<ALBERTO<<<<\n'


class TestDNIScumdocParser(unittest.TestCase):
    """Tests for `scumdoc_parser` package."""

    keywords = {'nombre': True,  'sexo nacionalidad': True, "domicilio": True, "domicilio / domicili": True, "hijo/a de": True,
                'fecha de nacimiento': True, 'lugar de nacimiento': True, "lugar de nacimiento/ lloc de naixement": True,
                # new keywords
                "espana o documento nacional de identidad": True,
                "apellidos": True, "num soport validez": True, 'dni': True,
                # old keywords
                'documento nacional de identidad': True, "idesp": True,
                "primer apellido": True, "segundo apellido": True, "valido hasta": True, "dni num": True,
                "provincia/pais":  True,  "lugar de domicilio": True,
                "equipo": True, "equipo / equip": True}

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
            for key_mr, value_mr in result['ocr'].items():
                for key, value in result['ocr'][key_mr].items():
                    self.assertEqual(ocrs[key], value, '%s not %s' % (key, value))

    def assertAnalysis(self, result_expected, analysis):
        self.assertEqual(len(result_expected), len(analysis), analysis)
        for result in result_expected:
            self.assertIn(result, analysis)

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
                'surnames': 'sanchoz de la blancakpuente', 'names': 'm'}
        parser = DNIScumParser(DNI_OLD)
        result = parser.parse()
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
        ocrs = {'date_expires': u'260412', 'surnames': u'alvarez dorado', 'date_birth': u'831117',
                     'names': u'ramon', 'nat': u'esp', 'country': u'esp', 'dni': u'04900073d', 'sex': u'm'}
        parser = DNIScumParser(DNI_NEW)
        result = parser.parse()
        self.assertResult(result, [date(year=1983, month=11, day=17),
                                   date(year=2026, month=4, day=12)], keywords, ocrs)

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
        self.assertResult(result, [date(year=1983, month=11, day=17),
                                   date(year=2026, month=4, day=12)], keywords, ocrs)

    def test_dni_new_no_back_no_correct_dates(self):
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
        parser = DNIScumParser(DNI_NEW_NO_BACK_ERROR_DATES)
        result = parser.parse()
        self.assertResult(result, [], keywords, ocrs)

    def test_dni_old_first_back_in_same_level(self):
        keywords = dict(self.keywords)
        keywords = {key:False for key, value in self.keywords.items()}
        keywords["idesp"] = True
        keywords['dni num'] = True
        keywords['domicilio / domicili'] = True
        keywords['lugar de nacimiento/ lloc de naixement'] = True
        keywords['equipo / equip'] = True
        parser = DNIScumParser(DNI_OLD_FIRST_BACK)
        result = parser.parse()
        ocrs = {'date_expires': u'210610', 'surnames': u'martinez gago', 'date_birth': u'690619',
                'names': u'pepa esther', 'nat': u'esp', 'country': u'esp', 'dni': u'53686041w', 'sex': u'f'}
        self.assertResult(result, [date(year=1969, month=6, day=19),
                                   date(year=2021, month=6, day=10)], keywords, ocrs)

    def test_dni_search_found(self):
        parser = DNIScumParser(DNI_OLD)
        result = parser.search(['maria del sagrario'])
        self.assertResult(result, [], {'maria del sagrario': True}, {})

    def test_dni_search_not_found(self):
        parser = DNIScumParser(DNI_OLD)
        result = parser.search(['ojete'])
        self.assertResult(result, [], {'ojete': False}, {})

    def test_fuzzy_search(self):
        result = {}
        fuzzy_search = FuzzySearch('name', '1234567890', 0.7)
        fuzzy_search.search('12345678aa', result)
        self.assertTrue(result['name'])
        result = {}
        fuzzy_search.search('123456aaaa', result)
        self.assertFalse(result['name'])

    def test_regex_search(self):
        result = {}
        regex_search = RegexSearch('dates', '(\d{2})\s(\d{2})\s(\d{4})')
        regex_search.search('abcd', result)
        self.assertFalse('dates' in result)
        result = {}
        regex_search.search('10 11 1984', result)
        self.assertIsNotNone(result['dates'])

    def test_regex_search_pre_process(self):
        result = {}
        def pre_process(content):
            return content.replace(',', ' ')
        regex_search = RegexSearch('name', '(\d{2})\s(\d{2})\s(\d{4})', pre_process=pre_process)
        regex_search.search('10,11,1984', result)
        self.assertIsNotNone(result['name'])

    def test_regex_search_post_process(self):
        result = {}
        def post_process(content):
            return datetime.strptime('%s-%s-%s' % content.groups(), '%d-%m-%Y').date()
        regex_search = RegexSearch('name', '(\d{2})\s(\d{2})\s(\d{4})', post_process=post_process)
        regex_search.search('10 11 1984', result)
        self.assertEqual(datetime(year=1984, month=11, day=10).date(), result['name'])


    def test_number_mr(self):
        parser = DNIScumParser(DNI_OLD)
        self.assertEqual(parser.number, '56933095f')

    def test_number_no_mr(self):
        parser = DNIScumParser(DNI_OLD_NO_BACK)
        self.assertEqual(parser.number, None)

    def test_expired_date_mr(self):
        parser = DNIScumParser(DNI_OLD)
        self.assertEqual(parser.expired_date, datetime(year=2021, month=9, day=19).date())

    def test_expired_date_no_mr(self):
        parser = DNIScumParser(DNI_OLD_NO_BACK)
        self.assertEqual(parser.expired_date, None)

    def test_name_mr(self):
        parser = DNIScumParser(DNI_NEW)
        self.assertEqual(parser.name, 'ramon')

    def test_name_no_mr(self):
        parser = DNIScumParser(DNI_OLD_NO_BACK)
        self.assertEqual(parser.name, None)

    def test_surnames_mr(self):
        parser = DNIScumParser(DNI_NEW)
        self.assertEqual(parser.surnames, 'alvarez dorado')

    def test_surnames_no_mr(self):
        parser = DNIScumParser(DNI_OLD_NO_BACK)
        self.assertEqual(parser.surnames, None)

    def test_not_is_invalid(self):
         def _test_not_is_invalid(dni_to_test):
             parser = DNIScumParser(dni_to_test)
             self.assertFalse(parser.is_invalid())
         for dni_to_test in [DNI_OLD, DNI_OLD_NO_BACK, DNI_OLD_FIRST_BACK, DNI_NEW_NO_BACK,
                             DNI_NEW, DNI_OLD_CAT, DNI_OLD_NO_BACK_CAT]:
             _test_not_is_invalid(dni_to_test)

    def test_is_invalid(self):
         parser = DNIScumParser(DNI_NOT_VALID)
         self.assertTrue(parser.is_invalid())

    def test_not_is_expired_with_back_mr(self):
         parser = DNIScumParser(DNI_NEW)
         reference_date = datetime(year=2017, month=12, day=1).date()
         self.assertFalse(parser.is_expired(reference_date))

    def test_is_expired_with_back_mr(self):
         parser = DNIScumParser(DNI_NEW)
         reference_date = datetime(year=2030, month=12, day=1).date()
         self.assertTrue(parser.is_expired(reference_date))

    def test_not_is_expired_with_no_back(self):
         parser = DNIScumParser(DNI_NEW_NO_BACK)
         reference_date = datetime(year=2017, month=12, day=1).date()
         self.assertFalse(parser.is_expired(reference_date))

    def test_is_expired_with_no_back(self):
         parser = DNIScumParser(DNI_NEW_NO_BACK)
         reference_date = datetime(year=2030, month=12, day=1).date()
         self.assertTrue(parser.is_expired(reference_date))

    def test_is_front(self):
         parser = DNIScumParser(DNI_NEW_NO_BACK)
         self.assertTrue(parser.is_front())

    def test_not_is_front(self):
         parser = DNIScumParser(DNI_ONLY_BACK)
         self.assertFalse(parser.is_front())

    def test_is_back(self):
         parser = DNIScumParser(DNI_NEW)
         self.assertTrue(parser.is_back())

    def test_not_is_back(self):
         parser = DNIScumParser(DNI_NEW_NO_BACK)
         self.assertFalse(parser.is_back())

    def test_check_id_complete_dni(self):
         parser = DNIScumParser(DNI_OLD)
         self.assertTrue(parser.check_id('56933095f'))

    def test_check_id_only_front(self):
         parser = DNIScumParser(DNI_OLD_NO_BACK)
         self.assertTrue(parser.check_id('56933095f'))

    def test_check_id_only_back(self):
         parser = DNIScumParser(DNI_OLD_ONLY_BACK)
         self.assertTrue(parser.check_id('56933095f'))

    def test_check_id_complete_dni_not_found(self):
         parser = DNIScumParser(DNI_OLD)
         self.assertFalse(parser.check_id('77 933095f'))

    def test_check_id_only_front_not_found(self):
         parser = DNIScumParser(DNI_OLD_NO_BACK)
         self.assertFalse(parser.check_id('89933095f'))

    def test_check_id_only_back_not_found(self):
         parser = DNIScumParser(DNI_OLD_ONLY_BACK)
         self.assertFalse(parser.check_id('89933095f'))

    def test_check_person_found(self):
         parser = DNIScumParser(DNI_NEW)
         self.assertTrue(parser.check_person({'name': 'ramon', 'surnames': 'alvarez dorado'}))

    def test_check_person_not_found(self):
         parser = DNIScumParser(DNI_NEW)
         self.assertFalse(parser.check_person({'name': 'jose', 'surnames': 'martinez dorado'}))

    def test_analysis_new_dni_valid(self):
         parser = DNIScumParser(DNI_NEW)
         reference_date = datetime(year=2017, month=11, day=1).date()
         self.assertAnalysis([parser.VALID], parser.analysis(person={'name': 'ramon', 'surnames': 'alvarez dorado',
                                                                     'id':'04900073d'},
                                                             reference_date=reference_date))

    def test_analysis_new_dni_valid_with_only_number(self):
         parser = DNIScumParser(DNI_NEW)
         reference_date = datetime(year=2017, month=11, day=1).date()
         self.assertAnalysis([parser.VALID], parser.analysis(person={'name': 'ramon', 'surnames': 'alvarez dorado'},
                                                             reference_date=reference_date))

    def test_analysis_new_dni_not_client(self):
         parser = DNIScumParser(DNI_NEW)
         reference_date = datetime(year=2017, month=11, day=1).date()
         self.assertAnalysis([parser.FRONT, parser.BACK, parser.NOT_VALID_PERSON],
                             parser.analysis(person={'name': 'luis', 'surnames': 'alvarez dorado', 'id': '14900073d'},
                                             reference_date=reference_date))

    def test_analysis_old_dni_valid_no_id(self):
         parser = DNIScumParser(DNI_OLD)
         reference_date = datetime(year=2017, month=11, day=1).date()
         self.assertAnalysis([parser.VALID],
                             parser.analysis(person={'name': 'maria del sagrario',
                                                     'surnames': 'sanchez de la blanca puente'},
                                             reference_date=reference_date))

    def test_analysis_old_dni_valid_id_none(self):
        parser = DNIScumParser(DNI_OLD_ALL)
        reference_date = datetime(year=2017, month=11, day=1).date()
        self.assertAnalysis([parser.VALID],
                            parser.analysis(person={'name': 'Clara',
                                                    'surnames': 'Abad', 'id': None},
                                            reference_date=reference_date))

    def test_analysis_old_dni_valid_id_surnames(self):
        parser = DNIScumParser(DNI_OLD_COMPLETE_SURNAMES)
        reference_date = datetime(year=2017, month=11, day=1).date()
        self.assertAnalysis([parser.VALID],
                            parser.analysis(person={'name': 'Jose alberto',
                                                    'surnames': 'Cort\xe9s sanz', 'id': None},
                                            reference_date=reference_date))


    def test_analysis_old_dni_valid(self):
         parser = DNIScumParser(DNI_OLD)
         reference_date = datetime(year=2017, month=11, day=1).date()
         self.assertAnalysis([parser.VALID],
                             parser.analysis(person={'name': 'maria del sagrario',
                                                     'surnames': 'sanchez de la blanca puente', 'id': '56933095f'},
                                             reference_date=reference_date))

    def test_analysis_dni_expired(self):
         parser = DNIScumParser(DNI_OLD)
         reference_date = datetime(year=2030, month=11, day=1).date()
         self.assertAnalysis([parser.EXPIRED, parser.FRONT, parser.BACK],
                             parser.analysis(person={'name': 'maria del sagrario',
                                                     'surnames': 'sanchez de la blanca puente', 'id': '56933095f'},
                                             reference_date=reference_date))

    def test_analysis_not_valid(self):
         parser = DNIScumParser(DNI_NOT_VALID)
         self.assertAnalysis([parser.NOT_VALID], parser.analysis())

    def test_analysis_dates_not_found(self):
        parser = DNIScumParser(DNI_NO_DATES)
        self.assertAnalysis([parser.BACK], parser.analysis(person={'name': 'begoña',
                                                    'surnames': 'sanz perez', 'id': '25748789r'}))

    def test_analysis_keywords_not_found(self):
        parser = DNIScumParser(DNI_NO_KEYWORDS)
        self.assertAnalysis([parser.BACK], parser.analysis(person={'name': 'manuel',
                                                            'surnames': 'martinez perez', 'id': '16925657p'}))

