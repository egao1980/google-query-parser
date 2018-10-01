import re

from pyparsing import Word, Literal, OneOrMore, Regex, Combine, StringEnd, FollowedBy, Suppress, Optional, White, \
    alphas, nums, alphanums

any_tag = Word(alphas) + FollowedBy(':')
word = Regex(r'[^-"\s()*|:]+', flags=re.UNICODE)
simple_query = OneOrMore(word) + StringEnd()
site = Regex(r'((xn--)?[a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,}', re.IGNORECASE)
domain_group = Regex(r'\.((xn--)?[a-z0-9]+(-[a-z0-9]+)*\.)*[a-z]{2,}', re.IGNORECASE)

AND = White(' ') | Literal(' AND ')
OR = Literal('|') | Literal(' OR ')
AROUND = Literal(' AROUND(') + Word(nums) + Literal(') ')
RANGE = Literal('..')

binary_op = OR | AROUND | AND


def tag(name):
    return Literal(name) + FollowedBy(':')


def tag_value(x):
    return {
        'tag': x[0],
        'value': ' '.join(x[1:])
    }


def all_in(name):
    return (tag('allin{}'.format(name)) + Suppress(':') + Suppress(Optional(White())) + OneOrMore(word)).setParseAction(tag_value)


def parse_tag(name, word):
    return (tag('{}'.format(name)) + Suppress(':') + word).setParseAction(tag_value)


in_site = tag('site') + Suppress(':') + site
related = tag('related') + Suppress(':') + site
file_type = parse_tag('filetype', Word(alphanums, max=4))


in_cache = (tag('cache') + Suppress(':') + site + simple_query).setParseAction(lambda x: {
    'tag': 'cache',
    'site': x[1],
    'value': ' '.join(x[2:])
})
query = all_in('text') | all_in('url') | all_in('title') | all_in('anchor') | in_cache
