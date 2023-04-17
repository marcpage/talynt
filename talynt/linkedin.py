#!/usr/bin/env python3

""" Tools to work with LinkedIn job descriptions
"""


import html.parser
import re


class Entity:
    def __init__(self, name:str=None, attrs:list=None, data:str=None, end=False):
        self.__name = name
        self.data = data
        self.end = end
        self.__attrs = attrs if attrs else []

    def __str__(self) -> str:
        if self.end:
            return f"</{self.__name}>"

        if self.data is not None:
            return self.data

        return f"<{self.__name}" + ''.join(f' {a[0]}="{a[1]}"' for a in self.__attrs) + ">"

    def matches(self, *keys) -> bool:
        if self.__name is None:
            return False

        return self.__name.lower() in [k.lower() for k in keys]

    def contains(self, key:str, check:str) -> bool:
        value = self.get(key)
        return False if value is None else check.lower() in value.lower()

    def get(self, key:str, default:str=None) -> str:
        found = [a[1] for a in self.__attrs if a[0].lower() == key.lower()]
        return found[0] if found else default

    def __getitem__(self, key:str) -> str:
        return self.get(key)

    def __len__(self):
        return len(self.__attrs)

    def has_key(self, key):
        return key.lower() in self.keys()

    def keys(self):
        return [a[0].lower() for a in self.__attrs]

    def values(self):
        return [a[1] for a in self.__attrs]


class Description:
    CLASS_DESCRIPTION = 'description__text'

    def __init__(self):
        self.__in_description = False
        self.__description = ''

    def handle(self, entity:Entity):
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

    def handle(self, entity:Entity):
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


class Scraper(html.parser.HTMLParser):

    def __init__(self):
        self.__scanners = (Criteria(), Description())
        super().__init__()

    def __scan(self, entity:Entity):
        for scanner in self.__scanners:
            scanner.handle(entity)

    def handle_starttag(self, tag:str, attrs:list):
        self.__scan(Entity(name=tag, attrs=attrs))

    def handle_endtag(self, tag:str):
        self.__scan(Entity(name=tag, end=True))

    def handle_data(self, data:str):
        self.__scan(Entity(data=data))

    def feed(self, contents:str):
        super().feed(contents)
        return self

    def properties(self) -> dict:
        return {k:v for s in self.__scanners for k,v in s.value().items()}
