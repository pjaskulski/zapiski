""" skrypt tworzy listę popularnych rzeczowników z podanego tekstu artykułu """
import re
import locale
from collections import Counter
import spacy


def first_cap(input_string: str) -> bool:
    """ czy pierwsza duża litera? """
    return input_string[0].isupper()


nlp = spacy.load('pl_core_news_md')
with open('./data/output_clear.txt', 'r', encoding='utf-8') as f:
    text = f.readlines()

pattern_page = r'\[PAGE:\s*\d{1,3}\]'
pattern_number = r'\d{1,3}'
page_num = ''

nouns = []
nouns_text = {}
noun_counter = Counter()

# słownik na zawartość poszczególnych stron tekstu
pages = {}

print('Wczytanie tekstu...')

for line in text:
    match = re.search(pattern_page, line)
    if match:
        page = match.group().strip()
        match = re.search(pattern_number, page)
        if match:
            page_num = int(match.group())
    else:
        if not page_num:
            continue # ewentualny tekst przed pierwszym numerem strony pomijamy

        if page_num in pages:
            pages[page_num] = pages[page_num] + line
        else:
            pages[page_num] = line

person_index = {}
for k_page, v_text in pages.items():
    print(f'Przetwarzanie strony: {k_page}')
    doc = nlp(v_text)

    for token in doc:
        if token.pos_ == "NOUN":
            lemma = token.lemma_
            word = token.text
            if not first_cap(lemma):
                nouns.append(lemma)
                if lemma in nouns_text:
                    nouns_text[lemma].append(word)
                else:
                    nouns_text[lemma] = [word]

noun_counter.update(Counter(nouns))
tmp_nouns = list(noun_counter.most_common())

for tmp in tmp_nouns:
        if tmp[0] in nouns_text:
            lista = list(set(nouns_text[tmp[0]]))
            tmp = tmp + ('', ', '.join(lista),)
        if tmp[1] > 10:
            print(tmp)

#locale.setlocale(locale.LC_COLLATE, "pl_PL.UTF-8")
#persons = sorted(list(person_index.keys()), key=locale.strxfrm)

