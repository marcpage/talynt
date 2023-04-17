#!/usr/bin/env python3

""" Tools to help scan HTML
"""


import html.parser


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


class MetaData:
    def __init__(self, tag:str, attr:str, contents:str, name:str):
        self.__tag = tag
        self.__name = name
        self.__attr = attr
        self.__contents = contents
        self.__in_tag = False
        self.__value = None

    def handle(self, entity:Entity):
        if entity.matches(self.__tag) and entity.contains(self.__attr, self.__contents):
            self.__in_tag = True
        elif entity.end and entity.matches(self.__tag):
            self.__in_tag = False
        elif entity.data is not None and self.__in_tag:
            self.__value = entity.data.strip()
            self.__in_tag = False

    def value(self) -> dict:
        return {} if self.__value is None else {self.__name: self.__value}


class Scraper(html.parser.HTMLParser):

    def __init__(self, *scanners):
        self.__scanners = scanners
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
