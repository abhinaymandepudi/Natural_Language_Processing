from nltk.corpus import wordnet
from nltk.tokenize import RegexpTokenizer
import sys

def simplifiedLesk( word, sentence ):
    final = None
    maxoverlap = 0
    word=wordnet.morphy(word)

    print("Total senses are")
    print("------------------------")

    senses = wordnet.synsets(word)
    print(senses)
    for sense in senses:
        print (sense)
        overlap = computerOverlap(sense,sentence)
        for hyponyms in sense.hyponyms():
            overlap += computerOverlap( hyponyms, sentence )

        if overlap > maxoverlap:
                maxoverlap = overlap
                final = sense
        print (overlap)
    print ("--------------------------------")
    print("\nFinal Chosen Sense")
    return final

def computerOverlap( synset, sentence ):
    x=synset.definition()
    gloss = set(tokenizer.tokenize(x))
    for example in synset.examples():
         gloss=gloss.union(example)
    gloss = gloss.difference( stop_words )

    sentence = set(sentence.split(" "))
    sentence = sentence.difference( stop_words )
    gloss=gloss.intersection(sentence)
    return len( gloss )

tokenizer = RegexpTokenizer(r'\w+')
stop_words = set(line.strip() for line in open('stopwords.txt'))


def main():
    sentence = input("Enter Sentence :")
    word = input("Enter word :")

    lesk = simplifiedLesk(word,sentence)
    print (lesk)
    if lesk is not None:
        print ("Definition: ",lesk.definition())
        example=0
        print ("\nExamples:")
        for i in lesk.examples():
            example=example+1
            print (str(example)+'.',i)

if __name__=='__main__':
    main()