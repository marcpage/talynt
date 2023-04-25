#!/usr/bin/env python3


from talynt.html import Entity, Scraper

HTML = """
<html>
    <head>
        <title>Test</title>
    </head>
    <body>
        <div id="test" class="test me more">
        </div>
    </body>
</html>
"""

class Scanner:
    def handle(self, entity:Entity):
        if entity.matches('div') and not entity.end:
            assert entity['id'] == 'test', entity
            assert entity.contains('class', 'more'), entity
            assert len(entity) == 2, entity
            assert entity.has_key('id'), entity
            assert entity.has_key('class'), entity
            assert set(entity.keys()) == {'class', 'id'}, entity
            assert set(entity.values()) == {'test', 'test me more'}, entity
        elif not entity.end:
            assert len(entity) == 0, entity

    def value(self) -> dict:
        return {}


def test_basic():
    value = Scraper(Scanner()).feed(HTML).properties()


if __name__ == "__main__":
    test_basic()
