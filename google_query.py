import re

from pyparsing import (Word, Literal, OneOrMore, Regex, StringEnd, FollowedBy, Suppress, Optional, White,
                       alphas, alphanums, Keyword, QuotedString, infixNotation, opAssoc, nums, pyparsing_common,
                       Combine)

and_kw, or_kw, around_kw, star_kw = map(lambda x: Keyword(x, caseless=False), ['AND', 'OR', 'AROUND', '*'])
reserved_words = (and_kw | or_kw | around_kw | star_kw)
any_tag = Word(alphas) + FollowedBy(':')
word = ~reserved_words + Regex(r'\b[^-"\s()*|:]+\b', flags=re.UNICODE)
simple_query = OneOrMore(word)
domain_name = Regex(r'\.?((xn--)?[a-z0-9]+(-[a-z0-9]+)*\.)*((xn--[a-z0-9]{2,})|([a-z]{2,}))', re.IGNORECASE)
quoted_string = QuotedString('"')


def tag(name):
    return Literal(name) + FollowedBy(':')


def tag_value(x):
    return {
        'tag': x[0],
        'value': ' '.join(x[1:])
    }


def parse_tag(name, word):
    return (tag('{}'.format(name)) + Suppress(':') + word).setParseAction(tag_value)


in_site = parse_tag('site', domain_name)
related = parse_tag('related', domain_name)
file_type = parse_tag('filetype', Word(alphanums, max=4))

in_cache = (tag('cache') + Suppress(':') + domain_name + simple_query).setParseAction(lambda x: {
    'tag': 'cache',
    'site': x[1],
    'value': ' '.join(x[2:])
})

raw_text = Regex(r'\S+')
number = Regex(r'[+-]?\d+(\.\d+)?')
price = Combine(Literal('$') + number)


def add_range(values):
    return {'tag': 'range',
            'start': values[0],
            'end': values[1]}


num_range = (number + FollowedBy('..') + Suppress('..') + number).setParseAction(add_range)
price_range = (price + FollowedBy('..') + Suppress('..') + price).setParseAction(add_range)

in_anchor, in_text, int_title, in_url = map(lambda name: parse_tag(name, raw_text | quoted_string),
                                            ['inanchor', 'intext', 'intitle', 'inurl'])

tags = (in_site | file_type | related | in_anchor | in_text | int_title | in_url)
token = (star_kw | price_range | price | num_range | number | tags | word | quoted_string)
query = infixNotation(token, [
    (around_kw + Suppress('(') + Word(nums) + Suppress(')'), 2, opAssoc.LEFT),
    (or_kw, 2, opAssoc.LEFT),
    (Optional(and_kw, default='AND'), 2, opAssoc.LEFT),
])


def all_in(name):
    return (tag('allin{}'.format(name))
            + Suppress(':')
            + Suppress(Optional(White()))
            + OneOrMore(word, stopOn=any_tag | StringEnd())
            ).setParseAction(tag_value)


all_in_query = (all_in('text') | all_in('url') | all_in('title') | all_in('anchor')) + (
        Optional(in_site) & Optional(file_type) & Optional(related))

search_query = all_in_query | in_cache | query


def parse(query):
    return simple_query.parseString(query, True)
