import pandas as pd

# create some test data
# columns are topics and rows are URLs of articles
'''testdata = pd.DataFrame([[1,1,0,0],[0,1,0,0],[0,0,1,0]],
                    columns=['Extreme poverty','Cure Cancer','US land use',
                             'US teacher red tape'],
                    index=['a','b','c'])'''

def calculateURLQUALYs(topicsofURLS,QUALYdatafile):
    # This function takes in a dataframe and the name of a CSV file and outputs
    # a dictionary of the total QUALYs for each URL

    
    # Read in the data for the QUALYs for each topic
    global_prios = pd.read_csv(QUALYdatafile)

    # Select only the part of the CSV needed
    global_prios = global_prios[['Topic',' Yearly QALY/DALY']]

    # Convert this data for the qualys for each topic to a dictionary
    qualydata = {}

    for index, row in global_prios.iterrows():
        qualydata[row[0]] = row[1]

    # Create a dictioary giving the QUALYs for each URL
    qualys = {}

    for index, row in testdata.iterrows():
        qualys[index] = 0
        for topic in list(testdata):
            if testdata[topic][index] > 0:
                qualys[index] += qualydata[topic]
                
    return(qualys)

#print(calculateURLQUALYs(testdata,"global_prios.csv"))
    
