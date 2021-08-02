# coding=utf-8
# author:xsl


from instance.maps import mapping
from instance.resource import (
    ArticleSpiderRes,
    ArticlesRes,
    ArticleRes,
    ArticleTagsRes,

    SourcesRes,

    SpiderRes,
    SpiderArtsRes,
    SpiderArticlesRes,

    TagsRes,
    TagRes,
)

# 文章
art_prefix = '/articles'
art_map = {
    ArticlesRes: '',
    ArticleRes: '/<id>',
    ArticleSpiderRes: 'spider'
}

# 来源
source_prefix = '/sources'
source_map = {
    SourcesRes: ''
}

# 爬虫
spider_prefix = '/spider'
spider_map = {
    SpiderRes: '',
    SpiderArticlesRes: '/articles',
}

# 标签
tag_prefix = '/tags'
tag_map = {
    TagsRes: '',
    TagRes: '/<id>',
}

def map_article(api):
    mapping(api, art_prefix, art_map)
    mapping(api, source_prefix, source_map)
    mapping(api, spider_prefix, spider_map)
    mapping(api, tag_prefix, tag_map)
