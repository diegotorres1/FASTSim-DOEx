##Author: Diego Torres
##Date of Modification: 6/28/18
##Description: Implement an equivalent DOE function in python for FASTSim
import csv
import os
import FASTSim
import time
fieldnames = []
resultDict = {}
orderDict = {}
orderStringDict = {}
def callFunc(listArrays,listdv,n,cyc,veh):
    if(n>1):
        for x in listArrays[n-1]:
            listdv[n-1] = x
            newlist = listdv[:]
            callFunc(listArrays,newlist,n-1,cyc,veh)
    else:
        count = 0
        global fieldnames
        global resultDict
        global orderDict
        global orderStringDict
        for y in listArrays[n-1]:
            listdv[n-1] = y
            #change the design variables

            for key in orderStringDict:
                if(orderStringDict[key] < len(listdv)):
                    #print(str(veh['maxFuelConvKw']) + ',' + str(veh['maxMotorKw']) + ',' + str(veh['maxEssKw']) + ',' + str(veh['maxEssKwh']))
                    print(type(veh[key]))
                    veh[key] = float(listdv[orderStringDict[key]])

            if(all(listdv)):
                output = FASTSim.sim_drive(cyc, veh)
            #write sim to DOEout
                count = 0
                for key in resultDict:
                    if(orderStringDict[key] < len(listdv)):
                        resultDict[key].append(str(listdv[orderStringDict[key]]))
                    else:
                        # print('This is the orderString index : ' + str(orderStringDict[key]))
                        print(key + '\t\t\t\t: ' + str(output[key]))
                        resultDict[key].append(str(output[key]))
                    count = count + 1
            print(str(listdv))
            #print(str(veh['maxFuelConvKw']) + ',' + str(veh['maxMotorKw']) + ',' + str(veh['maxEssKw']) + ',' + str(veh['maxEssKwh']))
def genList(low,high,levels):
    low = int(low)
    high = int(high)
    levels = int(levels)
    list = []
    for i in range(levels):
        list.append((((high-low)/(levels - 1)) * i) + low)
    return list
def main():
    os.chdir('D://UCI//Research APEP//fastsim-python-2018b//fastsim-2018b//src')
    dvDict = {}
    listdv = []



    global fieldnames
    global resultDict
    global orderDict
    global orderStringDict

    cyc = FASTSim.get_standard_cycle("udds")
    veh = FASTSim.get_veh(10)
    print(veh)
    with open('DOEdv.csv', 'rb') as csvfile:
        doereader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in doereader:
            if(row[0] == 'designvariables'):
                del row[0]
                dvNames = row
                print(dvNames)
            elif(row[0] == 'low'):
                del row[0]
                low = row
            elif(row[0] == 'high'):
                del row[0]
                high = row
            elif(row[0] == 'levels'):
                del row[0]
                levels = row
            elif(row[0] == 'results'):
                del row[0]
                outputNames = row

    fieldnames = dvNames + outputNames
    n = len(low)
    count = 0
    for name in dvNames:
        dvDict[name] = 0
        listdv.append(0)
        orderDict[count] = name
        orderStringDict[name] = count
        resultDict[name] = [0]
        count = count + 1
    for oname in outputNames:
        orderDict[count] = oname
        orderStringDict[oname] = count
        resultDict[oname] = [0]
        count = count + 1
    # print('This is the orderStringDict : ' + str(orderStringDict))

    listArrays = []
    listWriteRow = []
    for i in range(n):
        listArrays.append(genList(low[i],high[i],levels[i]))
    start = time.time()
    print('Estimated Time for Completion : \t\t\t' + str(reduce(lambda x, y: x*y, map(int,levels))))
    callFunc(listArrays,listdv,n,cyc,veh)
    end = time.time()
    print('Entire Time : ' + str(end - start ))
    with open('DOEout.csv', 'wb') as csv_file:
        doewriter = csv.writer(csv_file)
        doewriter.writerow(fieldnames)
        for i in range(len(resultDict[fieldnames[0]])):
            for x in orderDict:
                listWriteRow.append((resultDict[orderDict[x]])[i])
            if(listWriteRow[0] != 0):
                doewriter.writerow(listWriteRow)
            listWriteRow = []

if __name__ ==  "__main__":
    main()
    print('RecurseTest')
