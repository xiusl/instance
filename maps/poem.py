# coding=utf-8
# author:xsl

from instance.maps import mapping
from instance.resource import (
    PoemAuthorsRes,
    PoemsRes,
    PoemTagsRes,
)

poem_prefix = '/p'
poem_map = {
    PoemAuthorsRes: '/authors',
    PoemsRes: '/poems',
    PoemTagsRes: '/tags', 
}

def map_poem(api):
    mapping(api, poem_prefix, poem_map)
