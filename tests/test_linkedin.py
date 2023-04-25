#!/usr/bin/env python3


from talynt.linkedin import parse


def test_basic():
    with open('tests/linkedin_posting.html', 'r') as html:
        results = parse(html.read())

    assert 'Knowledge of data centers electrical infrastructure' in results['description']
    assert results['Seniority level'] == "Not Applicable"
    assert results['type'] == "Full-time"
    assert results['Job function'] == "Information Technology and Engineering"
    assert results['Industries'] == "Information Services and Technology, Information and Internet"
    assert results['title'] == "Power Monitoring Execution Engineer, Google Data Center"
    assert results['company'] == "Google"
    assert results['location'] == "Austin, TX"


if __name__ == "__main__":
    test_basic()
