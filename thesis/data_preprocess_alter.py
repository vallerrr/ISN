import os
import re
import numpy as np
import pandas as pd
from pathlib import Path
from thesis import params


# Import data
df_alter = pd.read_stata(Path.cwd() / "data/thesis/36975-0004-Alter.dta")


columns = df_alter.columns
# params.check_when_recode('D1B', df_alter, columns)

alter_var_dict = params.alter_var_dict
alter = pd.DataFrame()
alter[['PRIM_KEY','ID_W1_W2_W3','NAME_NMBR2']] = df_alter[['PRIM_KEY','ID_W1_W2_W3','NAME_NMBR2']]
# alter = alter[list(alter_var_dict.keys()) + alter_edges + alter_relationship_types]

# for alters, first deal with the variables in the dictionary
for column, value in alter_var_dict.items():
    if value[1]==False:
        alter[column]=df_alter[column]
        if value[2]:  # multiple waves
            alter[column + '_2'] = df_alter[column + '_W2']
            alter[column + '_3'] = df_alter[column + '_W3']
        else:
            continue
    else:
        alter[column] = df_alter[column].replace(value[1])
        if value[2]:  # multiple waves
            alter[column + '_2'] = df_alter[column + '_W2'].replace(value[1])
            alter[column + '_3'] = df_alter[column + '_W3'].replace(value[1])
        else:
            continue

# frequency
alter_frequency = ['D1F', 'D1G', 'D1H', 'D1F_W2', 'D1G_W2', 'D1H_W2', 'D1F_W3', 'D1G_W3', 'D1H_W3']

temp_frequency = df_alter.loc[:,alter_frequency]
frequency_dict={'At least once a month': 3, 'At least once a week': 4, 'Several times during the year': 2,'Once a year or less': 1, 'At least once a day': 5, 'Never': 0,None:0}
temp_frequency=temp_frequency.apply(lambda x: x.replace(frequency_dict), axis=1)

for index,row in temp_frequency.iterrows():
    temp_frequency.loc[index, 'aggregate_1'] = row['D1F']+row['D1G']+row['D1H']
    temp_frequency.loc[index, 'aggregate_2'] = row['D1F_W2'] + row['D1G_W2'] + row['D1H_W2']
    temp_frequency.loc[index, 'aggregate_3'] = row['D1F_W3'] + row['D1G_W3'] + row['D1H_W3']
alter[['frequency_1','frequency_2','frequency_3']] = temp_frequency[['aggregate_1','aggregate_2','aggregate_3']]


# params.check_when_recode('D1H', df_alter, columns)

# relationship_types
alter_relationship_types = ['C1A', 'C1A_1', 'C1A_2', 'C1A_3', 'C1A_4', 'C1A_5', 'C1A_6', 'C1A_10', 'C1A_11', 'C1A_12',
                            'C1A_13',
                            'C1A_14', 'C1A_20', 'C1A_21', 'C1A_22', 'C1A_23', 'C1A_24', 'C1A_25', 'C1A_26', 'C1A_W2',
                            'C1A_1_W2',
                            'C1A_2_W2', 'C1A_3_W2', 'C1A_4_W2', 'C1A_5_W2', 'C1A_6_W2', 'C1A_10_W2', 'C1A_11_W2',
                            'C1A_12_W2',
                            'C1A_13_W2', 'C1A_14_W2', 'C1A_20_W2', 'C1A_21_W2', 'C1A_22_W2', 'C1A_23_W2', 'C1A_24_W2',
                            'C1A_25_W2', 'C1A_26_W2', 'C1A_W3', 'C1A_1_W3', 'C1A_2_W3', 'C1A_3_W3', 'C1A_4_W3',
                            'C1A_5_W3',
                            'C1A_6_W3', 'C1A_10_W3', 'C1A_11_W3', 'C1A_12_W3', 'C1A_13_W3', 'C1A_14_W3', 'C1A_20_W3',
                            'C1A_21_W3',
                            'C1A_22_W3', 'C1A_23_W3', 'C1A_24_W3', 'C1A_25_W3', 'C1A_26_W3']

alter_relationship_dict = {'C1A_1':'Spouse/Partner','C1A_2':'Romantic','C1A_3':'Parent', 'C1A_4':'Child', 'C1A_5':'Brother/sister',
                           'C1A_6':'OtherRelative', 'C1A_10':'Housemate/Roommate', 'C1A_11':'Neighbor', 'C1A_12':'KnowAtWork', 'C1A_13':'KnowAtSchool',
                           'C1A_14':'KnowAtChurch', 'C1A_20':'Friend', 'C1A_21':'Acquaintance', 'C1A_22':'Know another way', 'C1A_23':'Step-parent',
                           'C1A_24':'Step-child', 'C1A_25':'Step-brother', 'C1A_26': 'Half-brother'}


temp_type = df_alter.loc[:,alter_relationship_types]
temp = temp_type.loc[:,['C1A', 'C1A_W2', 'C1A_W3']]

for index,row in temp.iterrows():
    for column in temp.columns:
        numbers = re.findall(r'\d*',row[column])
        while '' in numbers:
            numbers.remove('')
        if len(numbers)==0:
            numbers=[]
        else:
            numbers=[int(x) for x in numbers]
        temp.loc[index,column] = numbers

alter[['C1A_1', 'C1A_2', 'C1A_3']] = temp[['C1A', 'C1A_W2', 'C1A_W3']]
# kin: 1-6,23-26
# non-kin: 10-14,20-22

# network condensity
'''
alter_edges = ['N1_N2', 'N1_N3', 'N1_N4', 'N1_N5', 'N2_N3', 'N2_N4', 'N2_N5', 'N3_N4', 'N3_N5', 'N4_N5',
               'N1_N2_W2', 'N1_N3_W2', 'N1_N4_W2', 'N1_N5_W2', 'N2_N3_W2', 'N2_N4_W2', 'N2_N5_W2', 'N3_N4_W2',
               'N3_N5_W2', 'N4_N5_W2', 'N1_N2_W3', 'N1_N3_W3', 'N1_N4_W3', 'N1_N5_W3', 'N2_N3_W3', 'N2_N4_W3', 'N2_N5_W3', 'N3_N4_W3',
               'N3_N5_W3', 'N4_N5_W3']



temp_condense = df_alter.loc[:, alter_edges]
# params.check_when_recode('N1_N2', df_alter, columns)
frequency_dict = {'do not know': 0, 'know a little': 1, 'very well': 2, 'something else': 0}
temp_condense = temp_condense.apply(lambda x: x.replace(frequency_dict), axis=1)

temp = pd.DataFrame()


Wave_1_lst = ['N1_N2', 'N1_N3', 'N1_N4', 'N1_N5', 'N2_N3', 'N2_N4', 'N2_N5', 'N3_N4', 'N3_N5', 'N4_N5']
Wave_2_lst = ['N1_N2_W2', 'N1_N3_W2', 'N1_N4_W2', 'N1_N5_W2', 'N2_N3_W2', 'N2_N4_W2', 'N2_N5_W2', 'N3_N4_W2', 'N3_N5_W2','N4_N5_W2']
Wave_3_lst = ['N1_N2_W3', 'N1_N3_W3', 'N1_N4_W3', 'N1_N5_W3', 'N2_N3_W3', 'N2_N4_W3', 'N2_N5_W3', 'N3_N4_W3','N3_N5_W3', 'N4_N5_W3']


count=0
for lst in [Wave_1_lst,Wave_2_lst,Wave_3_lst]:

    count_0 = 0
    count_1 = 0
    count_2 = 0
    print('deal for lst {}'.format(lst))
    for index,row in temp_condense.iterrows():
        for column in lst:
            if row[column]==0:
                count_0+=1
            elif row[column]==1:
                count_1+=1
            elif row[column]==2:
                count_1+=1
            else:
                continue
        temp.loc[index,'wave_'+str(count)+'count_0']=count_0
        temp.loc[index, 'wave_' + str(count) + 'count_1'] = count_1
        temp.loc[index, 'wave_' + str(count) + 'count_2'] = count_2
    count+=1

alter[['wave_1_do_not_know','wave_1_know_little','wave_1_know_well',
       'wave_2_do_not_know','wave_2_know_little','wave_2_know_well',
       'wave_3_do_not_know','wave_3_know_little','wave_3_know_well',]] = temp[temp.columns]
'''
# alter=alter.drop(axis=1,columns=['wave_0_do_not_know','wave_0_know_little','wave_0_know_well'])

# -------------------------------------------------------------------------------------
# part 2 : add alter level data
# -------------------------------------------------------------------------------------

# 2. rename variables

alter_rename_dict = {}
for column in alter.columns:
    wave = column[len(column) - 2:]
    if (wave=='_2') | (wave=='_3'):
        column=column.replace(wave,'')
    else:
        wave='_1'

    if column in alter_var_dict.keys():
        if wave=='_1':
            alter_rename_dict[column] = alter_var_dict[column][0].replace(' ', '_') + wave
        else:
            alter_rename_dict[column+wave] = alter_var_dict[column][0].replace(' ','_')+wave
    elif column=='C1A':
        alter_rename_dict[column + wave]= 'relationship_type'+wave


alter.rename(columns={'C1A_1':'relationship_type_1'},inplace=True)
alter = alter.rename(columns=alter_rename_dict)

# keep data that is not nan in NAME_NMBR2
# alter_w1.dropna(subset=['NAME_NMBR2'],inplace=True,axis=0)


# 2.
alter_at_ego_level = pd.DataFrame()
prim_key = list(set(alter['PRIM_KEY']))
for key in prim_key:
    index = prim_key.index(key)
    rows = alter.loc[alter['PRIM_KEY']==key,]
    alter_number = len(rows)

    alter_at_ego_level.loc[index, 'PRIM_KEY'] = key  # key

    for wave in ['_1','_2','_3']:
        # Interaction type

        alter_at_ego_level.loc[index, 'Social_Companionship'+wave] = rows['Social_Companionship'+wave].notnull().sum()
        alter_at_ego_level.loc[index, 'Demanding'+wave] = rows['Demanding'+wave].notnull().sum()
        alter_at_ego_level.loc[index, 'Advice' + wave] = rows['Advice' + wave].notnull().sum()
        alter_at_ego_level.loc[index, 'Practical_Help' + wave] = rows['Practical_help' + wave].notnull().sum()
        alter_at_ego_level.loc[index, 'Injury_Helper' + wave] = rows['Injury_Helper' + wave].notnull().sum()
        alter_at_ego_level.loc[index, 'Help_out' + wave] = rows['Help_out' + wave].notnull().sum()
        alter_at_ego_level.loc[index, 'Confide' + wave] = rows['Confide' + wave].notnull().sum()

        # network size
        size = rows[['Help_out' + wave,'Confide' + wave,'Social_Companionship'+wave,'Demanding'+wave,'Advice' + wave,'Practical_help' + wave,'Injury_Helper' + wave]]
        size= size.dropna(how='all')
        alter_at_ego_level.loc[index, 'Network_Size'+ wave] = len(size)


        # subjective feeling
        # alter_at_ego_level.loc[index, 'Respondent_be_obliged_to_help' + wave] = rows['R_would_be_obliged_to_help' + wave].notnull().sum()
        alter_at_ego_level.loc[index, 'R_feels_esp_close_to'+ wave] = rows['R_feels_esp_close_to'+ wave].sum()

        # homophily
        alter_at_ego_level.loc[index, 'Same_Race' + wave] = rows['same_race-ethnicity' + wave].notnull().sum()
        alter_at_ego_level.loc[index, 'Same_Gender' + wave] = rows['same_gender_as_R' + wave].sum()

        # knowing years and frequency
        year_response = rows['How_long_R_knows_sub-name_(years)'+ wave].notnull().sum()
        if year_response==0:
            alter_at_ego_level.loc[index, 'average_knows_year_among_notnull' + wave] =None
        else:
            alter_at_ego_level.loc[index, 'average_knows_year_among_notnull'+ wave]=rows['How_long_R_knows_sub-name_(years)'+ wave].sum()/year_response
        # average frequency among not_null
        fre_response = rows.loc[rows['frequency' + wave] != 0,'frequency'+ wave].count()
        if fre_response==0:
            alter_at_ego_level.loc[index, 'frequency_among_notnull' + wave] = None
        else:
            alter_at_ego_level.loc[index, 'frequency_among_notnull'+ wave] = rows['frequency'+ wave].sum()/fre_response

        # rename column names

        kin,non_kin=0,0
        non_kin_lst = ['10', '11', '12', '13', '14','20','21','22']
        kin_lst = ['1','2','3','4','5','6','23','24','25','26']

        social_support_count = 0
        reciprocity_count = 0
        Demanding_and_Support_count=0
        for ind,row in rows.iterrows():
            # print(row['relationship_type'])

            if ~np.isnan(row['Injury_Helper'+wave]) | ~np.isnan(row['Practical_help'+wave]) | ~np.isnan(row['Advice'+wave]):
                social_support_count+=1
                support=True
                if support:
                    if ~np.isnan(row['Demanding'+wave]):
                        Demanding_and_Support_count+=1
                    if ~np.isnan(row['Injury_Helper'+wave]):
                        reciprocity_count+=1
            relationship_type = re.findall('\d*',str(row['relationship_type'+ wave]))
            for i in relationship_type:
                if i in kin_lst:
                    kin += 1
                elif i in non_kin_lst:
                    non_kin += 1
        alter_at_ego_level.loc[index, 'Kin' + wave] = kin
        alter_at_ego_level.loc[index, 'Non_Kin' + wave] = non_kin

        alter_at_ego_level.loc[index, 'Social_Support' + wave] = social_support_count
        alter_at_ego_level.loc[index, 'Reciprocity' + wave] = reciprocity_count
        alter_at_ego_level.loc[index, 'Demanding_and_Support' + wave] = Demanding_and_Support_count


# alter_at_ego_level.to_csv(Path.cwd()/'data/thesis/alter_at_ego_level_3_waves.csv')

