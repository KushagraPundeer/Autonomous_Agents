__author__ = 'kush'
import random
from collections import defaultdict
from collections import Counter
import itertools
import operator

class VotingMachine:
    number_of_voters = 100
    ballotBox = {}
    candidatesPoints = {}

    def performVotingPreference(self):
        voterCount = self.number_of_voters
        for voters in range(1, voterCount+1):
            candidatesPreferenceList = []
            remainingCandidates = range(1, self.number_of_voters+1)
            while len(remainingCandidates) > 0:
                myVote = random.choice(remainingCandidates)
                remainingCandidates.remove(myVote)
                candidatesPreferenceList.append(myVote)
            self.ballotBox[voters] = candidatesPreferenceList
        return self.ballotBox

    def pluralityChoice(self):
        bBox = self.ballotBox
        firstChoiceList = []
        for key, value in bBox.iteritems():
            firstChoiceList.append(value[0])
        d = defaultdict(int)
        for i in firstChoiceList:
            d[i] += 1
        result = max(d.iteritems(), key=lambda x: x[1])
        choosenNumb = result[0]
        numbFreq = result[1]
        return choosenNumb

    def bordaChoice(self):
        bBox = self.ballotBox
        toElect = 1
        electors = range(1, self.number_of_voters+1)
        eCandidate=self.newElectCandidates(electors, bBox, toElect)
        electedCandidate = eCandidate[0]
        return electedCandidate

    def analyzeVotes_PE(self):
        li = list(set(e for e in itertools.combinations(xrange(1, self.number_of_voters+1), 2)))
        candidateScores = {}
        for k in range(1, self.number_of_voters+1):
            candidateScores[k]=0
        numberOfPairs = len(li)
        bBox=self.ballotBox


        for i in range(0,numberOfPairs):
            thisPair=li[i]
            firstElement=thisPair[0]
            secondElement=thisPair[1]
            firstElement_score=0
            secondElement_score=0
            for key, value in bBox.iteritems():
                i_firstElelment = value.index(firstElement)
                i_secondElelment = value.index(secondElement)
                if (i_firstElelment > i_secondElelment):
                    firstElement_score=firstElement_score+1
                else:
                    secondElement_score=secondElement_score+1
            if (firstElement_score > secondElement_score):
                candidateScores[firstElement]=candidateScores[firstElement]+1
            elif (firstElement_score < secondElement_score):
                candidateScores[secondElement]=candidateScores[secondElement]+1
            else:
                candidateScores[firstElement]=candidateScores[firstElement]+0.5
                candidateScores[secondElement]=candidateScores[secondElement]+0.5

        sortedScores = sorted(candidateScores.items(), key=operator.itemgetter(1), reverse=True)
        winner=sortedScores[0][0]
        return winner


    def choiceByLot(self, listParent, toReduce):
        prevCollege = listParent
        sizeCollege = len(prevCollege)
        nextCollege = []
        for i in range(0, toReduce):
            pos = random.randrange( len(prevCollege) )
            element = prevCollege[pos]
            prevCollege[pos]=prevCollege[-1]
            del prevCollege[-1]
            nextCollege.append(element)
        return nextCollege

    def createNewBox(self, lisElectors, lisCandidates):
        bBox = self.ballotBox
        newBallotBox = {}
        lstElectors = lisElectors
        lstCandidates = lisCandidates

        for k in range(0,len(lstElectors)):
            elector = lstElectors[k]
            elChoiceList_inbBox = bBox[elector]
            newBallotBox[elector]=elChoiceList_inbBox

        return newBallotBox

    def extractElected(self, electedScores):
        thisList=electedScores
        electedList = []
        for k in range(0,len(thisList)):
            #print k
            thisListValue=thisList[k]
            candidate = int(thisListValue.split(":",1)[0])
            electedList.append(candidate)
        return electedList

    def newElectCandidates(self, lisElectors, neoBox, seats):
        lstElectors = lisElectors
        newBox=neoBox
        nSeats=seats
        listOfCandidates = list(newBox.values()[0])
        lenCandidates = len(listOfCandidates)
        candidateScores = {}

        for c in listOfCandidates:
            calcScore = 0
            prefValues = []

            for k in range(0,len(lstElectors)):
                elector = lstElectors[k]
                newList=list(newBox.values()[k])
                prefIndex=newList.index(c)
                thisScore=lenCandidates-(prefIndex+1)
                calcScore = calcScore + thisScore

            candidateScores[c]=calcScore

        electedList_Scores=[]
        for key, value in sorted(candidateScores.iteritems(), key=lambda (k,v): (v,k), reverse=True):
            kvpair = "%s: %s" % (key, value)
            electedList_Scores.append(kvpair)
        lenElectedList=len(electedList_Scores)

        approvedList=[]
        aprDict= {}
        newElectedList = self.extractElected(electedList_Scores)
        for i in range(0,lenElectedList):
            thisCandidate=newElectedList[i]
            appr=self.approveCandidate(lstElectors, thisCandidate)
            aprDict[thisCandidate]=appr

        sortedAprList = sorted(aprDict.items(), key=operator.itemgetter(1), reverse=True)
        check=sortedAprList[nSeats][1]
        for i in range(0, nSeats):
            elementList= sortedAprList[i][0]
            approvedList.append(elementList)
        return approvedList, check


    def approveCandidate(self, college, candidate):
        bBox=self.ballotBox
        thisScore = 0
        for i in range(0,len(college)):
            elector=college[i]
            electorsChoice = bBox[elector]
            prefIndex=electorsChoice.index(candidate)
            if (prefIndex < 50):
                thisScore = thisScore+1
            else:
                thisScore = thisScore

        approvalScore=thisScore
        return approvalScore


    def voteForDoge(self):
        myAgents=self.number_of_voters
        myAgentsList=range(1, myAgents+1)

        #------------------------100 to 30 by Lot
        nxtCollege = self.choiceByLot(myAgentsList, 30)
        #print "30-byLot:", nxtCollege

        #------------------------Reduce 30 to 9 by lot
        prvCollege = nxtCollege
        nxtCollege = self.choiceByLot(prvCollege, 9)
        #print "30->9-byLot:", nxtCollege

        #------------------------9 choose 40 by election
        prvCollege = nxtCollege
        numberOfSeats=40
        approvalRequired=7
        newBalBox=self.createNewBox(prvCollege, myAgentsList)
        retValues=self.newElectCandidates(prvCollege, newBalBox, numberOfSeats)
        nxtCollege=retValues[0]
        #print "List(9-choose-40-outof-100):", nxtCollege



        #------------------------Reduce 40 to 12 by lot
        prvCollege = nxtCollege
        nxtCollege = self.choiceByLot(prvCollege, 12)
        #print "40->12-byLot:", nxtCollege

        #------------------------12 choose 25 by election
        prvCollege = nxtCollege
        numberOfSeats=25
        approvalRequired=9
        newBalBox=self.createNewBox(prvCollege, myAgentsList)
        retValues=self.newElectCandidates(prvCollege, newBalBox, numberOfSeats)
        nxtCollege=retValues[0]
        #print "List(12-choose-25-outof-100):", nxtCollege

        #------------------------Reduce 25 to 9 by lot
        prvCollege = nxtCollege
        nxtCollege = self.choiceByLot(prvCollege, 9)
        #print "25->9-byLot:", nxtCollege

        #------------------------9 choose 45 by election
        prvCollege = nxtCollege
        numberOfSeats=45
        approvalRequired=7
        newBalBox=self.createNewBox(prvCollege, myAgentsList)
        retValues=self.newElectCandidates(prvCollege, newBalBox, numberOfSeats)
        nxtCollege=retValues[0]
        #print "List(9-choose-45-outof-100):", nxtCollege

        #------------------------Reduce 45 to 11 by lot
        prvCollege = nxtCollege
        nxtCollege = self.choiceByLot(prvCollege, 11)
        #print "45->11-byLot:", nxtCollege

        #------------------------11 choose 41 by election
        prvCollege = nxtCollege
        numberOfSeats=41
        approvalRequired=9
        newBalBox=self.createNewBox(prvCollege, myAgentsList)
        retValues=self.newElectCandidates(prvCollege, newBalBox, numberOfSeats)
        nxtCollege=retValues[0]
        #print "List(11-choose-41-outof-100):", nxtCollege

        #------------------------41 choose the Doge
        prvCollege = nxtCollege
        numberOfSeats=1
        approvalRequired=25
        newBalBox=self.createNewBox(prvCollege, myAgentsList)
        retValues=self.newElectCandidates(prvCollege, newBalBox, numberOfSeats)
        nxtCollege=retValues[0]
        electedDoge = nxtCollege[0]
        approvedBy = retValues[1]

        return electedDoge, approvedBy

if __name__ == "__main__":
    myCode = VotingMachine()
    print "-------------------------------------------------------------"
    print "--Runs--Plurality-----Borda------Pair-------Doge---"
    print "-------------------------------------------------------------"

    for k in range(0,5):
        myCode.performVotingPreference()
        cPlu = myCode.pluralityChoice()
        cBorda = myCode.bordaChoice()
        cPE=myCode.analyzeVotes_PE()
        cDoge = myCode.voteForDoge()
        print "--",k+1,"-----",cPlu,"------",cBorda[0],"--------",cPE,"----------",cDoge[0],"(aproved by:", cDoge[1],")"
        print "------------------------------------------------------------------"






