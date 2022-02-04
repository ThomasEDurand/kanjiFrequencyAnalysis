import pykakasi
import pyperclip
from requests import Session
from bs4 import BeautifulSoup
import os


kakasi = pykakasi.kakasi()
clpbrd = pyperclip.paste()
parsed = kakasi.convert(clpbrd)

# TODO
# Convert verbs to stem form
# Find better Frequency List
# Run top X words through Jisho.org
# Return a HTML Document and open with Chrome

kanjiWords = []

with open("Frequency.txt", "r",encoding='utf-8') as f:
    wordFreq = f.read().splitlines()
f.close()

for p in parsed:
    orig = p['orig']
    if orig != p['kana'] and orig != p['hira']: #is kanji word
        wordFound = False
        for i in range(0, len(kanjiWords)):
            if kanjiWords[i][0] == orig:
                kanjiWords[i] = (kanjiWords[i][0], kanjiWords[i][1] + 1)
                wordFound = True

        if not wordFound:
            kanjiWords.append((orig, 1))

print(kanjiWords)

for i in range(0, len(kanjiWords)):
    for j in range(0, len(wordFreq )):
        if kanjiWords[i][0] == wordFreq[j]:
            kanjiWords[i] = (kanjiWords[i][0], kanjiWords[i][1] * (j+1))

kanjiWords.sort(key=lambda y: y[1], reverse=True)
print(kanjiWords)

URL = "https://jisho.org/search/"

with Session() as s:
    # f.open("result", "w+")
    for i in range(0, 1):
        URL = "https://jisho.org/word/" + kanjiWords[i][0]
        print(URL)
        req = s.get(URL)
        soup = BeautifulSoup(req.content, 'html.parser')
        entry = soup.find(class_='meanings-wrapper')

        print(entry)


