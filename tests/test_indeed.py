#!/usr/bin/env python3


from talynt.indeed import parse


def test_basic():
    with open('tests/indeed_posting.html', 'r') as html:
        results = parse(html.read())

    assert 'solid background in software development' in results['description']
    assert results['type'] == "Full-time"
    assert results['title'] == "Engineering Manager, Sustaining Software Engineering, Worldwide"
    assert results['company'] == "Canonical"
    assert results['location'] == "Austin, TX"


if __name__ == "__main__":
    test_basic()
