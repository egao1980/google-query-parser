import pytest
from pyparsing import ParseBaseException, lineno, col

from google_query import word, domain_name, in_site, related, file_type, query, search_query


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
    ('site:.apple.com', {'site': '.apple.com'}),
    ('site:www.apple.com', {'site': 'www.apple.com'})
])
def test_in_site(input, expected):
    matched = in_site.parseString(input, True)
    assert matched[0] == expected


@pytest.mark.parametrize('input,expected', [
    ('related:.apple.com', {'related': '.apple.com'}),
    ('related:www.apple.com', {'related': 'www.apple.com'}),
    ('related:.com', {'related': '.com'})
])
def test_related(input, expected):
    matched = related.parseString(input, True)
    assert matched[0] == expected


@pytest.mark.parametrize('input,expected', [
    ('filetype:pdf', {'filetype': 'pdf'}),
    ('filetype:yaml', {'filetype': 'yaml'}),
    ('filetype:c', {'filetype': 'c'}),
    ('filetype:r', {'filetype': 'r'}),
])
def test_related(input, expected):
    matched = file_type.parseString(input, True)
    assert matched[0] == expected


@pytest.mark.parametrize('input,expected', [
    ('foo bar', {'AND': ['foo', 'bar']}),
    ('foo AND bar', {'AND': ['foo', 'bar']}),
    ('foo OR bar', {'OR': ['foo', 'bar']}),
    ('foo | bar', {'|': ['foo', 'bar']}),
    ('foo * bar', {'*': ['foo', 'bar']}),
    ('foo AROUND(3) bar', {'AROUND': ['foo', '3', 'bar']}),
])
def test_query(input, expected):
    matched = query.parseString(input, True)
    assert matched[0] == expected


@pytest.mark.parametrize('input,expected', [
    ('foo bar', {'AND': ['foo', 'bar']}),
    ('foo AND bar', {'AND': ['foo', 'bar']}),
    ('foo OR bar', {'OR': ['foo', 'bar']}),
    ('foo | bar', {'|': ['foo', 'bar']}),
    ('foo * bar', {'*': ['foo', 'bar']}),
    ('foo AROUND(3) bar', {'AROUND': ['foo', '3', 'bar']}),
    ('foo bar buzz', {'AND': ['foo', 'bar', 'buzz']}),
    ('$4..$10', {'RANGE': ['$4', '$10']}),
    ('4..10', {'RANGE': ['4', '10']}),
])
def test_search_query(input, expected):
    matched = query.parseString(input, True)
    assert matched[0] == expected


def test_search_query2():
    parsed = search_query.parseString(
        'foo bar site:apple.com filetype:pdf OR filetype:doc 1 2 $3 1..2 $4..$10 foo AROUND(3) bar * foo',
        parseAll=True)
