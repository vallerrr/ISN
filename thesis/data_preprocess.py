import os
import re
import numpy as np
import pandas as pd
from pathlib import Path
from thesis import params


# part 1 - data load
df_ego = pd.read_stata(Path.cwd() / "data/thesis/36975-0008-Ego.dta")

# 1. get the var_dict and recode the variables within the dict

columns = df_ego.columns

ego_var_dict = params.ego_var_dict

ego = pd.DataFrame()

for column, value in ego_var_dict.items():
    replace_dict = value[1]
    # replace_dict[None] = np.nan
    col_name = value[0].replace(' ','_')

    if 'Impact' in col_name:
        # binary variable
        col_name_binary = col_name.replace('_Impact','')

        ego[col_name+'_1'] = df_ego[column].replace(replace_dict)
        ego[col_name_binary+'_1'] = [0 if np.isnan(x) else 1 for x in ego[col_name+'_1']]
    else:
        ego[col_name]= df_ego[column].replace(replace_dict)

    if value[2]:  # multiple waves
        ego[col_name+'_2'] = df_ego[column+'_W2'].replace(replace_dict)
        ego[col_name+'_3'] = df_ego[column+'_W3'].replace(replace_dict)
    else:
        continue


# 2. get the data of first wave only ->ego_w1

ego_cols_w1 = [x if ('W2' not in x) & ('W3' not in x) else None for x in ego.columns]

while None in ego_cols_w1: ego_cols_w1.remove(None)
ego_w1 = pd.DataFrame()
ego_w1['PRIM_KEY'] = ego['ID']
ego_w1.loc[:, ego_cols_w1] = ego.loc[:, ego_cols_w1]


# 3. Recode the dependent variables into 2 variables: E_aggregate and E_Pattern
#    E_aggregate -> 1 if any of Know_More_Personal_Concerns,E4,E5 is 1
#    E_Pattern -> 7 patterns, see below for more information

ego_w1[['Know_More_Personal_Concerns', 'Know_More_Good_Time', 'Know_More_Sick_Help']] = ego_w1[['Know_More_Personal_Concerns','Know_More_Good_Time','Know_More_Sick_Help']].replace(np.nan, 0)
for index, row in ego_w1.iterrows():
    if (row['Know_More_Personal_Concerns'] == 1) | (row['Know_More_Good_Time'] == 1)|(row['Know_More_Sick_Help'] == 1):
        ego_w1.loc[index,'Know_More']=1
    else:
        ego_w1.loc[index, 'Know_More'] = 0

    if row['Know_More_Personal_Concerns']==1:
        if row['Know_More_Good_Time']==1:
            if row['Know_More_Sick_Help']==1:
                ego_w1.loc[index, 'Know_More_Pattern'] = 7  # Know_More_Personal_Concerns45
            else:
                ego_w1.loc[index, 'Know_More_Pattern'] = 6  # Know_More_Personal_Concerns4
        elif row['Know_More_Sick_Help']==1:
            ego_w1.loc[index, 'Know_More_Pattern'] = 5  # Know_More_Personal_Concerns5
        else:
            ego_w1.loc[index, 'Know_More_Pattern'] =4  # Know_More_Personal_Concerns
    elif row['Know_More_Good_Time']==1:
        if row['Know_More_Sick_Help']==1:
            ego_w1.loc[index, 'Know_More_Pattern'] = 3  # E45
        else:
            ego_w1.loc[index, 'Know_More_Pattern'] = 2  # E4
    elif row['Know_More_Sick_Help'] == 1:
        ego_w1.loc[index, 'Know_More_Pattern'] = 1  # E5
    elif row['Know_More_Sick_Help']==row['Know_More_Good_Time']==row['Know_More_Personal_Concerns']==0:
        ego_w1.loc[index, 'Know_More_Pattern'] = 0  # None
    else:
        print('error')


# 4. Recode the Income into K21 : HHIncome
income = ego.loc[:,['Household_Income','Personal_Income>50000']]

for index, row in income.iterrows():
    if np.isnan(row['Household_Income']):
        if np.isnan(row['Personal_Income>50000']):
            income.loc[index,'aggregate'] = None
        else:
            income.loc[index, 'aggregate'] = 6
    else:
        if np.isnan(row['Personal_Income>50000']):
            income.loc[index, 'aggregate'] = row['Household_Income']  # only Household_Income has value
        else:
            income.loc[index, 'aggregate'] = [row['Household_Income'], row['Personal_Income>50000']]  # both have values
            # result: no such combination

# replace the samples nans with median in this category in the income
income['aggregate'] = income['aggregate'].replace(np.nan, income['aggregate'].median())
ego_w1['Household_Income'] = income['aggregate']

# combine some variables

# 1. Recent_Major_Problem_on_work_school_or_financial
ego_w1['Recent_Major_Problem_on_work_school_or_financial'] = [x+y+z for x,y,z in zip(ego_w1['Recent_Major_Problem_at_work'],ego_w1['Recent_Major_Problem_at_School'],ego_w1['Recent_Financial_Problem'])]
ego_w1.drop(columns=['Recent_Major_Problem_at_work','Recent_Major_Problem_at_School','Recent_Financial_Problem'],inplace=True,axis=1)

# 2. Recent Pass away
ego_w1['Recent_kin_died']=[1 if (x==1)|(y==1)|(y==3) else 0 for x,y in zip(ego_w1['Recent_Close_Alter_Died'],ego_w1['Recent_Multiple_Alters_Died'])]
ego_w1['Recent_non_kin_died']=[1 if (x==2)|(y==2)|(y==3) else 0 for x,y in zip(ego_w1['Recent_Close_Alter_Died'],ego_w1['Recent_Multiple_Alters_Died'])]
ego_w1.drop(columns=['Recent_Close_Alter_Died','Recent_Multiple_Alters_Died'],axis=1,inplace=True)

# 3. New School/Job
ego_w1['New_School_Or_Job']=[1 if (x==1)|(y==1) else 0 for x,y in zip(ego_w1['New_School'],ego_w1['New_job'])]
ego_w1.drop(columns=['New_School','New_job'],axis=1,inplace=True)

# 4. Unemployed/retired
ego_w1['Recent_Retired_Or_Unemployed']=[1 if (x==1)|(y==1) else 0 for x,y in zip(ego_w1['Recent_Retired'],ego_w1['Recent_Unemployed'])]
ego_w1.drop(columns=['Recent_Unemployed','Recent_Retired'],axis=1,inplace=True)

# Recent_Break_Up_with_Close_Friends_or_Relatives

ego_w1.to_csv(Path.cwd()/'data/thesis/ego_w1.csv')
