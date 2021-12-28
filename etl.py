import pandas as pd

print("Reading raw data...")
df = pd.read_csv('data_balea.csv', sep=';')
print("Data read.")

# creating lists of proto-data
print("Preparing proto-data...")
comboListTAR = []
comboListFlag = []
comboListWeights = []
for i in range(0, len(df)):
    comboListFlag.append((df.TruckName[i], df.TARException[i], df.FlagWeightOverriden[i]))
    comboListTAR.append((df.TruckName[i], df.TARException[i]))
    theoWeight = df.WeightProductTradeUnitUsed[i]
    if df.Quantity[i] != 0:
        measuredWeight = df.Weight[i] / df.Quantity[i]
        if theoWeight != 0:
            comboListWeights.append((df.TruckName[i], (measuredWeight - theoWeight)/theoWeight, df.Weight[i]))
        else:
            comboListWeights.append((df.TruckName[i], 0, df.Weight[i]))
    else:
        measuredWeight = df.Weight[i]
        if theoWeight != 0:
            comboListWeights.append((df.TruckName[i], (measuredWeight - theoWeight)/theoWeight, df.Weight[i]))
        else:
            comboListWeights.append((df.TruckName[i], 0, df.Weight[i]))
print("Proto-data prepared.")

# creating list of trucks (individuals)
print("Preparing list of trucks...")
listOfTrucks = []
for truck in df.TruckName:
    if truck not in listOfTrucks:
        listOfTrucks.append(truck)
print("List of trucks prepared.")

# initialising new data lists
print("Preparing truck data...")
countTarExceptions = []
missionsOfTruck = []
exceptionRate = []
flagTARCorrelation = []
ratWeight = []
negWeight = []

for truck in listOfTrucks:
    nbExp = 0
    nbMissions = 0
    countEquals = 0
    countTotal = 0
    cnt = 0
    totalWeightDiv = 0
    cntNegWeight = 0
    for name,exp in comboListTAR:
        if name == truck:
            nbMissions += 1
            if exp == 1:
                nbExp += 1
    for name, e, f in comboListFlag:
        if truck == name:
            countTotal += 1
            if e == f:
                countEquals += 1
    for name, rat, wgt in comboListWeights:
        if truck == name:
            cnt += 1
            totalWeightDiv += rat
            if wgt <= 0:
                cntNegWeight += 1
    flagTARCorrelation.append(countEquals/countTotal)
    countTarExceptions.append(nbExp)
    missionsOfTruck.append(nbMissions)
    ratWeight.append(totalWeightDiv / cnt)
    negWeight.append(cntNegWeight/nbMissions)

for i in range(0, len(countTarExceptions)):
    exceptionRate.append(countTarExceptions[i]/missionsOfTruck[i])
print("Truck data prepared.")

# making new dataframe with trucks as individuals
print("Creating truck dataframe...")
zipped = list(zip(listOfTrucks, countTarExceptions, missionsOfTruck, exceptionRate, flagTARCorrelation, ratWeight, negWeight))
newDF = pd.DataFrame(zipped, columns=['Trucks', 'TARExceptions', 'NumMissions', 'ExceptionRate', 'TARCorrelation', 'AvgWeightDiff', 'NumNegativeWeights'])
zipped = list(zip(listOfTrucks, missionsOfTruck, exceptionRate, ratWeight))
figDF = pd.DataFrame(zipped, columns=['names', 'missions', 'exceptions', 'weight-diff'])
print("Truck dataframe created.")

newDF.to_csv('data_trucks.csv')
figDF.to_csv('data_fig.csv')
