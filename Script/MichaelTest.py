

# How this code works:
# I downloaded the file from git and then placed in on the hard drive. I haven't pulled data files from git before so that is something that I am looking into.

# =============================================================================
# The data steps used are:
#     Download the file onto the local drive
#     Convert the file to utf-8
#     Read through each line and then fix up issues that occur such as extra space, extra -.
#         From reviewing the file, there are only dashes in the account numbers so replacing all the '-' is fine
#     While each file is being read, insert them into a dataframe and then concat the objects in the dataframe to get
#     a new dataframe that can be used for creating a .tsv file that can be utilized.
#     To create the dataframe, the method used is with panda.to_csv
#     
# =============================================================================

import pandas as pd
SourceFile = r"C:\Users\mgold\Documents\data.tsv"
File2ndStep = r"C:\Users\mgold\Documents\data3.tsv"
DestinationFile = r"C:\Users\mgold\Documents\data4.tsv"

dfFinal = []
cat = ""

def update():
    with open(SourceFile, 'rb') as source_file:
      with open(File2ndStep, 'w+b') as dest_file:
        contents = source_file.read()
        dest_file.write(contents.decode('utf-16').encode('utf-8'))
    
    z = open(File2ndStep, 'rt')
    for line in z.readlines():
        line2 = line.replace('\t',',')
        line2 = line2.replace('\r',',')
        line2 = line2.replace('\n','')
        line2 = line2.replace('-','')
        line2 = line2.replace(' ','')
        if line2.count(',') == 4:
            cat = '' 
            new = pd.DataFrame(line2.split(',')).T
            dfFinal.append(new)
        if line2.count(',') != 4:
            if line2.count(',') < 4:
                cat += line2
            else:
                cat = ""
        if cat.count(',') == 4:
            cat = cat.replace('\t',',')
            cat = cat.replace('\r',',')
            cat = cat.replace('\n','')
            cat = cat.replace('-','')
            cat = cat.replace(' ','')
            new = pd.DataFrame(cat.split(',')).T
            dfFinal.append(new)
    z.close()
    
    ResultFinal = pd.concat(dfFinal)
    new_header = ResultFinal.iloc[0] #grab the first row for the header
    ResultFinal = ResultFinal[1:] #take the data less the header row
    ResultFinal.columns = new_header #set the header row as the df header
    
    ResultFinal.to_csv(DestinationFile, sep='\t', index = False)

def __init__():
    update()  # When this program is run immediately run the update() function    

if __name__ == "__main__":
    __init__()  # When run as a script call this function
