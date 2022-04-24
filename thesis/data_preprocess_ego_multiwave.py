import os
import re
import numpy as np
import pandas as pd
from pathlib import Path
from thesis import params


# part 1 - data load
df_ego = pd.read_stata(Path.cwd() / "data/thesis/36975-0008-Data.dta")

# 1. get the var_dict and recode the variables within the dict

columns = df_ego.columns

ego_var_dict = params.ego_var_dict

ego = pd.DataFrame()

for column, value in ego_var_dict.items():
    replace_dict = value[1]
    # replace_dict[None] = np.nan
    col_name = value[0].replace(' ','_')
    ego[col_name+'_1']= df_ego[column].replace(replace_dict)

    if value[2]:  # multiple waves
        ego[col_name+'_2'] = df_ego[column+'_W2'].replace(replace_dict)
        ego[col_name+'_3'] = df_ego[column+'_W3'].replace(replace_dict)
    else:
        continue


# 2. Recode the dependent variables into 2 variables: E_aggregate and E_Pattern
#    E_aggregate -> 1 if any of Know_More_Personal_Concerns,E4,E5 is 1
#    E_Pattern -> 7 patterns, see below for more information
IV = ['Know_More_Personal_Concerns_1',
 'Know_More_Personal_Concerns_2',
 'Know_More_Personal_Concerns_3',
 'Know_More_Good_Time_1',
 'Know_More_Good_Time_2',
 'Know_More_Good_Time_3',
 'Know_More_Sick_Help_1',
 'Know_More_Sick_Help_2',
 'Know_More_Sick_Help_3']

ego[IV] = ego[IV].replace(np.nan, 0)


for index, row in ego.iterrows():
    for wave in ['_1','_2','_3']:
        if (row['Know_More_Personal_Concerns'+wave] == 1) | (row['Know_More_Good_Time'+wave] == 1)|(row['Know_More_Sick_Help'+wave] == 1):
            ego.loc[index,'Know_More'+wave]=1
            ego.loc[index, 'Know_More_Score' + wave] = row['Know_More_Personal_Concerns'+wave]+row['Know_More_Good_Time'+wave]+row['Know_More_Sick_Help'+wave]
        else:
            ego.loc[index, 'Know_More'+wave] = 0
            ego.loc[index, 'Know_More_Score' + wave]=0

'''
        if row['Know_More_Personal_Concerns'+wave]==1:
            if row['Know_More_Good_Time'+wave]==1:
                if row['Know_More_Sick_Help'+wave]==1:
                    ego.loc[index, 'Know_More_Pattern'+wave] = 7  # Know_More_Personal_Concerns45
                else:
                    ego.loc[index, 'Know_More_Pattern'+wave] = 6  # Know_More_Personal_Concerns4
            elif row['Know_More_Sick_Help'+wave]==1:
                ego.loc[index, 'Know_More_Pattern'+wave] = 5  # Know_More_Personal_Concerns5
            else:
                ego.loc[index, 'Know_More_Pattern'+wave] =4  # Know_More_Personal_Concerns
        elif row['Know_More_Good_Time'+wave]==1:
            if row['Know_More_Sick_Help'+wave]==1:
                ego.loc[index, 'Know_More_Pattern'+wave] = 3  # E45
            else:
                ego.loc[index, 'Know_More_Pattern'+wave] = 2  # E4
        elif row['Know_More_Sick_Help'+wave] == 1:
            ego.loc[index, 'Know_More_Pattern'+wave] = 1  # E5
        elif row['Know_More_Sick_Help'+wave]==row['Know_More_Good_Time'+wave]==row['Know_More_Personal_Concerns'+wave]==0:
            ego.loc[index, 'Know_More_Pattern'+wave] = 0  # None
        else:
            print('error')
'''

# check with the Know_More for multiple waves
# save this in case we want to use it
# ego_IV_Patterns = ego.loc[:,['Know_More_Pattern_1','Know_More_Pattern_2','Know_More_Pattern_3']]

Know_More_columns = [x if ('Know_More' in x) & ('Pattern' not in x) else None for x in ego.columns]
while None in Know_More_columns: Know_More_columns.remove(None)

# ego_IV = ego.loc[:, Know_More_columns]


# 3. Recode the Income into K21 : HHIncome
'''
income_columns = ['Household_Income_1','Personal_Income>50000_1','Household_Income_2','Personal_Income>50000_2','Household_Income_3','Personal_Income>50000_3']

income = ego.loc[:,income_columns]

for index, row in income.iterrows():
    for wave in ['_1', '_2', '_3']:
        if np.isnan(row['Household_Income'+wave]):
            if np.isnan(row['Personal_Income>50000'+wave]):
                income.loc[index,'aggregate'+wave] = None
            else:
                income.loc[index, 'aggregate'+wave] = 6
        else:
            if np.isnan(row['Personal_Income>50000'+wave]):
                income.loc[index, 'aggregate'+wave] = row['Household_Income'+wave]  # only Household_Income has value
            else:
                income.loc[index, 'aggregate'+wave] = row['Household_Income'+wave]  # both have values # result: no such combination
        # mean = income['aggregate'+ wave].mean()
        # income['aggregate' + wave] = income['aggregate' + wave].replace(np.nan,mean)
        ego['Household_Income'+wave] = income['aggregate'+wave]
'''


# combine some variables

params.var_name_check('Recent_Unemployed',ego.columns)
for wave in ['_1', '_2', '_3']:
    # 1. Recent_Major_Problem_on_work_school_or_financial
    ego[['Recent_Major_Problem_at_work'+wave,'Recent_Major_Problem_at_School'+wave,'Recent_Major_Financial_Problem'+wave]]=ego[['Recent_Major_Problem_at_work'+wave,'Recent_Major_Problem_at_School'+wave,'Recent_Major_Financial_Problem'+wave]].replace(np.nan,0)
    ego['Recent_Major_Problem_on_work_or_school_or_financial'+wave] = [x+y+z for x,y,z in zip(ego['Recent_Major_Problem_at_work'+wave],ego['Recent_Major_Problem_at_School'+wave],ego['Recent_Major_Financial_Problem'+wave])]
    ego.drop(columns=['Recent_Major_Problem_at_work'+wave,'Recent_Major_Problem_at_School'+wave,'Recent_Major_Financial_Problem'+wave],inplace=True,axis=1)
    
    # 2. Recent Pass away
    ego['Recent_kin_died'+wave]=[1 if (x==1)|(y==1)|(y==3) else 0 for x,y in zip(ego['Recent_Close_Alter_Died'+wave],ego['Recent_Multiple_Alters_Died'+wave])]
    ego['Recent_non_kin_died'+wave]=[1 if (x==2)|(y==2)|(y==3) else 0 for x,y in zip(ego['Recent_Close_Alter_Died'+wave],ego['Recent_Multiple_Alters_Died'+wave])]
    ego.drop(columns=['Recent_Close_Alter_Died'+wave,'Recent_Multiple_Alters_Died'+wave],axis=1,inplace=True)

    # 3. Recent New School/Job
    ego['New_School_Or_Job'+wave]=[1 if (x==1)|(y==1) else 0 for x,y in zip(ego['Recent_New_School'+wave],ego['Recent_New_Job'+wave])]
    ego.drop(columns=['Recent_New_School'+wave,'Recent_New_Job'+wave],axis=1,inplace=True)


# Recent_Break_Up_with_Close_Friends_or_Relatives

# ego.to_csv(Path.cwd()/'data/thesis/ego.csv')



ego['Recent_Major_Problem_on_work_or_school_or_financial_1'].replace({np.nan,0},inplace=True)
ego['Poor_Health_2'].replace({"1-2-3-5-6":1,'1-2-6-5':1,'1-2-3-4-5':1,'2-1-6':1,'3-1-5':1,'1-2-6-4-5':1},inplace=True)

ego['Unemployed_2'].replace({'':0,None:0,np.nan:0,np.NaN:0},inplace=True)
ego['Health_Issue_1'].replace({'':0,np.nan:0,np.NaN:0},inplace=True)
ego['Health_Issue_2'].replace({'':0,None:0,np.nan:0},inplace=True)
ego['Poor_Health_2'].replace({'':0,None:0,np.nan:0,np.NaN:0},inplace=True)
ego['Recent_Major_Problem_on_work_or_school_or_financial_1'].replace({'':0,None:0,np.nan:0,np.NaN:0},inplace=True)
ego['Recent_Major_Problem_on_work_or_school_or_financial_2'].replace({'':0,None:0,np.nan:0,np.NaN:0},inplace=True)
ego['Recent_Have_a_Child_Or_Grandchild_2'].replace({'':0,np.nan:0,np.NaN:0,None:0,np.NAN:0},inplace=True)
ego['Recent_Retired_2'].replace({'':0,np.nan:0,np.NaN:0},inplace=True)
ego['Recent_Important_change_in_marriage_1'].replace({'':0,np.NAN:0,np.NaN:0,None:0},inplace=True)
ego['Recent_Important_change_in_marriage_2'].replace({'':0,np.NAN:0,np.NaN:0,None:0},inplace=True)

ego['Recent_Break_Up_with_Close_Friends_or_Relatives_2'].replace({'':0,np.nan:0,np.NaN:0,None:0},inplace=True)

ego['Recent_Retired_1'].replace({'':0,np.nan:0,np.NaN:0,None:0},inplace=True)

'''
for column in ego.columns:
    print(ego['Recent_Have_a_Child_Or_Grandchild_2'].value_counts())
    continue_mark = input('press y to continue, 1 to print unique')
    if continue_mark =='1':
        print(ego[column].unique())
    else:
        continue

'''



ego['Belief_On_Having_Kin_To_Help_With_Serious_Problem_2'].replace({"4 Probably don't have":0},inplace=True)


# recode for wave 3
ego['Belief_On_Having_Kin_To_Help_With_Serious_Problem_3'].replace({"4 Probably don't have":0,'3':3,'2':2,'1':1},inplace=True)
ego['Recent_Retired_3'].replace({28:0,33:0},inplace=True)
ego['Recent_Retired_3'].replace({'3-1-2':1},inplace=True)

#ego.to_csv(Path.cwd()/'data/thesis/ego.csv')
