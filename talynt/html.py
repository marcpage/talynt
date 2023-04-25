#!/usr/bin/env python3

""" Tools to help scan HTML
"""


import html.parser


class Entity:
    """an entity in html (tag, text, etc)"""

    def __init__(
        self, name: str = None, attrs: list = None, data: str = None, end=False
    ):
        self.__name = name
        self.data = data
        self.end = end
        self.__attrs = attrs if attrs else []

    def __str__(self) -> str:
        if self.end:
            return f"</{self.__name}>"

        if self.data is not None:
            return self.data

        return (
            f"<{self.__name}" + "".join(f' {a[0]}="{a[1]}"' for a in self.__attrs) + ">"
        )

    def matches(self, *keys) -> bool:
        """Check to see the tag name matches one of the given tag types"""

        if self.__name is None:
            return False

        return self.__name.lower() in [k.lower() for k in keys]

    def contains(self, key: str, check: str) -> bool:
        """Check a tag attribute to see it contains a given check string"""

        value = self.get(key)
        return False if value is None else check.lower() in value.lower()

    def get(self, key: str, default: str = None) -> str:
        """Get the contents of a tag attribute"""
        found = [a[1] for a in self.__attrs if a[0].lower() == key.lower()]
        return found[0] if found else default

    def __getitem__(self, key: str) -> str:
        return self.get(key)

    def __len__(self):
        return len(self.__attrs)

    def has_key(self, key):
        """determine if the tag has a given attribute"""
        return key.lower() in self.keys()

    def keys(self):
        """Get the attributes of the tag"""
        return [a[0].lower() for a in self.__attrs]

    def values(self):
        """Get the values of the attributes of the tag"""
        return [a[1] for a in self.__attrs]


class MetaData:
    """Parses the text contents of a tag"""

    def __init__(self, tag: str, attr: str, contents: str, name: str):
        """
        tag - the type of tag to look at
        attr - only if it has this attr
        contents - and the attr value contains contents
        name - the name of the value to return
        """
        self.__tag = tag
        self.__name = name
        self.__attr = attr
        self.__contents = contents
        self.__in_tag = False
        self.__value = None

    def handle(self, entity: Entity):
        """look at html entities to find the metadata"""
        if entity.matches(self.__tag) and entity.contains(self.__attr, self.__contents):
            self.__in_tag = True
        elif entity.end and entity.matches(self.__tag):
            self.__in_tag = False
        elif entity.data is not None and self.__in_tag and entity.data.strip():
            self.__value = entity.data.strip()
            self.__in_tag = False

    def value(self) -> dict:
        """get the found"""
        return {} if self.__value is None else {self.__name: self.__value}


class TagPattern:
    """Search HTML tags for regex"""

    def __init__(self, tag: str, re_pattern):
        """
        tag - the type of tag to search the text of
        re_pattern - the re.compile pattern
                        Make sure to use re symbolic group name (?P<name>...).
                        The group name will be the name in the value returned.
        """
        self.__in_tag = 0
        self.__tag = tag
        self.__pattern = re_pattern
        self.__values = {}

    def handle(self, entity: Entity):
        """If we are inside of the given tag and the text matches pattern"""
        if entity.matches(self.__tag) and not entity.end:
            self.__in_tag += 1

        elif entity.matches(self.__tag) and entity.end:
            self.__in_tag -= 1

        elif entity.data is not None and self.__in_tag > 0:
            contains_pattern = self.__pattern.search(entity.data)

            if contains_pattern:
                found = {
                    k: v
                    for k, v in contains_pattern.groupdict().items()
                    if v is not None
                }
                self.__values.update(found)

    def value(self) -> dict:
        """return the named group -> match string for any found matches"""
        return self.__values


class Scraper(html.parser.HTMLParser):
    """Scrapes html values"""

    def __init__(self, *scanners):
        """scanners - A list of constructed objects that will be called to handle()
        Entity's in the html.
        """
        self.__scanners = scanners
        super().__init__()

    def __scan(self, entity: Entity):
        for scanner in self.__scanners:
            scanner.handle(entity)

    def handle_starttag(self, tag: str, attrs: list):
        self.__scan(Entity(name=tag, attrs=attrs))

    def handle_endtag(self, tag: str):
        self.__scan(Entity(name=tag, end=True))

    def handle_data(self, data: str):
        self.__scan(Entity(data=data))

    def error(self, message):
        pass

    def feed(self, data: str):
        super().feed(data)
        return self

    def properties(self) -> dict:
        """Get the properties found during scraping"""
        return {k: v for s in self.__scanners for k, v in s.value().items()}
