""" skrypt tworzy listę popularnych rzeczowników z podanego tekstu artykułu """
import re
import locale
import spacy
from spacy.matcher import Matcher


lista = ['król', 'kapitan', 'komisarz', 'strażnik', 'kapr', 'kaper', 'poseł', 'car', 'kupiec',
'żołnierz', 'cesarz',
'senator', 'członek', 'kasztelan', 'urzędnik', 'admirał', 'delegat', 'mistrz',
'żeglarz', 'prezes', 'sekretarz', 'armator', 'władca', 'kanclerz', 'marynarz', 'właściciel',
'dowódca', 'podkanclerzy', 'namiestnik', 'książę', 'starosta', 'sługa',
'wojownik', 'mocodawca', 'burmistrz', 'delegat', 'historyk', 'koadiutor',
'elektor'
]

patterns = [
        [{"LEMMA": {"IN": lista}}, {"POS":"ADJ", "OP":"?"},{"POS":"PROPN", "OP":"+"}],
        [{"POS":"PROPN", "OP":"+"}, {"LEMMA": {"IN": lista}}, {"POS":"ADJ", "OP":"?"},{"POS":"PROPN", "OP":"+"}],
    ]

nlp = spacy.load('pl_core_news_md')

matcher = Matcher(nlp.vocab)
matcher.add("Zlozone", patterns=patterns)

with open('./data/output_clear.txt', 'r', encoding='utf-8') as f:
    text = f.readlines()

pattern_page = r'\[PAGE:\s*\d{1,3}\]'
pattern_number = r'\d{1,3}'
page_num = ''

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

wyniki = []
for k_page, v_text in pages.items():
    print(f'Przetwarzanie strony: {k_page}')
    doc = nlp(v_text)

    matches = matcher(doc)

    # tylko nie zawierające się znaleziska
    spans = [doc[start:end] for _, start, end in matches]
    for span in spacy.util.filter_spans(spans):
        funkcja = span.text.strip()
        #wyniki.append(f'{funkcja} ({k_page})')
        if funkcja not in wyniki:
            wyniki.append(funkcja)

locale.setlocale(locale.LC_COLLATE, "pl_PL.UTF-8")
wyniki = sorted(wyniki, key=locale.strxfrm)

for item in wyniki:
    print(item)
