""" skrypt tworzy indeks postaci z podanego tekstu artykułu """
import re
import locale
import spacy


nlp = spacy.load('pl_core_news_md')
with open('./data/output_clear.txt', 'r', encoding='utf-8') as f:
    text = f.readlines()

pattern_page = r'\[PAGE:\s*\d{1,3}\]'
pattern_number = r'\d{1,3}'
page_num = ''

# słownik na zawartość poszczególnych stron tekstu
pages = {}

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
    doc = nlp(v_text)

    for ent in doc.ents:
        # jeżeli osoba
        # bez krótkich znalezisk -  są zwykle błędne
        # jeżeli nie zaczyna się od dużej litery - pomijamy
        if ent.label_ == 'persName' and len(ent.text) > 2 and ent.lemma_[0].isupper():
            if ent.lemma_ in person_index:
                if k_page not in person_index[ent.lemma_]:
                    person_index[ent.lemma_].append(k_page)
            else:
                person_index[ent.lemma_] = [k_page]

locale.setlocale(locale.LC_COLLATE, "pl_PL.UTF-8")
persons = sorted(list(person_index.keys()), key=locale.strxfrm)

for item in persons:
    print(item, person_index[item])
