file = open("WordleList.txt", "r")
wordList, letterFrequency = file.read().split("\n\n")
wordScore = 0
wordScores = []
newWordList = []
newWordScores = []
wordList = wordList.split("\n")
letterFrequency = [line.replace("\t", "") for line in letterFrequency.split("\n")]
wrongLetters = input("Enter Incorrect Letters: ")
rightLetters = input("Enter Correct Letters: ")
for letter in wrongLetters:
    for value in range(len(letterFrequency)):
        if letter == letterFrequency[value][0]:
            letterFrequency[value] = letterFrequency[value][0]
            letterFrequency[value] += "0"

        if letter.capitalize() == letterFrequency[value][0]:
            letterFrequency[value] = letterFrequency[value][0]
            letterFrequency[value] += "0"

for letter in rightLetters:
    for value in range(len(letterFrequency)):
        if letter == letterFrequency[value][0]:
            letterFrequency[value] = letterFrequency[value][0]
            letterFrequency[value] += "10000"

for word in wordList:
    currentWord = word
    wordScore = 0
    for letter in currentWord:
        if currentWord.count(letter) == 2:
            for value in letterFrequency:
                if letter.capitalize() == value[0]:
                    wordScore += int(value[1:])
            currentWord = currentWord.replace(letter, "", 1)
        elif currentWord.count(letter) > 2:
            currentWord = currentWord.replace(letter, "", 1)

    newWordScores.append(wordScore)
    newWordList.append(currentWord)

for i in range(len(newWordList)):
    wordScore = 0
    for letter in newWordList[i]:
        for value in letterFrequency:
            if letter == value[0]:
                wordScore += int(value[1:])

    wordScore = wordScore + newWordScores[i]
    while len(str(wordScore)) < 5:
        wordScore = str("0" + str(wordScore))

    wordScores.append(str(wordScore) + wordList[i])

wordScores.sort()
for word in wordScores:
    print(word[-5:] + ": " + word[:-5])
if len(wrongLetters) > 0:
    print("Incorrect Letters: " + wrongLetters)
if len(rightLetters) > 0:
    print("Correct Letters: " + rightLetters)
