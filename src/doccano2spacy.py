""" doccano to spacy """

import json
import sys
from spacy.tokens import DocBin
import spacy

nlp = spacy.blank("pl")
db = DocBin()

filename = sys.argv[1]
with open(filename, "r", encoding="utf-8") as f:
    data = f.readlines()

for line in data:
    line = json.loads(line)

    text = labels = None
    if "text" in line:
        text = line["text"]
    if "label" in line:
        labels = line["label"]

    if text and labels:
        doc = nlp.make_doc(text)
        ents = []
        for start, end, label in labels:
            print(start, end, label)
            span = doc.char_span(start, end, label=label,
                                 alignment_mode="contract")
            if span:
                ents.append(span)
        doc.ents = ents
        db.add(doc)

db.to_disk(filename + ".spacy")
