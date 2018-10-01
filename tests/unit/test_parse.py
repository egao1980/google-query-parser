import pytest
from pyparsing import ParseBaseException

from google_query import word, domain_name, in_site, related, file_type


@pytest.mark.parametrize('input,expected', [
    ('foo', True),
    ('foo:', False),
    ('OR', False),
    ('foo:bar', False),
    ('foo()', False),
    ('"foo"', False),
    ('f o o', False),
])
def test_word(input, expected):
    try:
        matched = word.parseString(input, True)
        assert expected and matched[0] == input
    except ParseBaseException:
        assert not expected


@pytest.mark.parametrize('input,expected', [
    ('.foo', True),
    ('bar.foo', True),
    ('apple.com', True),
    ('google.co.uk', True),
    ('xn--bcher-kva.example', True),
    ('foo()', False),
    ('"foo"', False),
    ('f o o', False),
])
def test_domain_name(input, expected):
    try:
        matched = domain_name.parseString(input, True)
        assert expected and matched[0] == input
    except ParseBaseException:
        assert not expected


@pytest.mark.parametrize('input,expected', [
    ('site:.apple.com', {'tag': 'site', 'value': '.apple.com'}),
    ('site:www.apple.com', {'tag': 'site', 'value': 'www.apple.com'})
])
def test_in_site(input, expected):
    matched = in_site.parseString(input, True)
    assert matched[0] == expected


@pytest.mark.parametrize('input,expected', [
    ('related:.apple.com', {'tag': 'related', 'value': '.apple.com'}),
    ('related:www.apple.com', {'tag': 'related', 'value': 'www.apple.com'}),
    ('related:.com', {'tag': 'related', 'value': '.com'})
])
def test_related(input, expected):
    matched = related.parseString(input, True)
    assert matched[0] == expected


@pytest.mark.parametrize('input,expected', [
    ('filetype:pdf', {'tag': 'filetype', 'value': 'pdf'}),
    ('filetype:yaml', {'tag': 'filetype', 'value': 'yaml'}),
    ('filetype:c', {'tag': 'filetype', 'value': 'c'}),
    ('filetype:r', {'tag': 'filetype', 'value': 'r'}),
])
def test_related(input, expected):
    matched = file_type.parseString(input, True)
    assert matched[0] == expected