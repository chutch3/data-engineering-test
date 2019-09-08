#!/usr/bin/env python
# coding: utf-8

# In[34]:


import pandas as pd
import csv


# In[101]:


### Read the file line by line
print('Reading the file line by line')
data = []
with open('../data/data.tsv','r', encoding='utf-16-le') as f:
    for line in f:
        data.append(line.split('\t'))
print('Read all the lines')


# In[103]:


print("There are {att} attributes in the data which are: {cols}".format(att=len(data[0]),cols=data[0]))


# In[104]:


print("There are {l} records in the file but the last id in the file is {lastid}".format(l = len(data),lastid = data[-1][0]))


# In[105]:


print("Find the lines that are messed up and search the pattern in them")


# In[106]:


line_num = 0
for record in data:
    if len(record)!=5:
        print("line number",line_num)
        print(record)
    line_num = line_num+1   


# In[44]:


print("There is a misalignment in those 16 lines")


# In[153]:


clean_data = []
reading_data = True
line_number = 0
while reading_data:
    #print(line_number)
    record = data[line_number]
    line_number = line_number+1
    if len(record)==5:
        clean_data.append([x.split("\n")[0] for x in record])
    else:
        print(line_number-1,record)
        found_record_w_correct_format = False
        psudo_line_number = line_number
        while not found_record_w_correct_format:
            psudo_record = data[psudo_line_number]
            psudo_line_number = psudo_line_number +1
            print(psudo_line_number-1,psudo_record)
            if len(psudo_record)==5:
                psudo_line_number = psudo_line_number -1
                found_record_w_correct_format = True
        fixed_record = [x.split("\n")[0] for x in record if x.strip()!='']
        for bad_line in range(line_number,psudo_line_number):
            fixed_record = fixed_record + [x.split("\n")[0] for x in data[bad_line] if x.strip()!='']
            print(fixed_record)
        print("Skipped line number",line_number-1,psudo_line_number)
        clean_data.append(fixed_record)
        line_number = psudo_line_number
        
    if record[0]==data[-1][0]: 
        reading_data=False


# In[156]:


print("Check if any record list has more than 5 values")
for record in clean_data:
    if len(record)!=5:
        print(record)


# In[159]:


print("Fix those records manually")
clean_data[29] = ['29', 'Adena', 'Hobbs Bosley', '656184', 'ac.ipsum.Phasellus@ut.net']
clean_data[217] = ['217', 'Boris', 'Harrington', '325378', 'neque.Nullam.ut@laoreetlectus.edu']


# In[169]:


print('Write to a file')
df = pd.DataFrame(clean_data[1:],columns=clean_data[0])

df.to_csv('../data/clean_data.tsv',sep='\t',encoding='utf-8',index=False)


# In[ ]:




