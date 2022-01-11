import pandas as pd
DATE = (2021, 1, 7)

# TODO - Restart ETL with scales in mind, not trucks. Truck data can be synthesised from scale data after.
# Then change app.py to work correctly with it.

print("Reading raw data...")
df = pd.read_csv('data_balea.csv', sep=';')
print(len(df))
print("Data read.")

prepListBalances = []
for i in range(0, len(df)):
    prepListBalances.append((df.TruckName[i], df.CorridorNumber[i]))

# creating list of trucks (individuals)
print("Preparing list of trucks...")
listOfTrucks = []
for truck in df.TruckName:
    if truck not in listOfTrucks:
        listOfTrucks.append(truck)
print("List of trucks prepared.")
print("Preparing list of balances...")
protoListOfBalances = []
listOfBalances = []
for truck,balance in prepListBalances:
    if len(protoListOfBalances) > 0:
        val = True
        for (t,b) in protoListOfBalances:
            if truck == t and b == balance:
                val = False
        if val:
            protoListOfBalances.append((truck, balance))
    else:
        protoListOfBalances.append((truck, balance))
for truck, balance in protoListOfBalances:
    listOfBalances.append(truck.__str__()+" : "+balance.__str__())
print("List of balances prepared.")

# initialising new data lists

# creating lists of proto-data
print("Preparing proto-data...")
comboListTAR = []
comboListFlag = []
comboListWeights = []
for i in range(0, len(df)):
    comboListFlag.append((df.TruckName[i], df.CorridorNumber[i], df.TARException[i], df.FlagWeightOverriden[i]))
    comboListTAR.append((df.TruckName[i], df.CorridorNumber[i], df.TARException[i]))
    theoWeight = df.WeightProductTradeUnitUsed[i]
    if df.Quantity[i] != 0:
        measuredWeight = df.Weight[i] / df.Quantity[i]
        if theoWeight != 0:
            comboListWeights.append((df.TruckName[i], df.CorridorNumber[i], (measuredWeight - theoWeight)/theoWeight, df.Weight[i]))
        else:
            comboListWeights.append((df.TruckName[i], df.CorridorNumber[i], 0, df.Weight[i]))
    else:
        measuredWeight = df.Weight[i]
        if theoWeight != 0:
            comboListWeights.append((df.TruckName[i], df.CorridorNumber[i], (measuredWeight - theoWeight)/theoWeight, df.Weight[i]))
        else:
            comboListWeights.append((df.TruckName[i], df.CorridorNumber[i], 0, df.Weight[i]))
print("Proto-data prepared.")

print("Preparing balance data...")
countTarExceptionsBalance = []
measuresOfTruckBalance = []
exceptionRateBalance = []
ratWeightBalance = []
negWeightBalance = []
for truck, balance in protoListOfBalances:
    nbExp = 0
    nbMissions = 0
    countEquals = 0
    countTotal = 0
    cnt = 0
    totalWeightDiv = 0
    cntNegWeight = 0
    for (name, bal, exp) in comboListTAR:
        if name == truck and bal == balance:
            nbMissions += 1
            if exp == 1:
                nbExp += 1
    for (name, bal, e, f) in comboListFlag:
        if truck == name and bal == balance:
            countTotal += 1
            if e == f:
                countEquals += 1
    for (name, bal, rat, wgt) in comboListWeights:
        if truck == name and bal == balance:
            cnt += 1
            totalWeightDiv += rat
            if wgt <= 0:
                cntNegWeight += 1
    countTarExceptionsBalance.append(nbExp)
    measuresOfTruckBalance.append(nbMissions)
    if(cnt != 0):
        ratWeightBalance.append(totalWeightDiv / cnt)
    else:
        ratWeightBalance.append(0)
    negWeightBalance.append(cntNegWeight)

for i in range(0, len(countTarExceptionsBalance)):
    exceptionRateBalance.append(countTarExceptionsBalance[i]/measuresOfTruckBalance[i])
print("Balance data prepared.")

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
    for name, bal, exp in comboListTAR:
        if name == truck:
            nbMissions += 1
            if exp == 1:
                nbExp += 1
    for name, bal, e, f in comboListFlag:
        if truck == name:
            countTotal += 1
            if e == f:
                countEquals += 1
    for name, bal, rat, wgt in comboListWeights:
        if truck == name:
            cnt += 1
            totalWeightDiv += rat
            if wgt <= 0:
                cntNegWeight += 1
    if(countTotal != 0):
        flagTARCorrelation.append(countEquals/countTotal)
    else:
        flagTARCorrelation.append(0)
    countTarExceptions.append(nbExp)
    missionsOfTruck.append(nbMissions)
    if(cnt != 0):
        ratWeight.append(totalWeightDiv / cnt)
    else:
        ratWeight.append(0)
    negWeight.append(cntNegWeight)

for i in range(0, len(countTarExceptions)):
    exceptionRate.append(countTarExceptions[i]/missionsOfTruck[i])
print("Truck data prepared.")

# making new dataframe with trucks as individuals
print("Creating dataframes...")
zipped = list(zip(listOfTrucks, countTarExceptions, missionsOfTruck, exceptionRate, ratWeight, negWeight))
newDF = pd.DataFrame(zipped, columns=['Trucks', 'TARExceptions', 'NumMissions', 'ExceptionRate', 'AvgWeightDiff', 'NumNegativeWeights'])
zipped = list(zip(listOfBalances, countTarExceptionsBalance, measuresOfTruckBalance, exceptionRateBalance, ratWeightBalance, negWeightBalance))
balDF = pd.DataFrame(zipped, columns=['Balances', 'TARExceptions', 'NumMissions', 'ExceptionRate', 'AvgWeightDiff', 'NumNegativeWeights'])
zipped = list(zip(listOfTrucks, missionsOfTruck, exceptionRate, ratWeight))
figDF = pd.DataFrame(zipped, columns=['names', 'missions', 'exceptions', 'weight-diff'])
print("Dataframes created.")

balDF.to_csv('data_balances.csv')
newDF.to_csv('data_trucks.csv')
figDF.to_csv('data_fig.csv')
