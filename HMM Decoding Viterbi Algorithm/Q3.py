import sys
def Viterbi_Algorithm(ObservedSequences):
    #HMM Declaration
    b = {(1,"H") : 0.2,
          (2,"H") : 0.4,
          (3,"H") : 0.4,
          (1,"C") : 0.5,
          (2,"C") : 0.4,
          (3,"C") : 0.1}

    a = {("S","H"):0.8,("S","C"):0.2,
                  ("H","H"): 0.7,("H","C"): 0.3,
                  ("C","H"): 0.4,("C","C"): 0.6}

    States = {"H","C"}
    #Viterbi #Decoding
    #initialisation


    v = []
    backPointer = [{},{}]
    for i in range(0,len(ObservedSequences)+1):
        v += [[]]
        v[i] = {}
        for j in States:
            v[i][j] = 1

    for j in States:
        backPointer[1][j] = "S"
        o1 = (int(ObservedSequences[0]))
        v[1][j] = a[("S",j)]* b[(o1,j)]
    #print ("v = ",v,"bP-",backPointer)
    for i in range(2,len(ObservedSequences)+1):
        t = int(ObservedSequences[i-1])
        #print (i-1,t)
        backPointer += [{}]
        for s in States:
            v[i][s] = 0
            temp = 0
            st = ""

            for s1 in States:
                v[i][s] = max(v[i][s],v[i-1][s1]*a[(s1,s)]*b[(t,s)])
                if temp <= v[i-1][s1]*a[(s1,s)]:
                    temp = v[i-1][s1]*a[(s1,s)]
                    st = s1
            backPointer[i][s] = st    
    backPointer += [{}] #final state
    v += [[]]
    v[len(ObservedSequences)+1] = {}
    v[len(ObservedSequences)+1]["E"] = 0
    temp = 0
    #print (backPointer,"\n\n")
    backPointer[len(ObservedSequences)+1]["E"] = ""
    #print (backPointer,"\n\n")
    for s in States:
        v[len(ObservedSequences)+1]["E"] = max(v[len(ObservedSequences)+1]["E"],v[len(ObservedSequences)][s])
        if temp <= v[len(ObservedSequences)][s]:
            backPointer[len(ObservedSequences)+1]["E"] = s
            temp = v[len(ObservedSequences)][s]

    HiddenSequences = []
    for i in range(0,len(ObservedSequences)):
        HiddenSequences += [""]
    st = backPointer[len(backPointer)-1]["E"] 
    HiddenSequences[-1] = st
    for index in range(len(backPointer)-2,1,-1):
        HiddenSequences[index-2] = backPointer[index][st]
        st = backPointer[index][st]
    #print ("".join(HiddenSequences),v[len(ObservedSequences)+1]["E"])
    return "".join(HiddenSequences),v[len(ObservedSequences)+1]["E"] 




#Question3 
ObservedSequenceList = input("Enter Sequence:").split()#["331","122313","331123312","313","333"]
for s in ObservedSequenceList:
    HS , p = Viterbi_Algorithm(s)
    print ("Observed Sequence:",s,", Hidden Sequence:",HS,", probability:",p)