
#Brill's Algorithm
"""
Q3: Brills Algorithm

 function TBL(corpus) :
    INTIALIZE-WITH-MOST-LIKELY-TAGS(corpus)
    until end condition is met  do
        template = (FromTag, ToTag, PreviousTag)
        best-transform =  GET-BEST-TRANSFORM(corpus, template)
        APPLY-TRANSFORM(best-transform, corpus)
        ENQUEUE(best-transform-rule, transforms-queue)
    end
    return(transforms-queue)
#———————————————————————————————
 function GET-BEST-TRANSFORM(corpus, templates):
    (instance, score) = GET-BEST-INSTANCE(corpus, template)
     if (score > best-transform.score)  then
        best-transform =  (instance, score)
 return(best-transform)

#———————————————————————————————

 procedure APPLY-TRANSFORM(transform, corpus):    #transform here is best-rule
    for pos   from 1  to corpus-size  do
        if (current-tag[pos]==best-rule[from]) and current-tag[pos-1]==best-rule[prev])):
            current-tag[pos] = best-rule[to]

#———————————————————————————————

 function GET-BEST-INSTANCE(corpus, template):
    for from-tag  from tag_1  to tag_n  do
        for to-tag  from tag_1  to tag_n  do
            for pos  from 1  to corpus-size  do
                if (correct-tag[pos] == to-tag and current-tag[pos] == from-tag)
                    num-good-transforms(current-tag[pos-1])++
                elseif (correct-tag[pos]==from-tag and current-tag[pos]==from-tag)
                    num-bad-transforms(current-tag[pos-1])++
            end
            best-Z = ARGMAXt (num-good-transforms(t) - num-bad-transforms(t))
            if(num-good-transforms(best-Z) - num-bad-transforms(best-Z)> best-instance.Z)  then
                best-instance “Change tag from from-tag to to-tag if previous tag is best-Z”
 return(best-instance)

#———————————————————————————————

"""

from collections import Counter
import pandas as pd
import time
CorpusFile = open("HW2_S18_NLP6320_POSTaggedTrainingSet-Unix.txt","r") #Corpus Input
CorpusData = CorpusFile.read() #Reading Corpus
CorpusWords =   CorpusData.split() #Splitting Into Tokens
TagsCounter = Counter()
AllTags = set()
WordTagCounter = Counter()
for word_tag in CorpusWords:
    word = word_tag.split("_")[0]
    tag = word_tag.split("_")[1]
    TagsCounter[tag] += 1
    if len(AllTags) < 50 and  tag not in AllTags:
        #print (tag,)
        AllTags.add(tag)
    if WordTagCounter[word] == 0:
        WordTagCounter[word] = Counter()
        WordTagCounter[word][tag] += 1
    else:
        WordTagCounter[word][tag] += 1
#for reference
#print (sorted(AllTags))
#print (WordTagCounter["is"])
#print (WordTagCounter["'s"].values())
TotalTags = sum(TagsCounter.values())
#Intialization :  i.e to tag with the most likely tag
#that is Stage 1
CorrectTags = []
CurrentTags = []
TotalWords = len(CorpusWords)
WrongWords = 0
for word_tag in CorpusWords:
    word = word_tag.split('_')[0]
    RealTag = word_tag.split('_')[1]
    for key in WordTagCounter[word]:
        if WordTagCounter[word][key] == max(WordTagCounter[word].values()):
            tag =  key
    if max(WordTagCounter[word].values()) == 0:
        tag = "NN"
    CorrectTags +=[(word,RealTag)]
    CurrentTags += [[word,tag]]
    if RealTag != tag:
        WrongWords += 1
        
#Intialized
#Rules (FROM_TAG, TO_TAG, PREVIOUS_WORD_TAG) = score
#Score : Correctly labeled instances in whole corpus - Incorrectly labeled instances in whole corpus
#print ("Intial Error Rate :",round(WrongWords/(0.01 * TotalWords),2),"%")

TrainFlag = False
TF = input("do you want to train Brills ? yes= 1 | no = 0:  ")
if TF.strip() == "0":
    print ("using the rules generated earlier, which are stored in FinalRules.txt")
else:
    TrainFlag = True
    print ("Training Selected")



RulesFlag = False
import os.path
if  (os.path.isfile("FinalRules.txt")):
    RulesFlag = True
if TrainFlag == True or RulesFlag == False:
    RulesCounter = Counter()
    start_time = time.clock()
    print ("Started Fetching Rules")
    count = 1
    PreviousWordTagsSet = {}
    for FromTag in AllTags:
        for ToTag in AllTags:
            if FromTag == ToTag:
                continue
            else:
                PreviousWordTagsSet[(FromTag,ToTag)] = dict((tag,0) for tag in AllTags)
                Score = 0
                for pos in range(1,len(CurrentTags)):
                        if (CorrectTags[pos][1] == ToTag and CurrentTags[pos][1] == FromTag):
                            PreviousWordTagsSet[(FromTag,ToTag)][CurrentTags[pos-1][1]] += 1
                        elif (CorrectTags[pos][1] == FromTag and CurrentTags[pos][1] == FromTag):
                            PreviousWordTagsSet[(FromTag,ToTag)][CurrentTags[pos-1][1]] -= 1
                for PreviousWordTag in PreviousWordTagsSet[(FromTag,ToTag)]:
                    if PreviousWordTagsSet[(FromTag,ToTag)][PreviousWordTag] > 0:
                        count += 1
                        Score = PreviousWordTagsSet[(FromTag,ToTag)][PreviousWordTag]
                        RulesCounter[(FromTag,ToTag,PreviousWordTag)] = Score
                        #print (FromTag,ToTag,PreviousWordTag,Score)
    print ("Time required to learn :" , round (time.clock() - start_time,2), "seconds")     
    FinalRules = (RulesCounter.most_common())
    print (FinalRules)
    RulesFile = open('FinalRules.txt', 'w')
    for item in FinalRules:
        RulesFile.write((item[0][0] +"," +item[0][1]  +"," + item[0][2]+ "," +str(item[1])+"\n"))
    RulesFile.close()
    #print (FinalRules)
else:
    RulesFile = (open('FinalRules.txt', 'r')).read().strip()
    RulesFile = RulesFile.split("\n")
    FinalRules = []
    #print (RulesFile)
    for each in RulesFile:
        rule = each.split(",")
        #print (rule[3])
        FinalRules +=[(tuple(rule[0:3]),rule[3])]
        
        
        
        
#Testing Phase
#input sentence
#Sentence = ("The_DT president_NN wants_VBZ to_TO control_VB the_DT board_NN 's_POS abhi_NN")
Sentence = input("Enter Testing Sentence with its Tags:\n").strip()

print("Given Sentence : \n",Sentence)
SentenceWordsTags = Sentence.split()


SentenceUnigramWords = []
SentenceBrillsWords = []
SentenceGoldenWords = []
SentenceBigramWords = []
for word_tag in SentenceWordsTags:
    word = word_tag.split('_')[0]
    RealTag = word_tag.split('_')[1]
    if WordTagCounter[word] == 0:
        WordTagCounter[word] =  Counter()
        WordTagCounter[word]["NN"] = 1 
    for key in WordTagCounter[word]:
        if WordTagCounter[word][key] == max(WordTagCounter[word].values()):
            tag =  key
    if max(WordTagCounter[word].values()) == 0:
        tag = "NN"
    SentenceUnigramWords += [[word.split("_")[0],tag]]
    SentenceBrillsWords += [[word.split("_")[0],tag]]
    SentenceGoldenWords += [[word.split("_")[0],RealTag]]
    SentenceBigramWords += [[word.split("_")[0],None]]


BrillsError = 0
Iterations = 0
BrillsErrorRate = 1
MaxErrorRate = 0.01


while BrillsErrorRate > MaxErrorRate and Iterations < 10:
    Iterations += 1
    for index in range(0,len(SentenceBrillsWords)-1):
        for Rule in FinalRules:
            if Rule[0][2] == SentenceBrillsWords[index][1]:
                if  Rule[0][0] == SentenceBrillsWords[index+1][1]:
                    SentenceBrillsWords[index+1][1] = Rule[0][1]
                    #print (SentenceBrillsWords[index+1])
                    break

UnigramError = 0
for index in range(0,len(SentenceGoldenWords)):
    if SentenceGoldenWords[index] != SentenceUnigramWords[index]:
        UnigramError += 1


"""while BrillsErrorRate > MaxErrorRate and Iterations < 10:
    Interations += 1"""
for index in range(0,len(SentenceGoldenWords)):
    if SentenceGoldenWords[index] != SentenceBrillsWords[index]:
        BrillsError += 1 
    BrillsErrorRate = round(BrillsError/(1.0 * len(SentenceGoldenWords)),2)



#Part B : Naive Bayes Bigram Model
#where we maximise the probabilities of tags for a given sentence
#TagsCounter #Counts of all tags in the given corpus
TagTagBigramCounter = Counter()
#WordTagCounter = we already defined as WordTagCounter[Word][Tag] = count
#TagTagBigramCounter = TagTagCounter[(t1,t2)]
for index in range(0,len(CorpusWords)-1):
    word_tag = CorpusWords[index]
    word = word_tag.split("_")[0]
    tag = word_tag.split("_")[1]
    word_tag_next = CorpusWords[index+1]
    word_next = word_tag_next.split("_")[0]
    tag_next = word_tag_next.split("_")[1]
    if word_tag is ("._."):
        continue
    else:
        TagTagBigramCounter[(tag,tag_next)] += 1

NoOfPosibbleProbabilities = 1
for  wordTag in SentenceBigramWords:
    TagsPossible = len(WordTagCounter[wordTag[0]])
    NoOfPosibbleProbabilities *= TagsPossible
NoOfPosibbleProbabilities
TotalPossiblityMatrix = [[None]*(len(SentenceBigramWords)+1)]*NoOfPosibbleProbabilities
TotalPossiblityMatrix = [0] *  NoOfPosibbleProbabilities
for i in range(NoOfPosibbleProbabilities):
    TotalPossiblityMatrix[i] = [None] * (len(SentenceBigramWords)+1)
    
#print(TotalPossiblityMatrix)
frequency = NoOfPosibbleProbabilities
for indexI in range(0,len(SentenceBigramWords)):
    wordTag = SentenceBigramWords[indexI]
    NoOfTagsPossible = len(WordTagCounter[wordTag[0]])
    EachTagRepeatition = NoOfPosibbleProbabilities/NoOfTagsPossible
    cycles = 1
    if NoOfTagsPossible > 1:
        frequency = frequency/NoOfTagsPossible
        Freq = frequency
        cycles = NoOfPosibbleProbabilities/(Freq*NoOfTagsPossible)
    else :
        Freq = NoOfPosibbleProbabilities
    #print(EachTagRepeatition,Freq,cycles)
    indexJ = 0
    for cycle in range(0,int(cycles)):
        indexJ = 0
        for tag in WordTagCounter[wordTag[0]]:
            for freqCount in range(0,int(Freq)):
                #print("indexJ:",indexJ,"cycle:",cycle,"Freq:",Freq,indexJ + cycle*int(Freq*NoOfTagsPossible),tag)
                J = indexJ + cycle*int(Freq*NoOfTagsPossible)
                TotalPossiblityMatrix[J][indexI] = tag
                indexJ += 1
#print (TotalPossiblityMatrix)
#Store Probabilities in TotalPossiblityMatrix[:][-1]

for each in range(0,len(TotalPossiblityMatrix)):
    CountsOfWord_Tag = WordTagCounter[SentenceBigramWords[0][0]][TotalPossiblityMatrix[each][0]]
    CountsOfTag = TagsCounter[TotalPossiblityMatrix[each][0]]
    probabilityOfWordGivenTag = CountsOfWord_Tag/CountsOfTag
    TotalPossiblityMatrix[each][-1]= probabilityOfWordGivenTag
#print (TotalPossiblityMatrix)


for wordIndex in range(1,len(SentenceBigramWords)):
    wordN_1 = SentenceBigramWords[wordIndex-1][0]
    wordN = SentenceBigramWords[wordIndex][0]
    #print (wordN_1,wordN)
    for IndexJ in range(0,len(TotalPossiblityMatrix)):

        
        #for present word
        tagN = TotalPossiblityMatrix[IndexJ][wordIndex]
        CountsOfWord_Tag = WordTagCounter[wordN][tagN]
        CountsOfTagN = TagsCounter[tagN]
        probabilityOfWordGivenTag = CountsOfWord_Tag/CountsOfTagN
        
        #for previous word
        tagN_1 = TotalPossiblityMatrix[IndexJ][wordIndex-1]
        CountsofTag_Tag = TagTagBigramCounter[(tagN_1,tagN)]
        CountsOfTagN_1 = TagsCounter[tagN_1]
        probabilityOftagN_GivenTagN_1 = CountsofTag_Tag/CountsOfTagN_1
        
        P = (probabilityOfWordGivenTag*probabilityOftagN_GivenTagN_1)

        TotalPossiblityMatrix[IndexJ][-1] *= P
        #print (TotalPossiblityMatrix[IndexJ][-1],IndexJ)
#print (TotalPossiblityMatrix)
ResultRowIndex = 0
ResultProbability = 0
for index in range(0,len(TotalPossiblityMatrix)):
    if ResultProbability < TotalPossiblityMatrix[index][-1]:
        ResultProbability = TotalPossiblityMatrix[index][-1]
        ResultRowIndex = index
ResultRowTags = TotalPossiblityMatrix[ResultRowIndex][:-1]
#print (ResultRowTags)
BigramErrorCounts = 0
for index in range(0,len(SentenceBigramWords)):
    SentenceBigramWords[index][1] =  ResultRowTags[index]
    if ResultRowTags[index] != SentenceGoldenWords[index][1]:
        BigramErrorCounts += 1
#SentenceBigramWords
#print (SentenceBigramWords)
#print (BigramErrorCounts) 

print ("Unigram")
print (SentenceUnigramWords)

print ("\nBrills")
print (SentenceBrillsWords)

print ("\nBigram")
print (SentenceBigramWords)

print ("\nManual Tagging")
print (SentenceGoldenWords)
print ("\nTotal Words in the given Sentence:",len(SentenceGoldenWords))
print ("\nUnigram Errors for given Sentence =",UnigramError," & Error Rate =",round(UnigramError/(0.01 * len(SentenceGoldenWords)),2),"%")
print ("\nBrill's Errors for given Sentence =",BrillsError," & Error Rate =",round(BrillsError/(0.01 * len(SentenceGoldenWords)),2),"%")
print ("\nBigram's Errors for given Sentence =",BigramErrorCounts," & Error Rate =",round(BigramErrorCounts/(0.01 * len(SentenceGoldenWords)),2),"%")



