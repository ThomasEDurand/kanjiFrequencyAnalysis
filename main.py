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
# Condense definitions
# Add delta value to calculations

kanjiWords = []

with open("Frequency.txt", "r", encoding='utf-8') as f:
    wordFreq = f.read().splitlines()
f.close()

for p in parsed:
    orig = p['orig']
    hira = p['hira']
    if orig != p['kana'] and orig != p['hira'] and orig != '\r' and orig != '\n':  # check if word contains kanji
        wordFound = False
        for i in range(0, len(kanjiWords)):
            if kanjiWords[i][0] == orig:
                kanjiWords[i] = (kanjiWords[i][0], kanjiWords[i][1] ,kanjiWords[i][2] + 1)
                wordFound = True

        if not wordFound:
            kanjiWords.append((orig, hira, 1))

print(kanjiWords)

for i in range(0, len(kanjiWords)):
    wordFound = False
    for j in range(0, len(wordFreq)):
        if kanjiWords[i][0] == wordFreq[j]:
            kanjiWords[i] = (kanjiWords[i][0], kanjiWords[i][1], kanjiWords[i][2] * (j + 1))
            wordFound = True
    if not wordFound:
        kanjiWords[i] = (kanjiWords[i][0], kanjiWords[i][1], kanjiWords[i][2] * 21000)


kanjiWords.sort(key=lambda y: y[2], reverse=True)
print(kanjiWords)

numWords = 0
if len(kanjiWords) > 10:
    print("Found " + str(len(kanjiWords)) + " words written with kanji")

    try:
        numWords = int(input("How many words to look up (hit 0 for all): "))
    except:
        numWords = min(len(kanjiWords), 10)
        print("Invalid input, searching " + str(numWords) + " words")

    if numWords == 0:
        numWords = len(kanjiWords)

else:
    numWords = len(kanjiWords)

try:
    t = input("Save as: ") + '.html'
except:
    t = 'result.html'

# CHROME PATH CONFIGS MAY NEED CHANGE ON OTHER SYSTEMS
chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
d = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
path = os.path.join(d, t)

with Session() as s:
    f = open(path, "w+", encoding='utf-8')
    for i in range(0, numWords):
        currentWord = kanjiWords[i][0]
        currentKana = kanjiWords[i][1]
        URL = "https://jisho.org/search/" + currentWord
        print(URL)
        f.write('<p><b>' + str(i+1) + ". " + currentWord + ": " + currentKana + '</b></p>' + "\n")
        try:
            req = s.get(URL)
            soup = BeautifulSoup(req.content, 'html.parser')
            # Using find instead of findall because I only want the first result now
            entry = soup.find(class_='meanings-wrapper')
            for e in entry:
                f.write('<p>' + e.text + '</p>')

        except:
            print("Error searching word " + currentWord)

        f.write("\n")

    f.close()
s.close()

webbrowser.get(chrome_path).open(path)
