import os
import re
from thesis import params
import numpy as np
import pandas as pd
from pathlib import Path
from linearmodels.panel import PanelOLS

#alter_at_ego_level_3_waves
#alter_at_ego_level
alter_at_ego_level = pd.read_csv(Path.cwd() / 'data/thesis/alter_at_ego_level_3_waves.csv', index_col=0)
ego = pd.read_csv(Path.cwd() / 'data/thesis/ego.csv', index_col=0)
ego.rename(columns={'PRIM_KEY_1': 'PRIM_KEY'}, inplace=True)


# 1. merge data
alter_at_ego_level['PRIM_KEY'] = alter_at_ego_level['PRIM_KEY'].astype('float')
ego['PRIM_KEY'] = ego['PRIM_KEY'].astype('float')

# preprocess
df = pd.merge(left=ego, left_on='PRIM_KEY', right=alter_at_ego_level, right_on='PRIM_KEY')
df['Female_2'] = df['Female_1']
df.loc[df['Age_2'].isna(),'Age_2']= [55,53]


# recent friend died
var_name_1 = 'Recent_kin_died'
var_name_2 = 'Recent_non_kin_died'

new_var_name = 'Recent_Friend_Or_Kin_Died'
new_var_name_1 = new_var_name+'_1'
new_var_name_2 = new_var_name+'_2'
new_var_name_3 = new_var_name+'_3'
df[new_var_name_1]=[1 if (x!=0) | (y!=0) else 0 for x,y in zip(df[var_name_1+'_1'],df[var_name_2+'_1'])]
df[new_var_name_2]=[1 if (x!=0) | (y!=0) else 0 for x,y in zip(df[var_name_1+'_2'],df[var_name_2+'_2'])]
df[new_var_name_3]=[1 if (x!=0) | (y!=0) else 0 for x,y in zip(df[var_name_1+'_3'],df[var_name_2+'_3'])]
# Poor Health
var_name_1 = 'Health_Issue'
var_name_2 = 'Poor_Health'

new_var_name = 'Lower_Health'
new_var_name_1 = new_var_name+'_1'
new_var_name_2 = new_var_name+'_2'
new_var_name_3 = new_var_name+'_3'
df[new_var_name_1]=[1 if (x!=0) | (y!=0) else 0 for x,y in zip(df[var_name_1+'_1'],df[var_name_2+'_1'])]
df[new_var_name_2]=[1 if (x!=0) | (y!=0) else 0 for x,y in zip(df[var_name_1+'_2'],df[var_name_2+'_2'])]
df[new_var_name_3]=[1 if (x!=0) | (y!=0) else 0 for x,y in zip(df[var_name_1+'_3'],df[var_name_2+'_3'])]



# df.to_csv(Path.cwd() / 'data/thesis/merged_df.csv',index=False)

# 3. transform data into long format
columns = df.columns
cols=[]
for column in columns:
    if ('_3' in column):
        df.drop(columns=[column],axis=1,inplace=True)
    column=column.replace('1','').replace('2','').replace('3','')
    if column not in cols:
        cols.append(column)

cols.remove('PRIM_KEY')

# Unpivot df from wide to long format.
df_long = pd.wide_to_long(df, cols, i="PRIM_KEY", j="wave")

df_long.columns

cols = {}
for column in df_long.columns:
    cols[column] = column[:len(column)-1]
df_long.rename(columns=cols, inplace=True)


for column in df_long.columns:
    print(df_long[column].value_counts())
# df_long=df_long.reset_index()








df_long=df_long.reset_index()

df_long.reset_index(inplace=True)

cols_to_fit = ['Know_More','Know_More_Score','Female','PRIM_KEY','wave','Recent_Have_a_Child_Or_Grandchild','Recent_Retired','Recent_Break_Up_with_Close_Friends_or_Relatives','Recent_Important_change_in_marriage','Recent_Major_Problem_on_work_or_school_or_financial',
           'Recent_kin_died','Recent_non_kin_died','New_School_Or_Job','average_knows_year_among_notnull',
           'frequency_among_notnull','Belief_On_Having_Kin_To_Help_With_Serious_Problem',
       'Belief_On_Having_Non-Kin_To_Help_With_Serious_Problem','Recent_Friend_Or_Kin_Died','Lower_Health','Kin','Non_Kin',
               'Confide','Social_Companionship',
               'Poor_Health','Health_Issue','Demanding_and_Support','Advice','Practical_Help','Injury_Helper',
               'Demanding','Social_Support','Reciprocity','Network_Size','Help_out','Same_Race','R_feels_esp_close_to','Same_Gender']

df_to_fit=pd.DataFrame()
for column in cols_to_fit:
    df_to_fit[column]=df_long[column]
    print(column)
    print(df_to_fit[column].isnull().sum())


df_to_fit['Recent_Have_a_Child_Or_Grandchild'].replace({None:0,np.nan:0},inplace=True)
df_to_fit['Recent_Break_Up_with_Close_Friends_or_Relatives'].replace({None:0,np.nan:0},inplace=True)
df_to_fit['Recent_Important_change_in_marriage'].replace({None:0,np.nan:0},inplace=True)
df_to_fit['Recent_Break_Up_with_Close_Friends_or_Relatives'].replace({None:0,np.nan:0},inplace=True)
df_to_fit['Recent_Major_Problem_on_work_or_school_or_financial'].replace({None:0,np.nan:0},inplace=True)
df_to_fit['Recent_Retired'].replace({None:0,np.nan:0},inplace=True)

for column in df_to_fit.columns:
    print(column)
    print(df_to_fit[column].isnull().sum())




df_to_fit.rename(columns={'Social_Support': 'Actual_Support', 'frequency_among_notnull': 'Frequency',
                              'average_knows_year_among_notnull': 'Average_Knowing_Years','Network_size':'Network_Size','Help_out':'Help_Out','R_feels_esp_close_to':'Especially_Close'}, inplace=True)




for KEY in df_to_fit.PRIM_KEY:
    rows = df_to_fit[df_to_fit['PRIM_KEY'] == KEY]
    Know_More_1 = rows.loc[rows['wave'] == 1, 'Know_More'].values
    Know_More_2 = rows.loc[rows['wave'] == 2, 'Know_More'].values
    if (Know_More_1==1) & (Know_More_2 ==0):
        df_to_fit.loc[df_to_fit['PRIM_KEY'] == KEY, 'Change_Type'] = 1 #10
    elif (Know_More_1==0) & (Know_More_2 ==1):
        df_to_fit.loc[df_to_fit['PRIM_KEY'] == KEY, 'Change_Type'] = 2 #01
    else:
        df_to_fit.loc[df_to_fit['PRIM_KEY'] == KEY, 'Change_Type'] = 0  # 01





df_to_fit.to_csv(Path.cwd() / 'data/thesis/data_long_format.csv', index=False)
# df_to_fit.to_csv(Path.cwd() / 'data/thesis/data_long_format_3_waves.csv', index=False)
''',
               'Confide_more','Social_Companionship_more',
               'Demanding_more','Social_Support_more','Reciprocity_more']'''





