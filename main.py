# TODO
# Add delta value to calculations?
# Allow word documents or pdfs to be opened also

import os
import pykakasi
import pyperclip
import webbrowser
import tkinter as tk

from bs4 import BeautifulSoup
from requests import Session
from tkinter import filedialog


def assembleKanjiDict(kanjiWords, numWords):
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
            print(str(i + 1) + "/" + str(numWords) + " words searched")
            f.write('<p><b>' + str(i + 1) + ". " + currentWord + ": " + currentKana + '</b>' + "<br>")
            try:
                req = s.get(URL)
                soup = BeautifulSoup(req.content, 'html.parser')
                # Using find instead of findall because I only want the first result now
                entry = soup.find(class_='meanings-wrapper')
                k = 0
                for e in entry:
                    if "Wikipedia definition" in e.text:
                        break
                    else:
                        # Based on the format of jisho.org such that entry number and entry are printed on the same line
                        if k % 2 == 0:
                            f.write('' + e.text + ': ')
                            k += 1
                        else:
                            f.write(e.text + '<br>')
                            k += 1

            except:
                print("Error searching word " + currentWord)

            f.write('<p>')

        f.close()
    s.close()
    webbrowser.get(chrome_path).open(path)


def obscuritySort(kanjiWords):
    with open("Frequency.txt", "r", encoding='utf-8') as f:
        wordFreq = f.read().splitlines()
    f.close()

    for i, word in enumerate(kanjiWords):
        wordFound = False
        for j in range(0, len(wordFreq)):
            if kanjiWords[i][0] == wordFreq[j]:
                kanjiWords[i][2] *= (j + 1)
                wordFound = True
        if not wordFound:
            kanjiWords[i][2] *= 21000



def main():
    kakasi = pykakasi.kakasi()
    parsed = kakasi.convert(pyperclip.paste())

    try:
        if int(input("0 to use text from clipboard, 1 to chose local file: ")):
            root = tk.Tk()
            root.withdraw()
            file_path = filedialog.askopenfilename()
            print(file_path)
            with open(file_path, "r", encoding='utf-8') as f:
                parsed = kakasi.convert(f.read().replace('\n', ''))
            f.close()
    except:
        print("Invalid input, using text from clipboard")

    kanjiWords = []
    specialChars = ['\r', '\n', '｢', '｣']  # special chars that kakasi picks up sometimes
    # Assemble kanjiWords from parsed
    for p in parsed:
        orig, hira = p['orig'], p['hira']
        if orig != p['kana'] and orig != p['hira'] and orig not in specialChars:  # check if word contains kanji
            wordFound = False
            for i, word in enumerate(kanjiWords):
                if word[0] == orig:
                    kanjiWords[i][2] += 1
                    wordFound = True
            kanjiWords.append([orig, hira, 1]) if not wordFound else None

    try:
        if int(input("0 to sort by order in text, 1 to sort by obscurity: ")):
            obscuritySort(kanjiWords)
    except:
        kanjiWords.sort(key=lambda y: y[2], reverse=True)
        print("Error, sorting order")

    print(kanjiWords)

    numWords = len(kanjiWords)
    if numWords > 10:
        print("Found " + str(numWords) + " words written with kanji")
        try:
            numWords = int(input("How many words to look up (hit 0 for all): "))
            if numWords == 0:
                numWords = len(kanjiWords)
        except:
            numWords = min(len(kanjiWords), 10)
            print("Invalid input, searching " + str(numWords) + " words")

    assembleKanjiDict(kanjiWords, numWords)


if __name__ == "__main__":
    main()
