import pandas as pd
import matplotlib.pyplot as plt

#Get the data url
with open ('data.txt', 'r') as f:
    data = f.read()
name = data.rsplit('/', 1)[-1]

#Download the data
import shutil
import urllib.request as request
from contextlib import closing

with closing(request.urlopen(data)) as r:
    with open(name,'wb') as f:
        shutil.copyfileobj(r, f)

#Create the DF and calculate chromosome lengths
df = pd.read_csv(name, sep="\t", comment='#', header=None, usecols=[0,3,4], names = ['chr', 'start', 'end'])
df = df.set_index('chr').astype(int)
df = df.groupby(['chr']).agg({'start': ['min'], 'end': ['max']}).diff(axis=1).drop(df.columns[[0]], axis=1)
df.columns = ['length']

#To sort by chromosome number and save as .xlsx
df = df.reset_index()
df['chr'] = df['chr'].str[3:]
dfnum = df[:-3]
dfcha = df[-3:]
dfnum = dfnum.sort_values(by='chr', key=lambda x: x.astype(int))
df = dfnum.append(dfcha)
df['chr'] = 'chr' + df['chr'].astype(str)
df = df.set_index('chr').astype(int)
df.to_excel("data.xlsx", sheet_name=name)

#Create the plot and save the graph
df.plot(kind='barh', title='Chromosome lengths in mouse genome', color='#FF7F50').invert_yaxis()
plt.savefig('graph.png', dpi=150)