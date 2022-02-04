import webbrowser
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
# CONFIGURE CHROME PATHS
# Condense definition

kanjiWords = []

with open("Frequency.txt", "r", encoding='utf-8') as f:
    wordFreq = f.read().splitlines()
f.close()

for p in parsed:
    orig = p['orig']
    if orig != p['kana'] and orig != p['hira']:  # check if word contains kanji
        wordFound = False
        for i in range(0, len(kanjiWords)):
            if kanjiWords[i][0] == orig:
                kanjiWords[i] = (kanjiWords[i][0], kanjiWords[i][1] + 1)
                wordFound = True

        if not wordFound:
            kanjiWords.append((orig, 1))

print(kanjiWords)


for i in range(0, len(kanjiWords)):
    for j in range(0, len(wordFreq)):
        if kanjiWords[i][0] == wordFreq[j]:
            kanjiWords[i] = (kanjiWords[i][0], kanjiWords[i][1] * (j + 1))

kanjiWords.sort(key=lambda y: y[1], reverse=True)
print(kanjiWords)

URL = "https://jisho.org/search/"

# CHROME PATH CONFIGS WILL NEED TO CHANGE ON OTHER COMPUTERS
chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
d = r'C:\Users\Thomas\PycharmProjects\jpnWFA\results'
title = "result"
t = title + '.html'

path = os.path.join(d, t)

print("Found " + str(len(kanjiWords)) + " words written with kanji")
numWords = int(input("How many words to look up (hit 0 for all): "))
if numWords == 0:
    numWords = len(kanjiWords)

with Session() as s:
    f = open(path, "w+", encoding='utf-8')
    for i in range(0, numWords):
        currentWord = kanjiWords[i][0]
        URL = "https://jisho.org/word/" + currentWord
        print(URL)
        f.write('<p><b>' + str(i+1) + " " + currentWord + '</b></p>' + "\n")
        try:
            req = s.get(URL)
            soup = BeautifulSoup(req.content, 'html.parser')
            # Using find instead of findall because I only want the first result now
            entry = soup.find(class_='meanings-wrapper')
            for e in entry:
                f.write('<p>' + e.text + '</p>')

        except:
            print("Error searching word")

        f.write("\n")

    f.close()
s.close()

webbrowser.get(chrome_path).open(path)
