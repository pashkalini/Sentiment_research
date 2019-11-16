import re
import pymorphy2
from bs4 import BeautifulSoup as bs

morph = pymorphy2.MorphAnalyzer()


def get_sample():
  with open('sample.xml', 'r', encoding='utf8') as inf:
    return bs(inf.read(), 'html.parser')


def lemmatize_texts(text):
  global morph
  texts = []
  for sentence in text:
    s = []
    word_list = re.sub('[».,«:;"%—!?)(]|\W-\W', '', sentence.strip().lower()).split()
    for word in word_list:
      p = morph.parse(word)[0]
      try:
        s.append(p.normal_form + '_' + p.tag.POS)
      except TypeError:
        s.append(word)
    texts.append(' '.join(s))
  return texts


def splitter(doc):
  return doc.split()