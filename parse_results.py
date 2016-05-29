import os


dist = {}
dist['coco'] = 20
dist['vspm-vssd'] = 32
dist['cmlv-cmls'] = 113 

#################################

def parse():

    fp = open("results_latest.txt","r")
    newRun = True
    allResults = []
    currentResult = []
    for line in fp.readlines():
        if "RUN" in line:
            if currentResult:
                allResults.append(currentResult)
                currentResult = []
        elif line.strip():
            currentResult.append(' '.join(line.strip().split()))
    fp.close()
    allResults.append(currentResult)

    maxSizeResults = []
    maxEdgeDensityResults = []
    for i in range(len(allResults)/2):
        maxSizeResults.append(allResults[i])
    for i in range(len(allResults)/2,len(allResults)):
        maxEdgeDensityResults.append(allResults[i])
    fpString = ""

    k = 0
    for communityResults in (maxSizeResults, maxEdgeDensityResults):
        k += 1
        if k==1:
            fpString = "max-size"+"_"
        else:
            fpString = "max-edge-density"+"_"
        meanResults = []
        medianResults = []
        for result in communityResults:
            if result[6].split()[-1]=="1" and result[7].split()[-1]=="0":
                meanResults.append(result)
            elif result[6].split()[-1]=="0" and result[7].split()[-1]=="1":
                medianResults.append(result)

        meanDicts = []
        trpoCount = 0
        fapoCount = 0
        prevMnd = {}
        j = 0
        for results in (meanResults,medianResults):
            j += 1
            mmfpString = "".join(fpString)
            if j==1:
                fpString += "mean"+"_"
            else:
                fpString += "median"+"_"
            for i in range(len(results)):
                result = results[i]
                coco = int(result[1].split()[-1])
                vspm = float(result[2].split()[-1])
                vssd = float(result[3].split()[-1])
                cmlv = float(result[4].split()[-1])
                cmls = float(result[5].split()[-1])
                trpo = float(result[10].split()[-1])
                fapo = float(result[12].split()[-1])
                mied = float(result[14].split()[-1])
                #print str(i) + ": " + str(cmlv)+","+str(cmls)
                prevfpString = "".join(fpString)
                if i>=0 and i<dist['coco']:
                    fpString += "content-count.txt"
                    fp = open("plots/"+fpString,"a")
                    fp.write(str(i)+" "+str(coco)+" "+str(trpo)+" "+str(fapo)+" "+str(mied)+"\n")
                    fp.close()
                    fpString = "".join(prevfpString)
                elif i>=dist['coco'] and i<dist['vspm-vssd']:
                    fpString += "view-share-prob-mean-stdv.txt"
                    fp = open("plots/"+fpString,"a")
                    fp.write(str(i-dist['coco'])+" "+str(vspm)+" "+str(vssd)+" "+str(trpo)+" "+str(fapo)+" "+str(mied)+"\n")
                    fp.close()
                    fpString = "".join(prevfpString)
                elif i>=dist['vspm-vssd'] and i<dist['cmlv-cmls']:
                    fpString += "content-min-level-view-share.txt"
                    fp = open("plots/"+fpString,"a")
                    fp.write(str(i-dist['vspm-vssd'])+" "+str(cmlv)+" "+str(cmls)+" "+str(trpo)+" "+str(fapo)+" "+str(mied)+"\n")
                    fp.close()
                    fpString = "".join(prevfpString)
            fpString = "".join(mmfpString)

#################################

def main():
    parse()
    return

#################################

if __name__ == "__main__":
    main()
