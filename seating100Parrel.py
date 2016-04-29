import pandas as pd
import numpy as np
from copy import deepcopy
import time
from joblib import Parallel, delayed
import multiprocessing
import gc



df=pd.read_csv('BloombergVOTELEVEL_Touse.csv',nrows=9)



caseList=pd.unique(df['caseid'])
caseList=caseList[pd.notnull(caseList)].tolist()


caseColumns=df.columns.tolist()


keep_col=['caseid','judgeidentificationnumber','Dissenting1']
for i in caseColumns:
    if (i in keep_col):
        caseColumns.remove(i)


df.drop(labels=caseColumns,axis=1,inplace=True)



df['judge2code'] = pd.Series(np.zeros(df.shape[0]), index=df.index)



df['judge2dissent'] = pd.Series(np.zeros(df.shape[0]), index=df.index)



print df.shape


num_cores = multiprocessing.cpu_count()

                
def for_seating(case):
    temper=np.where(df.caseid==case)
    temper=(temper[0]).tolist()
    for i in range(len(temper)):
        df.loc[temper[i],'judge2code']=df.ix[temper[i-1]]['judgeidentificationnumber']
        df.loc[temper[i],'judge2dissent']=df.ix[temper[i-1]]['Dissenting1']

Parallel(n_jobs=num_cores)(delayed(for_seating)(case) for case in caseList)

df.to_csv('seating100.csv')



