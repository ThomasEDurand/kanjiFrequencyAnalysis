# Kanji Word Frequency Analysis

The Japanese language is written using a combination of three alphabets: Hiragana, Katakana, and Kanji. The former two are phonetic and the third alphabet is composed of logographic Chinese characters. 
Because of each Kanji having multiple readings and the vast amount of them in use, Kanji are difficult for both Japanese and foreigners to learn. It is said that one needs to know over 3000 kanji to read a newspaper. 
This program was designed to ease the prep work required for reading Japanese texts by generating a list of words that should be learned before reading.
The pertinence of the word is calculated using both its frequency in the text and its use in the Japanese language. The list is then sorted based on this pertinence value
How to use:
1. Copy the text you want parsed to your clipboard and run the program (Planning on adding an option to upload files for parsing in the future)
2. Select how many words from the text you want saved and the name of the text. Selecting 50 will generate a list of the 50 most important Kanji words in the text along with definitions of them.
3. An HTML file will be generated and opened in Chrome if it is installed on your computer and saved to your desktop (Many HTML to PDF converters exist online)

Note
Japanese while being studied a decent amount in the west does not have as many resources as other Indo-European languages do. As such the frequency list from Wiktionary only compiles the frequency of about 20000 words. These words make up around 97.5% of all words spoken in Japanese (see Zipf's Law.) Words not in this first 20000 are still searched and added to the file but the calculation of the pertinence is a bit arbitrary. 

Discloser
The project uses jisho.org for the definition of the terms I AM NOT AFFILIATED WITH THIS ORGANIZATION  
Frequency lists from https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists/Japanese10001-20000



