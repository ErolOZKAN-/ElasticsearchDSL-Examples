from datetime import datetime
from elasticsearch_dsl import DocType, Date, Integer, Keyword, Text
from elasticsearch_dsl.connections import connections

# Define a default Elasticsearch client
connections.create_connection(hosts=['localhost'])
index = "myindex"

class Article(DocType):
    title = Text(analyzer='snowball', fields={'raw': Keyword()})
    body = Text(analyzer='snowball')
    tags = Keyword()
    published_from = Date()
    lines = Integer()

    class Meta:
        index = index

    def save(self, ** kwargs):
        self.lines = len(self.body.split())
        return super(Article, self).save(** kwargs)

    def is_published(self):
        return datetime.now() > self.published_from

# create the mappings in elasticsearch
Article.init()

# create and save an article
article = Article(meta={'id': 1}, title='Hello world!', tags=['text','text2'])
article.body = "looong text"
article.published_from = datetime.now()
article.save()

# create and save another article
article = Article(meta={'id': 2}, title='Hello world!', tags=['text','text2'])
article.body = "looong text 2"
article.published_from = datetime.now()
article.save()

# get article by id
article = Article.get(id=1)
print(article.is_published())

# Display cluster health
print(connections.get_connection().cluster.health())