#!/usr/bin/env python3

""" Tools to work with LinkedIn job descriptions
"""


import talynt.html


class Description:
    def __init__(self):
        self.__in_description = False
        self.__description = ''

    def handle(self, entity:talynt.html.Entity):
        if entity.matches('div') and entity.contains('class', 'description__text'):
            self.__in_description = True  # description start

        elif self.__in_description and not entity.matches('section', 'div'):
            self.__description += str(entity).strip()  # values in description

        elif self.__in_description and entity.end and entity.matches('div'):
            self.__in_description = False  # end of description

    def value(self) -> dict:
        return {'description': self.__description}


class Criteria:
    def __init__(self, mapping=None):
        self.__in_criteria_type = False
        self.__criteria_title = None
        self.__in_criteria_value = False
        self.__values = {}
        self.__mapping = mapping if mapping is not None else {}

    def handle(self, entity:talynt.html.Entity):
        if entity.matches('h3') and entity.contains('class', 'description__job-criteria-subheader'):
            self.__in_criteria_type = True

        elif entity.matches('span') and entity.contains('class', 'description__job-criteria-text'):
            self.__in_criteria_value = True

        if entity.data is not None:
            if self.__in_criteria_value:
                criteria_name = self.__mapping.get(self.__criteria_title, self.__criteria_title)
                self.__values[criteria_name] = entity.data.strip()
                self.__criteria_title = None
                self.__in_criteria_value = False

            elif self.__in_criteria_type:
                self.__criteria_title = entity.data.strip()
                self.__in_criteria_type = False

    def value(self) -> dict:
        return self.__values


def parse(html:str) -> dict:
    return talynt.html.Scraper(
        Description(),
        Criteria({'Employment type': 'type'}),
        talynt.html.MetaData('h3', 'class', 'sub-nav-cta__header', 'title'),
        talynt.html.MetaData('a', 'href', 'linkedin.com/company', 'company'),
        talynt.html.MetaData('span', 'class', 'sub-nav-cta__meta-text', 'location'),
    ).feed(html).properties()
