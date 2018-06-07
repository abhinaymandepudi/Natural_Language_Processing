from collections import Counter
import pandas as pd
import sys
def BigramProbabilityCalc(BigramCounter,UnigramCounter,SentenceWords,TotalTokens,SmoothFlag):
    if(SmoothFlag == 1):
        smooth = 1
        V = len(UnigramCounter)
    else:
        smooth = 0
        V = 0
    TotalProbability = 1 
    SentenceBigramCounts = []
    BigramProbability = []
    for index in range(0,len(SentenceWords)- 1):
        if (1.0 * V + UnigramCounter[SentenceWords[index]]) != 0:
            SentenceBigramCounts += [((BigramCounter[(SentenceWords[index],SentenceWords[index+1])] + smooth)*UnigramCounter[SentenceWords[index]])/(1.0 * V + UnigramCounter[SentenceWords[index]])]
        else:
            SentenceBigramCounts +=[0.0]
        if (UnigramCounter[SentenceWords[index]] +  1.0 * V) != 0:
            BigramProbability += \
            [(BigramCounter[(SentenceWords[index],SentenceWords[index+1])] + smooth)/(1.0 * V + UnigramCounter[SentenceWords[index]])]
            TotalProbability *= (BigramCounter[(SentenceWords[index],SentenceWords[index+1])] + smooth)/(1.0 * V + UnigramCounter[SentenceWords[index]])
        else:
            BigramProbability += [0]
            TotalProbability *= 0
    return (TotalProbability,SentenceBigramCounts,BigramProbability)

def GoodTuringSmoothing(BigramCounter,UnigramCounter,SentenceWords,TotalTokens):
    NormalCounts = Counter()
    GoodTuringCounts = Counter()
    TotalBigrams = sum(BigramCounter.values())
    N0 = TotalTypes * TotalTypes - len(BigramCounter)
    for word in BigramCounter:
        NormalCounts[BigramCounter[word]] += 1
    #print (NormalCounts.most_common())
    for i in NormalCounts:
        if NormalCounts[i] != 0:
            GoodTuringCounts[i] = (i + 1) * (NormalCounts[i+1]/(1.0 * NormalCounts[i]))
    GoodTuringCounts[0] = (NormalCounts[1]/N0)
    TotalProbability = 1 
    SentenceBigramCounts = []
    BigramProbability = []
    for index in range(0,len(SentenceWords)- 1):
        SentenceBigramCounts += [GoodTuringCounts[BigramCounter[(SentenceWords[index],SentenceWords[index+1])]]]
        if UnigramCounter[SentenceWords[index]] != 0:
            BigramProbability += \
            [GoodTuringCounts[(BigramCounter[(SentenceWords[index],SentenceWords[index+1])] )]/( UnigramCounter[SentenceWords[index]])]
            TotalProbability *= (GoodTuringCounts[BigramCounter[(SentenceWords[index],SentenceWords[index+1])] ])/( UnigramCounter[SentenceWords[index]])
        else:
            BigramProbability += [0]
            TotalProbability *= 0
    return TotalProbability, SentenceBigramCounts,BigramProbability
def Question2(Sentence,UnigramCounter,TotalTokens):
    SentenceWords = Sentence.split()
    #For a given input written sentence:
    #a. For each of the three scenarios, construct a table with the bigram counts for the sentence.
    #b. For each of the three scenarios, construct a table with the bigram probabilities for the sentence.
    #c. For each of the three scenarios, compute the total probability for the sentence
    SentenceBigrams = []
    SentenceBigramCounts = [[],[],[]]
    BigramProbability = [[],[],[]]
    TotalProbability = [1,1,1]
    for index in range(0,len(SentenceWords)-1):
        SentenceBigrams +=[(SentenceWords[index],SentenceWords[index+1])]
    #Without Any Smoothing
    TotalProbability[0], SentenceBigramCounts[0],BigramProbability[0]  = BigramProbabilityCalc(BigramCounter,UnigramCounter,SentenceWords,TotalTokens,0)
    #With One-Smoothing
    TotalProbability[1], SentenceBigramCounts[1],BigramProbability[1] = BigramProbabilityCalc(BigramCounter,UnigramCounter,SentenceWords,TotalTokens,1)
    #Good Turing C* Calculation
    TotalProbability[2], SentenceBigramCounts[2],BigramProbability[2] = GoodTuringSmoothing(BigramCounter,UnigramCounter,SentenceWords,TotalTokens)


    Method = ["No Smoothing","Add One Smoothing","Good Turing"]
    dfBigramCounts = pd.DataFrame(columns=["Method"]+SentenceBigrams)
    dfBigramProbability = pd.DataFrame(columns=["Method"]+SentenceBigrams)
    dfTotalProbability = pd.DataFrame(columns=Method)

    for i in range(0,3):
        dfBigramCounts.loc[i] = [Method[i]] + SentenceBigramCounts[i]
        dfBigramProbability.loc[i] = [Method[i]] + BigramProbability[i]
    dfTotalProbability.loc[0] = TotalProbability
    print("Given Sentence :\"",Sentence,"\"")
    print("\nBigram Counts")
    print (dfBigramCounts)
    print ("\nBigram Probabilities")
    print (dfBigramProbability)
    print ("\nTotal Probabilities")
    print(dfTotalProbability)
    print ("\n\nNote: when the bigram counts are high, due to missing buckets probabilities of them can become zero\n as professor suggested not to modify basic Good Turing")
    
        
    
CorpusFile = open("HW2_S18_NLP6320-NLPCorpusTreebank2Parts-CorpusA-Unix.txt","r") #Corpus Input
CorpusData = CorpusFile.read() #Reading Corpus
CorpusWords =   CorpusData.split() #Splitting Into Tokens
UnigramCounter = Counter() #Counter For Each Type
BigramCounter = Counter() #Counter For Each Bigram,Unigram
for index in range(0,(len(CorpusWords) - 1),1): #Generating Unigrams and Bigrams
    UnigramCounter[CorpusWords[index]] += 1        # 
    BigramCounter[(CorpusWords[index],CorpusWords[index+1])] += 1
UnigramCounter[CorpusWords[index]] += 1

TotalTokens = sum(UnigramCounter.values()) #Total Words in the Corpus #TokenSize
TotalTypes = len(UnigramCounter) #Total Different Words in the Corpus #TotalTypes
TotalBigrams = sum(BigramCounter.values())
#print (TotalTypes,TotalTokens,TotalBigrams)

TestSentence = input("Enter Testing Sentence.   :").strip()
Question2(TestSentence,UnigramCounter,TotalTokens)
