from sqlalchemy import create_engine, Column, Table, ForeignKey, MetaData
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base # DeclarativeBase
from sqlalchemy import (
    Integer, String, Date, DateTime, Float, Boolean, Text)
from scrapy.utils.project import get_project_settings

Base = declarative_base()

#CONNECTION_STRING = 'sqlite:///FiScrape.db'

def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(get_project_settings().get("CONNECTION_STRING")) #, echo=True)
    #return create_engine(CONNECTION_STRING)


def create_table(engine):
    Base.metadata.create_all(engine)

# def create_output_table(engine, spider_name):
#     # Create table with the spider_name
#     DeclarativeBase.metadata.create_all(engine)

# Association Table for Many-to-Many relationship between Article and Author
# https://docs.sqlalchemy.org/en/13/orm/basic_relationships.html#many-to-many
authors_association = Table('authors_association', Base.metadata,
    Column('article_id', Integer, ForeignKey('article.id'), primary_key=True),
    Column('author_id', Integer, ForeignKey('author.id'), primary_key=True)
)

# Association Table for Many-to-Many relationship between Article and Topic
# https://docs.sqlalchemy.org/en/13/orm/basic_relationships.html#many-to-many
topics_association = Table('topics_association', Base.metadata,
    Column('article_id', Integer, ForeignKey('article.id'), primary_key=True),
    Column('topic_id', Integer, ForeignKey('topic.id'), primary_key=True)
)

# Association Table for Many-to-Many relationship between Article and Tag
# https://docs.sqlalchemy.org/en/13/orm/basic_relationships.html#many-to-many
tags_association = Table('tags_association', Base.metadata,
    Column('article_id', Integer, ForeignKey('article.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tag.id'), primary_key=True)
)


class Article(Base):
    __tablename__ = "article"

    id = Column(Integer, primary_key=True)
    published_date = Column('published_date', DateTime)
    headline = Column('headline', Text(), nullable=False)
    standfirst = Column('standfirst', Text())
    # article_content = Column('article_content', Text())
    article_link = Column('article_link', Text())
    source_id = Column(Integer, ForeignKey('source.id')) # , nullable=False)  # Many articles to one source
    #source = relationship('Source', backref='articles', nullable=False)
    #author_id = Column(Integer, ForeignKey('author.id'))  # Many articles to one author
    authors = relationship('Author', secondary='authors_association',
        lazy='dynamic', backref="article")  # M-to-M for article and authors
    topics = relationship('Topic', secondary='topics_association',
         lazy='dynamic', backref="article")  # M-to-M for article and topic
    tags = relationship('Tag', secondary='tags_association',
        lazy='dynamic', backref="article")  # M-to-M for article and tag
    # snip_blob_id = relationship(Integer, ForeignKey('snip_blob.id'))   # 1-to-1 for article and snip_blob
    # blob_id = relationship(Integer, ForeignKey('blob.id'))  # 1-to-1 for article and blob
    # snip_vader_id = relationship(Integer, ForeignKey('snip_vader.id')) # 1-to-1 for article and snip_vader
    # vader_id = relationship(Integer, ForeignKey('vader.id'))  # 1-to-1 for article and vader
    # def __repr__(self):
    #     return "<{0} Id: {1} - Published: {2} Headline: {3} Standfirst: {4} Source_id: {5} URL: {6}>".format(self.__class__name, self.id,
    #             self.published_date, self.headline, self.standfirst, self.link)


class Topic(Base):
    __tablename__ = "topic"

    id = Column(Integer, primary_key=True)
    name = Column('name', String(30), unique=True) #, nullable=False)
    articles = relationship('Article', secondary='topics_association',
        lazy='dynamic', backref="topic")  # M-to-M for article and topic
    # def __repr__(self):
    #     return "<{0} Id: {1} - Topic: {2} Headline: {3}>".format(self.__class__name, self.id,
    #             self.name)


class Source(Base):
    __tablename__ = "source"

    id = Column(Integer, primary_key=True)
    name = Column('name', String(50), unique=True) #, nullable=False)
    # inception = Column('inception', DateTime)
    # location = Column('location', String(150))
    # about = Column('about', Text())
    # bias = Column('bias', Text())  # Add https://www.allsides.com/media-bias/media-bias-ratings?field_featured_bias_rating_value=All&field_news_source_type_tid%5B2%5D=2&field_news_bias_nid_1%5B1%5D=1&field_news_bias_nid_1%5B2%5D=2&field_news_bias_nid_1%5B3%5D=3&field_news_bias_nid_1%5B4%5D=4&title=
    articles = relationship('Article', backref='source', lazy='dynamic') # One author to many Articles
    # def __repr__(self):
    #     # return "<{0} Id: {1} - Name: {2} Bias: {6} About: {5}>".format(self.__class__name, self.id,
    #     #         self.name, self.bias, self.about)
    #     return "<{0} Id: {1} - Name: {2}>".format(self.__tablename__, self.id,
    #             self.name)

class Author(Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True)
    name = Column('name', String(50), unique=True)
    bio = Column('bio', Text())
    twitter = Column('twitter', String(36))
    email = Column('email', String(50))
    # birthday = Column('birthday', DateTime)
    # bornlocation = Column('bornlocation', String(150))
    #articles = relationship('Article', backref='author')  # One author to many Articles
    articles = relationship('Article', secondary='authors_association',
        lazy='dynamic', backref="author")  # M-to-M for article and authors
    # def __repr__(self):
    #     return "<{0} Id: {1} - Name: {2} Bio: {3} Twitter: {4} Email: {5}>".format(self.__class__name, self.id,
    #             self.name, self.twitter, self.email)
    # __table__args = {'exted_existing':True}
    # bias = Column('bias', Text()) # Add https://www.allsides.com/media-bias/media-bias-ratings?field_featured_bias_rating_value=All&field_news_source_type_tid%5B1%5D=1&field_news_bias_nid_1%5B1%5D=1&field_news_bias_nid_1%5B2%5D=2&field_news_bias_nid_1%5B3%5D=3&field_news_bias_nid_1%5B4%5D=4&title=

class Tag(Base):
    __tablename__ = "tag"

    id = Column(Integer, primary_key=True)
    name = Column('name', String(30), unique=True)
    articles = relationship('Article', secondary='tags_association',
        lazy='dynamic', backref="tag")  # M-to-M for article and tag
    # def __repr__(self):
    #     return "<{0} Id: {1} - Name: {2}>".format(self.__class__name, self.id,
    #             self.name)

# class SnipBlob(Base):
#     __tablename__ = "snip_blob" # Blob sentiment scores for the headline and standfirst
#     # TextBlob, based on the Natural Language ToolKit (NLTK), sentiment scores.

#     id = Column(Integer, primary_key=True)
#     subjectivity = Column('subjectivity', Float)
#     polarity = Column('polarity', Float)
#     article = relationship('Article', uselist=False, backref='snip_blob')  # One SnipBlob to one Article
#     def __repr__(self):
#         # return "<{0} Id: {1} - Name: {2} Bias: {6} About: {5}>".format(self.__class__name, self.id,
#         #         self.name, self.bias, self.about)
#         return "<{0} Id: {1} - Subjectivity: {2} Polarity: {3} Article Id: {4}>".format(self.__class__name, self.id,
#                 self.subjectivity, self.polarity, self.article.id)

# class Blob(Base):
#     __tablename__ = "blob"  # TextBlob sentiment scores for the main body
#     # TextBlob, based on the Natural Language ToolKit (NLTK), sentiment scores.

#     id = Column(Integer, primary_key=True)
#     subjectivity = Column('subjectivity', Float)
#     polarity = Column('polarity', Float)
#     article = relationship('Article', uselist=False, backref='blob')  # One Blob to one Article
#     def __repr__(self):
#         # return "<{0} Id: {1} - Name: {2} Bias: {6} About: {5}>".format(self.__class__name, self.id,
#         #         self.name, self.bias, self.about)
#         return "<{0} Id: {1} - Subjectivity: {2} Polarity: {3} Article Id: {4}>".format(self.__class__name, self.id,
#                 self.subjectivity, self.polarity,self.article.id)

# class SnipVader(Base):
#     __tablename__ = "snip_vader" # Vader sentiment scores for the headline and standfirst
#     # Valence Aware Dictionary and sEntiment Reasoning lexicon-based sentiment scores

#     id = Column(Integer, primary_key=True)
#     compound = Column('compound', Float)
#     negative = Column('negative', Float)
#     neutral = Column('neutral', Float)
#     positive = Column('positive', Float)
#     article = relationship('Article', uselist=False, backref='snip_vader')  # One SnipVader to one Article
#     def __repr__(self):
#         # return "<{0} Id: {1} - Name: {2} Bias: {6} About: {5}>".format(self.__class__name, self.id,
#         #         self.name, self.bias, self.about)
#         return "<{0} Id: {1} - Compound: {2} Negative: {3} Neutral: {4} Positive: {5} Article Id: {6}>".format(self.__class__name, self.id,
#                 self.compound, self.negative, self.neutral, self.positive, self.article.id)

# class Vader(Base):
#     __tablename__ = "vader"  # Vader sentiment scores for the main body
#     # Valence Aware Dictionary and sEntiment Reasoning lexicon-based sentiment scores

#     id = Column(Integer, primary_key=True)
#     compound = Column('compound', Float)
#     negative = Column('negative', Float)
#     neutral = Column('neutral', Float)
#     positive = Column('positive', Float)
#     article = relationship('Article', uselist=False, backref='vader')  # One Vader to one Article
#     def __repr__(self):
#         # return "<{0} Id: {1} - Name: {2} Bias: {6} About: {5}>".format(self.__class__name, self.id,
#         #         self.name, self.bias, self.about)
#         return "<{0} Id: {1} - Compound: {2} Negative: {3} Neutral: {4} Positive: {5} Article Id: {6}>".format(self.__class__name, self.id,
#                 self.compound, self.negative, self.neutral, self.positive, self.article.id)

# from sqlalchemy.orm import aliased
# Sentiment = aliased(SnipVader)