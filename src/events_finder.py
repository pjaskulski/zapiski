""" skrypt wyszukuje zdania z potencjalnymi wydarzeniami """
import re
import spacy

def sentence_filter(page_doc, current_page):
    """ filtruje zdania """
    pattern = r'\s?\d{1,2}\s+([a-ząśężźćńłó]{3,}|[XVI]+)\s+(15|149)'

    for sent in page_doc.sents:
        is_date = is_person = is_place = False
        sent_doc = sent.as_doc()
        for ent in sent_doc.ents:
            if ent.label_ == 'persName':
                is_person = True
            elif ent.label_ == 'placeName' and ent.text[0].isupper(): # tylko gdy nazwa zaczyna się z dużej litery
                is_place = True
            elif ent.label_ == 'date':
                match = re.search(pattern, ent.text) # weryfikacja czy jest to data dzienna z lat 1490-1599
                if match:
                    is_date = True
        if is_person and is_place and is_date:
            print(f"(str. {current_page}): ", sent.text.strip(), '\n')


nlp = spacy.load('pl_core_news_lg')

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


# przetwarzanie kolejnych stron
wyniki = []
for k_page, v_text in pages.items():
    doc = nlp(v_text)
    sentence_filter(doc, k_page)

