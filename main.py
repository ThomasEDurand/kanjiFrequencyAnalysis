# TODO
# Add delta value to calculations?
# Allow word documents or pdfs to be opened also

import os
import pykakasi
import pyperclip
import webbrowser
import tkinter as tk
import concurrent.futures

from bs4 import BeautifulSoup
from requests import Session
from tkinter import filedialog


def assemblePage(kanjiWords, numWords):
    try:
        t = input("Save as: ") + '.html'
    except:
        t = 'result.html'

    # CHROME PATH CONFIGS MAY NEED CHANGE ON OTHER SYSTEMS
    chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
    d = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    path = os.path.join(d, t)

    entries = []
    with Session() as s:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for i, key in enumerate(kanjiWords):
                if i >= numWords:
                    break

                (currentWord, currentKana) = key
                URL = "https://jisho.org/search/" + currentWord
                print(str(i + 1) + "/" + str(numWords) + " words searched")
                try:
                    def lookupThread(_URL, _currentWord, _currentKana):
                        req = s.get(_URL)
                        soup = BeautifulSoup(req.content, 'html.parser')

                        # Using find instead of findall because I only want the first result now
                        ent = soup.find(class_='meanings-wrapper')
                        entries.append((ent, _currentWord, _currentKana))
                        print(entries)

                    executor.submit(lookupThread, URL, currentWord, currentKana)


                except:
                    print("Error searching word " + currentWord)

        executor.shutdown(wait=True)

        f = open(path, "w+", encoding='utf-8')
        for i, key in enumerate(entries):
            (entry, currentWord, currentKana) = key
            k = 0
            f.write('<p><b>' + str(i + 1) + ". " + currentWord + ": " + currentKana + '</b>' + "<br>")
            if entry is not None:
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

                    f.write('<p>')



        f.close()
    s.close()
    webbrowser.get(chrome_path).open(path)


def obscuritySort(kanjiDict):
    with open("Frequency.txt", "r", encoding='utf-8') as f:
        wordFreq = f.read().splitlines()
    f.close()

    for i, key in enumerate(kanjiDict):
        wordFound = False
        for j in range(0, len(wordFreq)):
            (h, k) = key
            if h == wordFreq[j] or k == wordFreq[j]:
                kanjiDict[key] = kanjiDict.get(key) * (j+1)
                wordFound = True
                break
        if not wordFound:
            kanjiDict[key] = kanjiDict.get(key) * 21000

    return dict(sorted(kanjiDict.items(), key=lambda x: x[1], reverse=True))


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

    kanjiDict = {}
    specialChars = ['\r', '\n', '｢', '｣']
    for p in parsed:
        orig, hira = p['orig'], p['hira']
        if orig != p['kana'] and orig != p['hira'] and orig not in specialChars:
            tup = (orig, hira)
            tupGet = kanjiDict.get(tup)
            if tupGet is not None:
                kanjiDict[tup] = tupGet + 1
            else:
                d = {tup: 1}
                kanjiDict.update(d)

    try:
        if int(input("0 to sort by order in text, 1 to sort by obscurity: ")):
            print(kanjiDict)
            kanjiDict = obscuritySort(kanjiDict)
            print(kanjiDict)
    except:
        kanjiDict = dict(sorted(kanjiDict.items(), key=lambda x: x[1], reverse=True))
        print("Error, sorting order")

    numWords = len(kanjiDict)
    if numWords > 10:
        print("Found " + str(numWords) + " words written with kanji")
        try:
            numWords = int(input("How many words to look up (hit 0 for all): "))
            if numWords == 0:
                numWords = len(kanjiDict)
        except:
            numWords = min(len(kanjiDict), 10)
            print("Invalid input, searching " + str(numWords) + " words")

    assemblePage(kanjiDict, numWords)


if __name__ == "__main__":
    main()
