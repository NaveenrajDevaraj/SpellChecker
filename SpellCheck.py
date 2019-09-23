import os
from collections import Counter
import re
import pathlib
from os.path import abspath, exists

lineList = []
f_path = abspath("corpus-challenge5.txt")
if exists(f_path):
    sourceFileName = f_path
else:
    print("By default corpus-challenge5.txt file not exist in the current directory please specify the source location of file")
    while 1:
        sourceFileName = input("Enter Source File Name:   ")
        path = pathlib.Path(sourceFileName)
        if(path.exists()):
            break
        else:
            print("Not a valid source file, Plese enter the valid information")
            continue

with open(os.path.expanduser(sourceFileName)) as f:
    for line in f:
        for word in re.findall(r'\w+', line):
            lineList.append(re.sub(r"[^a-zA-Z0-9/'-]","",word.lower()))
print("read complete")
def compare(user_word,wordMap):
    found_word = ''
    frequency = 0
    break_count = 0
    for word in wordMap:
        if len(word) == len(user_word) or len(word) == len(user_word) - 1 or len(word) == len(user_word) + 1:
            for i in range(min(len(user_word), len(word))):
                if user_word[i] == word[i]:
                    continue
                elif(break_count < 2):
                    break_count = break_count + 1
                    continue
                else:
                    break
            if(break_count < 2):
                if wordMap[word] > frequency:
                    frequency = wordMap[word]
                    found_word = word
            else:
                break_count = 0
                continue
    return found_word

def missing_char(user_word,wordMap):
    found_word = ''
    frequency = 0
    temp_word= user_word
    break_count = 0
    for word in wordMap:
        if len(user_word) == len(word)-1:
            for i in range(min(len(wordMap),len(word))):
                if temp_word[i] == word[i]:
                    continue
                elif len(word) > i + 1 and temp_word[i] == word[i + 1] and break_count != 2:
                    temp_word = internal_swap(temp_word, i, word[i])
                    break_count = break_count + 1
                    continue
                else:
                    break_count = 2
                    temp_word = user_word
                    break
            if break_count < 2:
                if wordMap[word] > frequency:
                    frequency = wordMap[word]
                    found_word = word
            else:
                break_count = 0
                continue
    return found_word


def internal_swap(user_word,i,char):
    temp = [None] * (len(user_word)+1)
    k = 0
    for j in range(len(user_word)):
        if i == j:
            temp[i] = char
            k = k+1
        temp[k] = user_word[j]
        k = k + 1
    return temp


def swap_char(user_word,wordMap):
    found_word = ''
    frequency = 0
    break_count = 0
    temp_word = user_word
    for word in wordMap:
        if set(word) == set(user_word):
            for i in range(min(len(user_word), len(word))):
                if temp_word[i] == word[i]:
                    continue
                elif (temp_word[i] == word[i+1] and temp_word[i+1] == word[i]) and break_count != 2:
                    temp_list = list(temp_word)
                    temp_list[i] = temp_word[i]
                    temp_list[i+1] = temp_word[i]
                    temp_word = ''.join(temp_list)
                    break_count = break_count + 1
                    continue
                else:
                    break_count = 2
                    temp_word = user_word
                    break
            if (break_count < 2):
                print(word)
                if wordMap[word] > frequency:
                    frequency = wordMap[word]
                    found_word = word
            else:
                break_count = 0
                continue
    return found_word


def repeat_char(user_word,wordMap):
    found_word = ''
    frequency = 0
    break_count = 0
    temp_word = user_word
    for word in wordMap:
        if set(user_word) == set(word):
            for i in range(min(len(user_word), len(word))):
                if temp_word[i] == word[i]:
                    continue
                elif (i != 0 and temp_word[i] == word[i-1] and temp_word[i] == temp_word[i-1]) and break_count != 2:
                    temp_list = list(temp_word)
                    temp_list[i] = ''
                    temp_word = ''.join(temp_list)
                    break_count = break_count + 1
                    continue
                else:
                    break_count = 2
                    temp_word = user_word
                    break
            if (break_count < 2):
                if wordMap[word] > frequency:
                    frequency = wordMap[word]
                    found_word = word
            else:
                break_count = 0
                continue
    return found_word

wordMap = Counter(lineList)
wordCount = int(input("Number of words:"))
user_words = []

for i in range(wordCount):
    user_words.append(input("Enter the word to compare %d :"%i).lower())
for i in range(wordCount):
    if user_words[i] != '':
        if user_words[i] in wordMap:
            print("user word exists :",user_words[i])
        else:
            found_word = compare(user_words[i], wordMap)
            if (found_word == ''):
                found_word = compare(user_words[i], wordMap)
                if(found_word == ''):
                    found_word = missing_char(user_words[i], wordMap)
                    if(found_word == ''):
                        found_word = repeat_char(user_words[i],wordMap)
            if(found_word == ''):
                print("word not found so display as it is", user_words[i])
            else:
                print("Word Found ------- Actual Word: ",user_words[i]," Corrected Word: ", found_word)

