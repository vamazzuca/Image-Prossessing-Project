import math
import random

def euclidD(point1, point2):
    sum = 0
    for index in range(len(point1)):
        diff = (point1[index]-point2[index]) ** 2
        sum = sum + diff
        
    return math.sqrt(sum)

def manhattanD(point1, point2):
    sum = 0
    for i in range(len(point1)):
        diff = abs(point1[i]-point2[i])
        sum = sum + diff
        
    return sum

def createCentroids(k, datadict):
    centroids=[]           
    centroidCount = 0
    centroidKeys = []
    random.seed(68)

    keys = list(datadict.keys())

    while centroidCount < k: 
       rkey = random.randint(0,len(datadict))
       if rkey not in centroidKeys:
           centroids.append(datadict[keys[rkey]])   
           centroidKeys.append(rkey)       
           centroidCount = centroidCount + 1   
           
    return centroids

def showCentroids(centroids):
    print("CENTROIDS", end = " ")
    for cent in centroids:
        #print("%4.1f" % (cent[0]), end = " ")
        print(cent, end = " ")
    print()                     

def showClusters(clusters, datadict):
    for c in clusters:          
       print ("CLUSTER", end = " ")
       for key in c:
           print(datadict[key], end=" ")
       print()  

def assignPointsToClusters(centroids,datadict): 
    clusters = []
    k = len(centroids)
    for i in range(k):
        clusters.append([])             
    for akey in datadict:
        distances = []                     
        for clusterIndex in range(k):    
            dist = euclidD(datadict[akey],centroids[clusterIndex])
            distances.append(dist)       

        mindist = min(distances)         
        index = distances.index(mindist)   
        clusters[index].append(akey)     
    return clusters

def updateCentroids(clusters, centroids,datadict):
    dimensions = len(datadict[list(datadict.keys())[0]])
    k = len(centroids)      
    for clusterIndex in range(k):      
        sums = [0]*dimensions
        for akey in clusters[clusterIndex]:
            datapoints = datadict[akey]
            for ind in range(len(datapoints)):           
                sums[ind] = sums[ind] + datapoints[ind]  
        for ind in range(len(sums)):                    
            clusterLen = len(clusters[clusterIndex])
            if clusterLen != 0:
                sums[ind] = sums[ind]/clusterLen   
        centroids[clusterIndex] = sums
    return centroids
                    

def createClusters(centroids, datadict, repeats):
    k = len(centroids)
    doAgain = True
    apass = 0
    while doAgain and apass < repeats:
        clusters = []
        prevClusters = clusters

        clusters = assignPointsToClusters(centroids,datadict)

        if clusters == prevClusters:
            doAgain = False

        centroids = updateCentroids(clusters, centroids, datadict)
       
        apass = apass + 1

    return clusters

def readFile(filename):
    datafile = open(filename, "r")
    datadict = {}

    key = 0
    for aline in datafile:
       key = key + 1
       items = aline.split()
       datadict[key] = [int(k) for k in items]   
       
    return datadict

def main():
    datadict = readFile("scores.txt")
    numClusters = 5 # number of clusters
    dataCentroids = createCentroids(numClusters, datadict)
    maxPass = 10
    dataClusters = createClusters(dataCentroids, datadict, maxPass)

if __name__ == "__main__":
    main()

