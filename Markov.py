from konlpy.tag import Twitter; tw = Twitter()
from random import randint
import os
region = ["서울","부산","기장","대구","달성","인천","강화","옹진","광주","대전",
 "울산","울주","세종","수원","성남","안양","안산","용인","광명","평택",
 "과천","오산","시흥","군포","의왕","하남","이천","안성","김포","화성",
 "경기도_광주","여주","부천","양평","고양","의정부","동두천","구리","남양주",
 "파주","양주","포천","연천","가평","춘천","원주","강릉","동해","태백",
 "속초","삼척","홍천","횡성","영월","평창","정선","철원","화천","양구",
 "인제","강원도_고성","양양","청주","충주","제천","보은","옥천","영동","진천",
 "괴산","음성","단양","증평","천안","공주","보령","아산","서산","논산",
 "계룡","당진","금산","부여","서천","청양","홍성","예산","태안",'전주',
 '군산','익산','정읍','남원','김제','완주','진안','무주','장수','임실',
 '순창','고창','부안','목포','여수','순천','나주','광양','담양','곡성',
 '구례','고흥','보성','화순','장흥','강진','해남','영암','무안','함평',
 '영광','장성','완도','진도','신안','창원','진주','통영','사천','김해',
 '밀양','거제','양산','의령','함안','창녕','경상도_고성','남해','하동','산청',
 '함양','거창','합천','포항','경주','김천','안동','구미','영주','영천',
 '상주','문경','경산','군위','의성','청송','영양','영덕','청도','고령',
 '성주','칠곡','예천','봉화','울진','울릉','제주']
def wordListSum(wordList):
    sum = 0
    for word, value in wordList.items():
        sum += value
    return sum

def retrieveRandomWord(wordList):
    randIndex = randint(1,wordListSum(wordList))
    for word, value in wordList.items():
        randIndex -= value
        if randIndex <= 0:
            return word

def buildWordDict(text):
    text = text.replace("\n"," ")
    text = text.replace("\\"," ")
    punctuation = [',','.',';',':','[',']',"'"]
    for symbol in punctuation:
        text = text.replace(symbol, " ")

    words = text.split(" ")
    words = [word for word in words if word !=""]
    wordDict = {}
    list = []

    for i in range(1, len(words)):
        if words[i-1] not in wordDict:
            wordDict[words[i-1]] = {}
        if words[i] not in wordDict[words[i-1]]:
            wordDict[words[i-1]][words[i]] = 0
        wordDict[words[i-1]][words[i]] = wordDict[words[i-1]][words[i]] + 1
    for i in wordDict.keys():
        for j in wordDict[i]:
            if wordDict[i][j] >= 3: #빈도 수 결정하는 곳
                list.append((i+" "+j,wordDict[i][j]))
    return sorted(list)

def main(region):
    text = open(os.path.join("local_phrase", "%s_phrase.txt" % region), encoding='utf8').read()
    write_file = os.path.join("local_worddict", "%s_worddict.txt" % region)
    write_file = open(write_file, "w", encoding='utf8')
    text = str(tw.nouns(text))
    write_file.write(str(buildWordDict(text)))

os.makedirs("local_worddict")
for i in region:
    main(i)