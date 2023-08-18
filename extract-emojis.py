import requests
import re

url = 'https://www.unicode.org/Public/emoji/latest/emoji-test.txt'
response = requests.get(url)
emojiLines = response.text.split('\n')

emojis = []

emojiPattern = re.compile(r'^([0-9A-F ]+);\s*.*# (.*)$')

for line in emojiLines:
    match = emojiPattern.match(line)
    if match:
        emoji = match.group(2)
        emojis.append(emoji)

outputFilePath = 'extracted_emojis.txt'
with open(outputFilePath, 'w', encoding='utf-8') as outputFile:
    inserted = 0
    for emoji in emojis:
        outputFile.write(emoji.split()[0] + '\n')
        inserted += 1

print(f"extracted emojis have been written to {outputFilePath}")
print(f"extracted {inserted} emojis")
