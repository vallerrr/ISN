
def var_name_check(key_word, columns):
    # print the relevant var names in the df.columns
    for i in columns:
        if key_word in i:
            print(i)


def check_when_recode(varname,df,columns):

    print(df[varname].value_counts())
    check_continue = input('continue to recode dictionary? 0 to stop, anything to continue')
    if check_continue != '0':
        temp = df[varname].value_counts()
        index = list(temp.index)
        dict = {}
        for i in index:
            replace_value = input('for {}, you want to replace with'.format(i))
            replace_value = None if replace_value == 'None' else int(replace_value)
            dict[i] = replace_value
        print(dict)
        var_name_check(varname, columns)
    else:
        var_name_check(varname, columns)

# check_when_recode('E2A_W2',df=df_ego, columns=df_ego.columns)



ego_var_dict = {  # key:['explanation',replace dictionary, multi-waves]
    'PRIM_KEY': ['PRIM_KEY', None, False],
    'GENDER': ['Female', {'2 Female': 1, '1 Male': 0, 2: 0}, True],

    'E1A':['Belief On Having Kin To Help With Serious Problem',{'1 Definitely have': 3, '2 Probably have': 2, '4 Probably dont have': 0, '3 Might have': 1, '5 Int: Volunteered: Other: ~e1a_other': None},True],
    'E2A': ['Belief On Having Non-Kin To Help With Serious Problem',{1: 3, 2: 2, 3: 1, 4: 0, 5: None,'1 Definitely have': 3, '2 Probably have': 2, '3 Might have': 1, "4 Probably don't have": 0, '5 Int: Volunteered: Other: ~e2a_other': None}, True],

    'E3':['Know More Personal Concerns',{'2 Know enough already': 0, '1 Wish I knew more': 1, '3 Int: Volunteered: Other: ~e3_other': 0},True],
    'E4': ['Know More Good Time',
           {'1 Wish I knew more': 1, '2 Know enough already': 0, '3 Int: Volunteered: Other: ~e4_other': 0}, True],
    'E5':['Know More Sick Help',{'2 Know enough already': 0, '1 Wish I knew more': 1, '3 Int: Volunteered: Other: ~e5_other': 0},True],

    # 'BEGINTIME': 'Interview Time',
    'AGE': ['Age', None, True],
    'AGEGROUP': ['Younger Group', {'50-70':0,'21-30':1,'older':0,'younger':1},True],

    'K3': ['Degree Above Bachelor', {'7 Bachelors degree': 1, '8 Masters degree': 1, '5 Some college': 1, '9 Higher professional degree (like MD, JD, or PhD)': 1, '3 High school graduate': 0, '6 Associate degree': 0, '10 Other: ~k1_other': 0, '4 GED or equivalent': 0, '2 9th grade to 12th grade, but did not graduate': 0, '1 Less than 9th grade': 0},True],

    'K9A': ['Local Born', {'1 U.S.A.': 1, '15 Other:': 0, '3 China (including Taiwan)': 0, '7 India': 0, '12 Philippines': 0, '13 U.K.': 0, '2 Canada': 0, '5 Germany': 0, 14.0: 0, '8 Iran':0, '9 Japan':0, '10 Korea': 0, '11 Mexico': 0},False],

    'A2A': ['Married', {'5 Never married': 0, '1 Married': 1, '3 Divorced': 0, '2 Widowed': 0, '4 Separated': 0},True],
    'K15': ['Has Religion', {'7 No religion': 0, '6 Other: Specify: ~k15_other': 1, '2 Catholic': 1, '1 Protestant': 1, '3 Jewish': 1, '5 Buddhist': 1, '4 Muslim': 1},True],
    # 'K16': ['Religion been raised', {'2 Catholic': 2, '1 Protestant': 1, '7 No religion': 6, '6 Other: Specify: ~k16_other': 0, '3 Jewish': 3, '5 Buddhist': 5, '4 Muslim': 4},False],
    # 'K17': ['Religion of partner 2013', {'2 Catholic': 2, '1 Protestant': 1, '7 No religion': 6, '6 Other: Specify: ~k16_other': 0, '3 Jewish': 3, '5 Buddhist': 5, '4 Muslim': 4},False],
    'A21': ['Unemployed',{'1': 0, '6': 0, '2': 0, '3': 0, '8': 0, '4': 1, '2-3': 0, '1-3': 0, '3-2': 0, '5': 1, '2-6': 0, '7': 0, '6-8': 0, '2-8': 0, '6-7': 0, '3-4': 0, '6-2': 0, '2-7': 0, '4-8': 1, '3-5': 0, '1-7': 0, '3-1': 0, '1-8': 0, '8-6': 0, '4-3': 0, '8-1': 0, '3-8': 0, '6-1': 0, '1-3-8': 0, '4-7': 1, '.e': 0, '5-7': 1, '2-3-7': 0, '4-2': 0, '5-8': 1,'6-8-7':0,'8-5':1,'5-6-7': 0,'5-6-8':0,'6-8-5':0, '6-5-7': 0, '8-6-7-5-3': 0, '8-4-7': 1, '2-3-8': 0, '7-8-2':0,'8-7': 0, '6-4': 0, '6-4-2': 0, '3-7': 0, '2-6-8': 0, '5-7-8': 1, '7-2': 0, '7-5': 1, '6-7-8': 0, '6-2-8': 0, '2-4-8': 0, '7-8': 0, '4-6': 0, '6-7-4-8': 0, '1-4-8': 0, '6-3': 0,'8-5-6':0 ,'5-6': 0, '5-8-7': 0,'7-5-8':0, '1-8-4': 0, '8-2': 0, '0':0, '6-2-3':0, '2-6-7':0, '7-4-2':1, '7-6':0, '1-6-7' :0,'1-6':0, '8-4':1,'8-3':0, '5-6-7-8':1,'8-3-1':0, '6-3-7':0,'8-2-5':0,'2-3-4':0,'3-7-2':0,'3-1-8':0,'6-7-8-4':0,'4-7-8':0 ,'8-6-4':0, '2-7-8':0, '6-7-2':0, '6-3-8':0, '7-6-2':0, '7-2-8':0, '4-2-8':0,'2-4':0,'6-2-7':0,'2-5':0,},True],

    # Income
    'K21A': ['Household Income',{'8 H $100,000 to $124,999': 8, '10 J $150,000 to $199,999': 10, '6 F $60,000 to $74,999': 6, '7 G $75,000 to $99,999': 7, '11 K $200,000 to $299,999': 11, '5 E $45,000 to $59,999': 5, '9 I $ 125,000 to $149,999': 9, '12 L $300,000 to $499,999': 12, '4 D $35,000 to $44,999': 4, '13 M $500,000 or more': 13, '2 B $15,000 to $24,999': 2, '3 C $25,000 to $34,999': 3, '1 A Under $15,000': 1},True],
    'K21B': ['Personal Income>50000',{'1 Lower': 1, '2 Higher': 2, '3 About $80,000': 3}, True],
    # 'K22D_W2': ['Income compared at 16y 2016',{'Average': 3, 'Above average': 4, 'Below average': 2, 'Far above average': 5, 'Far below average': 1, "Don't know": 0},False],

    # life Events
    'F5A':['Recent Have a Child Or Grandchild',{'3 No': 0, '2 Yes, a grandchild': 1, '1 Yes, a child': 1},True],
    'A25':['Recent New Job', {0.0: 1, 1.0: 1, 2.0: 0, 3.0: 0, 4.0: 0, 5.0: 0, 15.0: 0, 10.0: 0, 11.0: 0, 8.0: 0, 25.0: 0, 6.0: 0, 30.0: 0, 14.0: 0, 12.0: 0, 17.0: 0, 20.0: 0, 9.0: 0, 7.0: 0, 18.0: 0, 13.0: 0, 28.0: 0, 24.0: 0, 16.0: 0, 40.0: 0, 35.0: 0, 26.0: 0, 34.0: 0, 21.0: 0, 33.0: 0, 19.0: 0, 45.0: 0, 23.0: 0, 22.0: 0, 29.0: 0, 31.0: 0, 39.0: 0, 36.0: 0, 37.0: 0, 2007.0: 0, 27.0: 0, 42.0: 0, 44.0: 0},True],
    'A27':['Recent New School', {0.0: 1, 2.0: 0, 1.0: 1, 3.0: 0, 4.0: 0, 5.0: 0, 6.0: 0, 8.0: 0, 9.0: 0},True],
    'A32':['Recent Retired', {3.0: 0, 0.0: 1, 5.0: 0, 2.0: 0, 1.0: 1, 10.0: 0, 6.0: 0, 7.0: 0, 8.0: 0, 4.0: 0, 11.0: 0, 12.0: 0, 15.0: 0, 9.0: 0, 13.0: 0, 14.0: 0, 25.0: 0, 17.0: 0, 108.0: 0, 32.0: 0, 16.0: 0, 26.0: 0, 21.0: 0, 20.0: 0, 36.0: 0, 24.0: 0,43:0,27:0},True],
    'F12A':['Recent Break Up with Close Friends or Relatives',{'2 No': 0, '1 Yes': 1},True],
    'F10A': ['Recent Important change in marriage',{'2 No': 0, '1 Yes': 1}, True],

    'F1A':['Recent Major Problem at work',{'2 No': 0, '1 Yes': 1},True],
    'F1D':['Recent Major Problem at School',{'2 No': 0, '1 Yes': 1},True],
    'F2A': ['Recent Major Financial Problem',{'2 No': 0, '1 Yes': 1},True],

    # Life Events Impact


    ## Tie Dissolution Event
    'F11C':['Recent Close Alter Died',{'4 Other relative': 1, '5 Friend': 2, '6 Someone else: ~f11c_other': 2, '2 Parent': 1, '1 Spouse/partner': 1},True],
    'F11E':['Recent Multiple Alters Died',{'': None, '5': 2, '4': 1, '4-5': 3, '4-6': 3, '6': 2, '2-5': 3, '5-4': 3, '2-4': 1, '5-6': 2, '1-4': 1, '2-4-5': 3, '2-6': 3, '6-4': 3, '6-5': 2, '4-2': 1, '5-6-4': 3, '4-5-6': 3, '.n': None, '2': 1, '2-6-5': 3, '2-3-4': 1, '1-5': 3},True],



    # Health Issue
    'G2': ['Health Issue',
           {'5': 0, '4': 1, '3': 1, '2': 1, '1': 1, '2-4': 1, '1-3': 1, '2-3': 1, '3-4': 1, '1-2': 1, '3-2': 1,
            '1-3-2': 1, '.n': None, '1-3-4': 1, '1-4': 1, '1-2-3-4': 1, '2-3-4': 1, '4-1': 1, '4-3-2': 1, '4-2': 1,
            '3-1': 1, '1-2-4': 1, '1-2-3': 1, '.d': None, '3-2-4': 1, '2-1-4': 1, '4-3': 1, '3-2-1-4': 1, '4-1-2': 1,
            '3-1-4': 1, '2-3-1': 1, '2-1': 1,'0':None, '.e':None, '3-4-1': 1}, True],
    'G3A':['Health Issue Impact',{'1 A lot': 2, '2 Some': 1, '3 Not that much': 0, '4 Int: Volunteered: ~f13c_othercnt': 0},False],
    'G7': ['Poor Health',
           {'9': 0, '6': 1, '1': 1, '4': 1, '5': 1, '4-6': 1, '1-6': 1, '2': 1, '5-6': 1, '1-2': 1, '1-5': 1, '3': 1,
            '1-5-6': 1, '6-4': 1, '1-4': 1, '4-5-6': 1, '1-2-5': 1, '2-6': 1, '1-2-5-6': 1, '1-3': 1, '1-4-5': 1,
            '2-5': 1, '1-4-6': 1, '1-2-6': 1, '1-3-5': 1, '1-4-5-6': 1, '1-2-4-5-6': 1, '3-6': 1, '2-5-6': 1, '4-5': 1,
            '5-4': 1, '3-5-6': 1, '2-4-5': 1, '3-5': 1, '1-2-4': 1, '5-1': 1, '4-2': 1, '4-1': 1, '2-1': 1, '1-2-3': 1,
            '2-1-5-6': 1, '1-3-4': 1, '1-3-6': 1, '2-6-5': 1, '1-2-3-4-5-6': 1, '1-2-3-6': 1, '1-6-4-5': 1, '4-5-3': 1,
            '1-2-3-4-6': 1, '2-1-4': 1, '.d': None, '6-2': 1, '2-1-3-5-6': 1, '2-5-1': 1, '1-2-4-5': 1, '.r': None,
            '4-5-6-1': 1, '1-6-5': 1, '2-4-1': 1, '6-1-4': 1, '2-4': 1, '6-5': 1, '2-3-4-6': 1, '1-2-5-4': 1,
            '1-2-4-6-5': 1, '2-3-4': 1, '1-2-3-5': 1, '1-6-2': 1, '1-3-4-6': 1, '3-4-5-6': 1, '2-4-5-6': 1, '4-6-2': 1,
            '1-5-2': 1, '1-3-4-5': 1, '2-3': 1, '5-1-2-3-4-6': 1, '5-1-6': 1, '1-3-5-6': 1, '2-5-4': 1, '1-3-4-5-6': 1,
            '4-3': 1,'0': 1, '6-3': 1, '6-1-5': 1, '2-1-5': 1, '.e': None, '1-5-4': 1, '5-2': 1, '2-1-6'
            '1-2-6-5': 1, '2-1-3-4-5-6': 1, '2-3-4-5': 1, '3-4-5': 1, '4-2-5-1': 1, '1-4-3': 1, '1-2-3-4-5'
            '1-2-3-5-6': 1, '6-5-4': 1, '2-1-4-5': 1, '1-6-4': 1, '3-6-1': 1, '3-4-6': 1, '3-4-5-6-2': 1, '3-1-5'
            '1-2-6-4-5': 1, '1-5-3-6': 1, '1-2-3-6-5': 1, '1-2-4-6': 1, '4-5-6-2': 1, '2-4-6': 1,'1': 1, '0': 0, '1-2-3-5-6': 1, '1-2-4-3-5': 1, '2-3-5': 1, '3-4': 1, '1-6-5-2-3': 1, '6-1': 1, '5-6-4-3': 1, '4-1-5': 1, '5-3-6': 1, '3-5-6-4': 1, '4-5-1-3': 1, '4-2-1-6': 1, '4-5-2': 1, '2-4-5-6-1': 1, '1-3-2': 1, '6-4-3': 1, '5-3': 1, '4-5-1': 1, '3-6-5': 1, '4-6-5': 1}, True],


    # 'H18': ['Sexual Orientation',{'1 Heterosexual or straight': 0, '3 Something else': 0, '2 Homosexual or gay': 1}, False],
    'WT_W1_DEM_95_INF': ['Weights 95',None,False],
    'WEIGHT_W1_DEMO':['Weights',None,False]}


# check_when_recode('B6B',df_alter,df_alter.columns)
alter_var_dict = {

    'B2A': ['Social Companionship',False,True],
    'B4A': ['Confide', False,True],
    'B5A': ['Advice', False,True],
    'B8A': ['Help out', False, True],
    'B6B': ['Practical help',False,True],
    'B7C': ['Injury Helper', False, True],
    'B9A': ['Demanding', False, True],


    # Demographic
    'C1C_NOLDER': ['6y older than R',{'yes': 1, 'no': 0, 'missing': None}, True],

    'C1B_NSAMESEX': ['same gender as R',{'yes': 1, 'no': 0, 'missing': None},True],


    'N_GENDER': ['Gender',{'female': 2, 'male': 1, 9.0: None},True],

    'C2G_NSAMERACE': ['same race-ethnicity',{'yes': 1, 'no': 0, 'missing': None},True],

    'D1C': ['Does sub-name have spouse?',{'yes': 1, 'no': 0, "don't know": None, 4.0: None},True],
    'D1B': ['How long R knows sub-name (years)',False,True],

    'C2B_NCLOSE': ['R feels esp close to',{'yes': 1, 'no': 0, 'missing': None},True],

    # 'C2E3_NALSOHOME': ['Also cares for home',{'wave 1 only': False, 'no': 0, 'yes': 1, 'missing': None,8.0: None},True],

    'D1K': ['R would be obliged to help', {'I would feel very obligated': 3, 'I would feel somewhat obligated': 2, 'I would not feel obligated': 0, 'I would feel a little obligated': 1}, False],

    # 'D1F': ['How often R sees sub-name',{'At least once a month': 3, 'At least once a week': 4, 'Several times during the year': 2,'Once a year or less': 1, 'At least once a day': 5, 'Never': 0}, True],

    # 'D1G': ['How often talks on phone to sub-name',{'At least once a month': 3, 'At least once a week': 4, 'Several times during the year': 2,'Once a year or less': 1, 'At least once a day': 5, 'Never': 0}, True],

}


'''

    'F5B': ['Recent Have a Child Or Grandchild Impact',{'1 A lot': 2, '3 Not that much': 0, '2 Some': 1, '4 Int: Volunteered: ~f5b_other': 0},False],
    'A25A':['Recent New Job Impact',{'1 A lot': 2, '2 Some': 1, '3 Not that much': 0, '4 Int: Volunteered: Other: ~a25a_other': 0}, False],
    'A27A':['Recent New School Impact',{'1 A lot': 2, '2 Some': 1, '3 Not that much': 0, '4 Int: Volunteered: Other: ~a27a_other': 0}, False],

    'A32B':['Recent Retired Impact',{'1 A lot': 2, '2 Some': 1, '3 Not that much': 0, '4 Int: Volunteered: Other: ~a32b_other': 0}, False],
    'A30B':['Recent Unemployed Impact',{'1 A lot': 2, '3 Not that much': 0, '2 Some': 1, '4 Int: Volunteered: Other: ~a30b_other': 0}, False],
    'F12B': ['Recent Break Up with Close Friends or Relatives Impact', {'2 Some': 1, '1 A lot': 2, '3 Not that much': 0, '4 Int: Volunteered: ~f12b_other': 0}, False],

    ## Recent Major Problem Impact = F1B+F1E+F2B
    'F1B':['Recent Major Problem at work Impact',{'1 A lot': 2, '2 Some': 1, '3 Not that much': 0, '4 Int: Volunteered: ~f1b_other': 0}, False],
    'F1E':['Recent Major Problem at School Impact',{'1 A lot': 2, '2 Some': 1, '3 Not that much': 0, '4 Int: Volunteered: ~f1e_other': 0}, False],
    'F2B':['Recent Major Financial Problem Impact',{'1 A lot': 2, '2 Some': 1, '3 Not that much': 0, '4 Int: Volunteered: ~f2b_other': 0},False],
'''
