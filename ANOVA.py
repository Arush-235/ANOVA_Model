#level_of_significance = 0.10
level_of_significance = input("Level of Significance \n\t(1) 0.10\n\t(2) 0.05\n")
if level_of_significance=='2':
    csv_filename = 'F Distribution α=0.05.csv'
elif level_of_significance=='1':
    csv_filename = 'F Distribution α=0.10.csv'

# α is taken 0.10 here since too much extra data would have to be carried along to accomodate all α

class population:
    def __init__(self, name):
        self.name = name
        self.sample = []
        self.mean = 0
        self.class_size = 0
        self.var = 0
        self.SumOfSqTotal = 0
        self.SumOfSqWithin = 0


    def collect_data(self):
        self.sample = list(map(float,input("Enter the sample data for population {} (Comma Separated): \n".format(self.name)).split()))
        self.class_size = len(self.sample)
        self.mean = sum(self.sample) / self.class_size

    def SStotal(self,grandMean):
        self.SumOfSqTotal = sum([(i-grandMean)**2 for i in self.sample])
        return self.SumOfSqTotal

    def SSwithin(self):
        self.SumOfSqWithin = sum([(i-self.mean)**2 for i in self.sample])
        return self.SumOfSqWithin

samples = []
for i in range(int(input("Number of sample classes: "))):
    p = population(input("Class name: "))
    p.collect_data()
    samples.append(p)

# Grand Mean
# It is calculated by adding all the values across all samples and dividing by total number of samples

Xi = 0
ni = 0
for i in samples:
    for j in i.sample:
        Xi += j
    ni += i.class_size
grand_mean = Xi/ni

# Sum of Squares Total Calculation:
SStotal = 0
for i in samples:
    SStotal += i.SStotal(grand_mean)

# Sum of Squares Within Calculation:
SSwithin = 0
for i in samples:
    SSwithin += i.SSwithin()

# Sum of Squares Between Claculation:
SSBetween = SStotal -SSwithin

# Degrees of Freedom Between and DF Within Calculation:
DFbetween = len(samples) - 1
DFwithin = sum([i.class_size for i in samples])

# Variance Within Classes and Variance Between Classes Calculation:
VarianceWithin = SSBetween / DFbetween
VarianceBetween = SSwithin / DFwithin

F = VarianceBetween / VarianceWithin

# Calculating F Critical Value for the distribution using a F Distribution Table for α = 0.10, which I downloaded from
# http://www.socr.ucla.edu/Applets.dir/F_Table.html and converted to a CSV using Google Sheets 
# https://docs.google.com/spreadsheets/d/1GjmWv60z4o_DhTF1tSKei-yH_4-LXsSTqxGcBV9quLg/edit?usp=sharing.

import csv
FCritical = 0

with open(csv_filename) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')  
    row = next(csv_reader)
    y = 0
    if DFbetween in row:
        y = row.index(DFbetween)
    else:
        i = 1
        while int(row[i])<DFbetween:
            i+=1
        y = i
    
    for row in csv_reader:
        if int(row[0]) <= DFwithin:
            FCritical = float(row[y])
        else:
            break
    
# Testing if the Null Hypothesis can be rejected or not

if F <= FCritical:
    print("Failed to reject the Null Hypothesis. This implies that the Variation of the means of the classes is negligible. ") 
else:
    print("Null Hypothesis is rejected. The data sample classes have significant variance.")
