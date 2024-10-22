#from __future__ import unicode_literals, print_function
from spacy.lang.pt import Portuguese
import bs4

import os
import urllib3

nlp = Portuguese()
nlp.add_pipe('sentencizer')


urls = ["pt.wikipedia.org/wiki/Damares_Alves",
      "pt.wikipedia.org/wiki/Incidente_de_Varginha",
      "pt.wikipedia.org/wiki/George_Santos"]

def get_page(url):
    return urllib3.request('GET', url)


def get_text(response):

    html = response.data
    soup = bs4.BeautifulSoup(html, 'html.parser')
 
    t =  soup.findAll('title')
    return [p.get_text() for p in  soup.findAll('p')]


def get_sentences(paragrafos):
    texto = ' '.join(paragrafos)
    doc = nlp(texto)
    return [sent.text.strip() for sent in doc.sents]


def main():
    
    texts = []

    for url in urls:
        
        nome = os.path.split(url)[-1]
        
        response = get_page(url)
        paragrafos = get_text(response)
        sentences = get_sentences(paragrafos)

        texts.append({'nome': nome, 'text': sentences})

    return texts


main()
