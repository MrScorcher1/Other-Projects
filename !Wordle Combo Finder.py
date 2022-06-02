file = open("WordleList.txt", "r")
wordList, letterFrequency = file.read().split("\n\n")
wordScore = 0
totalScore = 0
currentScore = 0
wordScores = []
newWordList = []
newWordScores = []
combos = []
delete = []
comboScores = []
wordList = wordList.split("\n")
letterFrequency = [line.replace("\t", "") for line in letterFrequency.split("\n")]
usedLetters = input("Enter a 5 Letter Word: ")
while usedLetters not in wordList:
    usedLetters = input("Not a Valid Word! Please Try Again: ")

skip = False
goodWordList = wordList.copy()
for word in wordList:
    wordScore = 0
    for letter in word:
        if word.count(letter) > 1:
            skip = True
        elif letter in usedLetters:
            skip = True
        else:
            for value in letterFrequency:
                if letter == value[0]:
                    wordScore += int(value[1:])

    if skip:
        del goodWordList[goodWordList.index(word)]
        skip = False
        continue

    wordScores.append(str(wordScore) + word)

wordScores.sort(reverse=True)
# wordScores = wordScores[:1000]
newWordScores = wordScores.copy()
# print(wordScores)
for i, word in enumerate(wordScores):
    if sorted(wordScores[i-1][4:]) == sorted(wordScores[i][4:]):
        del newWordScores[newWordScores.index(word)]
        continue

print(len(newWordScores))
goodWordList = []
# print(newWordScores)
originalWordScores = newWordScores.copy()
firstWordScores = newWordScores.copy()
secondWordScores = []
for word in newWordScores:
    goodWordList.append(word[-5:])
# print(goodWordList)
while True:
    while newWordScores:
        wordScores = []
        usedLetters += newWordScores[0][4:]
        print(usedLetters)

        if len(usedLetters) == 10:
            firstWordScores.pop(0)
        elif len(usedLetters) == 15:
            secondWordScores.pop(0)

        for word in goodWordList:
            wordScore = 0
            for letter in word:
                if letter in usedLetters:
                    skip = True
                    continue
                for value in letterFrequency:
                    if letter == value[0]:
                        wordScore += int(value[1:])

            if skip:
                goodWordList.remove(word)
                skip = False
                continue

            wordScores.append(str(wordScore) + word)

        # print(wordScores)
        newWordScores = wordScores.copy()
        goodWordList = []
        if len(usedLetters) == 10:
            secondWordScores = newWordScores.copy()
        # print(secondWordScores)
            for word in originalWordScores:
                goodWordList.append(word[-5:])
        elif len(usedLetters) == 15:
            for word in secondWordScores:
                goodWordList.append(word[-5:])

    else:
        if len(usedLetters) == 10:
            newWordScores = firstWordScores.copy()
        elif len(usedLetters) == 15:
            newWordScores = secondWordScores.copy()
        else:
            for letter in usedLetters:
                for value in letterFrequency:
                    if letter == value[0]:
                        totalScore += int(value[1:])

            combos.append(str(totalScore) + usedLetters)
            totalScore = 0
        usedLetters = usedLetters.replace(usedLetters[-5:], "")
        # print(len(usedLetters))

        for word in newWordScores:
            goodWordList.append(word[-5:])

        if len(firstWordScores) == 0 and len(secondWordScores) == 0:
            for i in range(len(combos)):
                while len(combos[i]) < 25:
                    combos[i] = "0" + combos[i]
                comboScore = combos[i][:-20]
                comboLetters = combos[i][-20:]
                for letter in combos[i]:
                    if combos[i].index(letter) % 5 == 0 and combos[i].index(letter) > 0:
                        comboScores.append(currentScore)
                        currentScore = 0
                    for value in letterFrequency:
                        if letter == value[0]:
                            currentScore += int(value[1:])
                comboScores.append(currentScore)
                combos[i] = comboScore + str(sorted(comboScores[-4:], reverse=True)) + comboLetters
                # print(combos[i])
                currentScore = 0
                # print(combos)

            combos.sort(reverse=True)
            comboScores = []

            for i in range(len(combos)):
                comboLetters = combos[i][-20:]
                comboScore = combos[i][:5]
                comboLetters = ", ".join(comboLetters[j:j + 5] for j in range(0, len(comboLetters), 5))
                for letter in (comboLetters.replace(",", "") + " "):
                    if letter == " ":
                        comboScores.append(currentScore)
                        currentScore = 0
                    else:
                        for value in letterFrequency:
                            if letter == value[0]:
                                currentScore += int(value[1:])
                combos[i] = comboLetters + ": " + comboScore + " " + ("(" + str(comboScores[4*i:4*i+4])[1:-1] + ")")
                if sorted(combos[i-1]) == sorted(combos[i]) and i > 0 and combos[i] not in delete:
                    delete.append(combos[i])

            for word in delete:
                del combos[combos.index(word)]

            print(combos)
            break

# for word in newWordScores:
#     print(word[-5:] + ": " + word[:-5])
