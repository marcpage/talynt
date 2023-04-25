#!/usr/bin/env python3

""" Tools to work with Indeed job descriptions
"""


import re

import talynt.html


class Description:
    def __init__(self):
        self.__in_description = False
        self.__description = ''

    def handle(self, entity:talynt.html.Entity):
        if entity.matches('div') and entity.contains('class', 'jobDescriptionText'):
            self.__in_description = True  # description start

        elif self.__in_description and not entity.matches('section', 'div'):
            self.__description += str(entity).strip()  # values in description

        elif self.__in_description and entity.matches('div') and entity.contains('id', 'belowFullJobDescription'):
            self.__in_description = False  # end of description

    def value(self) -> dict:
        return {'description': self.__description}

class Company(talynt.html.MetaData):
    def __init__(self):
        super().__init__('div', 'data-company-name', 'true', 'company')

    def value(self) -> dict:
        result = super().value()

        if 'company' in result:
            result['company'] = result['company'].replace(' - Jobs', '')

        return result

def parse(html:str) -> dict:
    return talynt.html.Scraper(
        Description(),
        Company(),
        talynt.html.MetaData('div', 'class', 'JobInfoHeader-title', 'title'),
        talynt.html.TagPattern('script', re.compile(r'"Job Type":\["(?P<type>[^"]+)"\]')),
        talynt.html.TagPattern('script', re.compile(r'"location":"(?P<location>[^"]+)"')),
    ).feed(html).properties()
