#!/bin/python
import math
import random
import sys
import string
import bisect
import itertools
import time
alpha = 1.0
beta = 12
decayRate = 0.35
gt=0
#filename = sys.argv[1]
#time_sto = int(sys.argv[2])

filename = 'ar9152.tsp'
time_sto = 5000


allAntsTour={}
numbAnts=10
iterMinDist=0
iterMinPath=[]
globalFirst=1

class ACO:
    antsCount=numbAnts

    def __init__(self, filename):
        lines = open(filename, 'r').readlines()
        while lines[0][0] not in string.digits:
            lines.pop(0)
            size = len(lines)
            self.Cities = {}
            for l in lines:
                try :
                    c_id, x, y = l.strip().split()
                    c_id = int(c_id)
                    x = float(x)
                    y = float(y)
                    if (x,y) not in self.Cities.values():
                        self.Cities[c_id]= (x, y)
                except :
                    pass
        self.totCities=len(self.Cities)
        self.base_pherom = 1.0/self.totCities
        self.pheromones = dict((e, 1) for e in itertools.permutations(self.Cities.keys(), 2))
        self.globalMinDist=0
        self.globalMinPath=[]
        self.globalFirst=globalFirst

    def EuDist(self, cityFrom, cityTo):
        coordCity1=self.Cities[cityFrom]
        coordCity2=self.Cities[cityTo]
        xi = coordCity1[0]
        xj = coordCity2[0]
        yi = coordCity1[1]
        yj = coordCity2[1]
        intercityDistance = math.sqrt(math.pow(abs(xj-xi),2)+ math.pow(abs(yj-yi),2))
        return intercityDistance

    def placeAntsRandomly(self, numbAnts, numbCities):
        noAnts=numbAnts
        noCities=numbCities
        self.antsDict = {k: [] for k in range(noAnts)}
        for m in self.antsDict:
            self.antsDict[m]=random.choice(self.Cities.keys())
        self.antsPositions=self.antsDict
        self.antsPosit=self.antsPositions
        return self.antsPositions

    def weighted_probability_selection(self, selection):
        (values, weights) = zip(*selection)
        total = 0
        Weight_cumulative = []
        for w in weights:
            total = total + w
            Weight_cumulative.append(total)
        x = random.random()*total
        i = bisect.bisect(Weight_cumulative, x)
        return values[i]

    def decayPheromones(self,MIN_DISTA):
        self.pheromones.update((x, (y*(1-decayRate))+decayRate*(1/MIN_DISTA)) for x, y in self.pheromones.items())

    def moveAnts(self):
        self.visitedCities=set()
        self.remainedCities=set()
        allShortestDist=[]
        prevAntTour=[]
        prevAntDist=0
        first=1
        antPos=self.placeAntsRandomly(numbAnts, self.totCities)

        for ants in range(0, self.antsCount):
            self.visitedCities=set()
            self.remainedCities=set()
            antID=ants
            position=antPos[ants]
            thisAntTour=[]
            thisAntDist=[]

            self.visitedCities.add(position)
            self.remainingCities=set(self.Cities.keys()).difference((self.visitedCities))
            self.visitedList = list(self.visitedCities)
            self.remainingList = list(self.remainingCities)
            for city in self.remainingList:
                thisAntTour.append(position)
                self.visitedCities.add(position)
                self.remainingCities=set(self.Cities.keys()).difference((self.visitedCities))
                self.visitedList = list(self.visitedCities)
                self.remainingList = list(self.remainingCities)
                self.edges = zip(self.visitedList*len(self.remainingList),self.remainingList)

                self.distances = dict((e, self.EuDist(*e)) for e in self.edges)
                d=0
                for city in self.remainingList:
                    incityDis=self.EuDist(position,city)
                    edgePherom=self.pheromones[position,city]
                    d=d+math.pow(edgePherom, alpha)* math.pow((1.0 / incityDis),beta)
                p={}
                for city in self.remainingList:
                    incityDis=self.EuDist(position,city)
                    p[city]=math.pow(edgePherom, alpha)* math.pow((1.0 / incityDis),beta) / d
                initPosition=position
                nextPosition=self.weighted_probability_selection((e, p) for (e, p) in p.iteritems())
                distanceBetween=self.EuDist(initPosition,nextPosition)
                self.pheromones[initPosition,nextPosition]=self.pheromones[initPosition,nextPosition]
                thisAntDist.append(distanceBetween)
                position=nextPosition

            thisAntTour.append(position)

            if (len(self.remainingList)==1):
                thisAntDist.append(self.EuDist(self.remainingList[0],antPos[ants]))
            sumDistance=sum(thisAntDist)

            allShortestDist.append(sumDistance)

            if first == 1:
                prevAntDist=sumDistance
                prevAntTour=thisAntTour
                self.globalMinDist=sumDistance
                self.globalMinPath=thisAntTour
                iterMinDist=sumDistance
                iterMinPath=thisAntTour
                first=first+1
            else:
                if (sumDistance < prevAntDist):
                    prevAntDist=sumDistance
                    prevAntTour=thisAntTour


            ants=ants+1

        if self.globalFirst==1:
            self.globalMinDist=prevAntDist
            self.globalMinPath=prevAntTour
            globalFirst=self.globalFirst+1
        else:
            if (prevAntDist < self.globalMinDist):
                self.globalMinDist=prevAntDist
        self.decayPheromones(self.globalMinDist)
        return self.globalMinDist

    def printFinal(self):
        gt=self.globalMinDist
        f=open("output.tour", "w")
        for n in self.globalMinPath:
            f.write("%d\n" % (n))


if __name__ == "__main__":

    myCode=ACO(filename)

    startTime = time.clock()
    myBestDistance=[]

    for n in range(0, time_sto):
        myBestDistance.append(myCode.moveAnts())
        endTime = time.clock()
        if ((endTime-startTime) > time_sto):
            myCode.printFinal()
            print filename, min(myBestDistance)
            sys.exit(0)
        n=n+1

    #print filename, min(myBestDistance)
    myCode.printFinal()
    print filename, min(myBestDistance)
