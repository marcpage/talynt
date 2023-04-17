#!/usr/bin/env python3

""" Tools to work with LinkedIn job descriptions
"""


import talynt.html


class Description:
    CLASS_DESCRIPTION = 'description__text'

    def __init__(self):
        self.__in_description = False
        self.__description = ''

    def handle(self, entity:talynt.html.Entity):
        if entity.matches('div') and entity.contains('class', Description.CLASS_DESCRIPTION):
            self.__in_description = True  # description start

        elif self.__in_description and not entity.matches('section', 'div'):
            self.__description += str(entity)  # values in description

        elif self.__in_description and entity.end and entity.matches('div'):
            self.__in_description = False  # end of description

    def value(self) -> dict:
        return {'description': self.__description}


class Criteria:
    CLASS_TYPE = 'description__job-criteria-subheader'
    CLASS_VALUE = 'description__job-criteria-text'

    def __init__(self):
        self.__in_criteria_type = False
        self.__criteria_title = None
        self.__in_criteria_value = False
        self.__values = {}

    def handle(self, entity:talynt.html.Entity):
        if entity.matches('h3') and entity.contains('class', Criteria.CLASS_TYPE):
            self.__in_criteria_type = True

        elif entity.matches('span') and entity.contains('class', Criteria.CLASS_VALUE):
            self.__in_criteria_value = True

        if entity.data is not None:
            if self.__in_criteria_value:
                self.__values[self.__criteria_title] = entity.data.strip()
                self.__criteria_title = None
                self.__in_criteria_value = False

            elif self.__in_criteria_type:
                self.__criteria_title = entity.data.strip()
                self.__in_criteria_type = False

    def value(self) -> dict:
        return self.__values


class Title(talynt.html.MetaData):
    def __init__(self):
        super().__init__('h3', 'class', 'sub-nav-cta__header', 'title')


class Company(talynt.html.MetaData):
    def __init__(self):
        super().__init__('a', 'href', 'linkedin.com/company', 'company')


class Location(talynt.html.MetaData):
    def __init__(self):
        super().__init__('span', 'class', 'sub-nav-cta__meta-text', 'location')


def parse(html:str) -> dict:
    return talynt.html.Scraper(
        Description(),
        Criteria(),
        Title(),
        Company(),
        Location(),
    ).feed().properties()


import sys

with open(sys.argv[1], 'r') as html:
    print(parse(html.read()))
