import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression, LogisticRegressionCV
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from pathlib import Path
import statsmodels.api as sm
import seaborn as sns
import scipy.stats as stats
import matplotlib.pyplot as plt
import shap
import xgboost
# define dataset
# define the model
df=pd.read_csv(Path.cwd() / 'data/thesis/merged_df.csv')
df_regression = pd.read_csv('/Users/valler/Documents/Oxford/MPhil/2021HT Social Network/social_network/data/thesis/regression_data.csv',index_col=0)
prim_key = list(set(df_regression['PRIM_KEY']))





df['Change']=0
df['Change_01']=0
df['Change_10']=0
for key in prim_key:
	df.loc[df['PRIM_KEY'] == key, 'Change'] = 1
	if df.loc[df['PRIM_KEY']==key,'Know_More_1'].values==0:
		df.loc[df['PRIM_KEY'] == key, 'Change_01'] = 1
	if df.loc[df['PRIM_KEY']==key,'Know_More_1'].values==1:
		df.loc[df['PRIM_KEY'] == key, 'Change_10'] = 1






# df_classification['Household_Income_1'].isnull().sum() 643

# Null check


df['Recent_Have_a_Child_Or_Grandchild_1'].replace({None:0,np.nan:0},inplace=True)
df['Recent_Break_Up_with_Close_Friends_or_Relatives_1'].replace({None:0,np.nan:0},inplace=True)
df['Recent_Important_change_in_marriage_1'].replace({None:0,np.nan:0},inplace=True)
df['Recent_Break_Up_with_Close_Friends_or_Relatives_1'].replace({None:0,np.nan:0},inplace=True)
df['Recent_Major_Problem_on_work_or_school_or_financial_1'].replace({None:0,np.nan:0},inplace=True)
df['Recent_Retired_1'].replace({None:0,np.nan:0},inplace=True)
df['Poor_Health_1'].replace({None:0,np.nan:0},inplace=True)
df['Degree_Above_Bachelor_1'].replace({None:0,np.nan:0},inplace=True)
df['Local_Born_1'].replace({None:0,np.nan:0},inplace=True)
df['Has_Religion_1'].replace({None:0,np.nan:0},inplace=True)
for column in df.columns:
	if '_1' in column:
		print(column)


# start from here



demographic_variables = ['Female_1','Younger_Group_1','Degree_Above_Bachelor_1','Local_Born_1','Married_1','Has_Religion_1','Unemployed_1']
# 1. non-cross wave change fixed effects: demographics
df_demographics = pd.pivot_table(df,index='Change',values=demographic_variables,aggfunc=np.mean)
df_demographics.rename(columns={x:y.replace('_1','').replace('_',' ') for x,y in zip(df_demographics.columns,df_demographics.columns)},inplace=True)


plt.rcParams["figure.figsize"] = [12,5]
plt.rcParams.update({'font.size': 11})
fig,ax=plt.subplots()
fig.subplots_adjust(left=0.2, top=0.95)

x = np.arange(len(df_demographics.columns))  # the label locations
width = 0.4  # the width of the bars

rects1 = ax.barh(x - width/2, df_demographics.iloc[1,:], width, label='Changed Attitude')
rects2 = ax.barh(x + width/2, df_demographics.iloc[0,:], width, label='Non-Changed Attitude')
labels=df_demographics.columns
# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_xlabel('Mean in each group')
ax.set_yticks(x, labels)
ax.legend()

ax.bar_label(rects1, padding=3,fmt='%.2f')
ax.bar_label(rects2, padding=3,fmt='%.2f')

ax.set_ylabel('Percentage in each group')
# ax.set_title('Demographic Comparisons at wave one between people who have changed their satisfaction over time')


ax.set_axisbelow(True)
ax.grid(alpha=0.4,linestyle='--',axis='x')
plt.savefig(Path.cwd()/'thesis/graphs/graph1.pdf')
plt.show()

# t-test

# -----------------------------------------------------------------------------------
# 2. Other Variables

network_vars = ['Social_Companionship_1','Demanding_1','Advice_1','Practical_Help_1','Injury_Helper_1','Help_out_1','Confide_1','Network_Size_1','average_knows_year_among_notnull_1','frequency_among_notnull_1','Kin_1','Non_Kin_1']

df_networks_1 = pd.pivot_table(df,index='Change',values=network_vars,aggfunc=np.mean)
df_networks_1.rename(columns={x:y.replace('_1','').replace('_',' ') for x,y in zip(df_networks_1.columns,df_networks_1.columns)},inplace=True)
df_networks_1.rename(columns={'average knows year among notnull':'Years','frequency among notnull':'Frequency','Social Companionship':'Companionship'},inplace=True)



df_networks_2 = pd.pivot_table(df,index='Change',values=[x.replace('1','2') for x in network_vars],aggfunc=np.mean)
df_networks_2.rename(columns={x:y.replace('_2','').replace('_',' ')for x,y in zip(df_networks_2.columns,df_networks_2.columns)},inplace=True)
df_networks_2.rename(columns={'average knows year among notnull':'Years','frequency among notnull':'Frequency','Social Companionship':'Companionship'},inplace=True)




plt.rcParams["figure.figsize"] = [12,10]
plt.rcParams.update({'font.size': 11})
fig,(ax1,ax2)=plt.subplots(2,1)
fig.subplots_adjust(right=0.98,top=0.95,bottom=0.05)
x = np.arange(len(df_networks_1.columns))  # the label locations
width = 0.4  # the width of the bars

rects1 = ax1.barh(x - width/2, df_networks_1.iloc[1,:], width, label='Changed Attitude')
rects2 = ax1.barh(x + width/2, df_networks_1.iloc[0,:], width, label='Non-Changed Attitude')
labels=df_networks_1.columns
# Add some text for labels, title and custom x-axis tick labels, etc.
ax1.set_xlabel('Mean in each group')
ax1.set_yticks(x, labels)
ax1.legend()

ax1.bar_label(rects1, padding=3,fmt='%.2f')
ax1.bar_label(rects2, padding=3,fmt='%.2f')

ax1.grid(alpha=0.4,linestyle='--',axis='y')
ax1.set_ylabel('Mean in each group')
ax1.set_title('Wave One')

rects1 = ax2.barh(x - width/2, df_networks_2.iloc[1,:], width, label='Changed Attitude')
rects2 = ax2.barh(x + width/2, df_networks_2.iloc[0,:], width, label='Non-Changed Attitude')
labels=df_networks_2.columns
# Add some text for labels, title and custom x-axis tick labels, etc.
ax2.set_xlabel('Mean in each group')
ax2.set_yticks(x, labels)
ax2.legend()

ax2.bar_label(rects1, padding=3,fmt='%.2f')
ax2.bar_label(rects2, padding=3,fmt='%.2f')

ax2.grid(alpha=0.4,linestyle='--',axis='x')
ax2.set_ylabel('Mean in each group')
ax2.set_title('Wave Two')

ax1.tick_params(axis='both', which='major', labelsize=12)

ax2.tick_params(axis='both', which='major', labelsize=10)

#'Network Characteristic Comparisons at wave two between people who have/ have not changed their satisfaction')
plt.savefig(Path.cwd()/'thesis/graphs/graph2.pdf')
plt.show()


# -----------------------------------------------------------------------------------
# 3. want to know more


plt.rcParams["figure.figsize"] = [12,8]
plt.rcParams.update({'font.size': 11})
fig,(ax1,ax2)=plt.subplots(1,2)
fig.subplots_adjust(top=0.95)
x= ['Know More','Personal \n Concerns','Good Time','Sick Help']
y0=np.array([158,0,0,0])
y1= np.array([329,0,0,0])
y2=np.array([225,0,0,0])
y3=[0,df['Know_More_Personal_Concerns_1'].sum(),df['Know_More_Good_Time_1'].sum(),df['Know_More_Sick_Help_1'].sum()]

ax1.bar(x, y0, color='steelblue')
ax1.bar(x, y1, bottom=y0,color='salmon')
ax1.bar(x, y2, bottom=y0+y1, color='wheat')
ax1.bar(x, y3, bottom=y0+y1+y2, color='darkgrey')
ax1.set_ylabel("Counts")
ax1.legend(["Triple Types","Single Type", "Double Types", ])
ax1.set_title("Know More Counts in Wave 1")
ax1.set_ylim(0, 750)
values_1 = [158, 329, 225]
kx, ky = -0.3, 50
count = 0
for i, rec in enumerate(ax1.patches):

	if (rec.get_xy()[1] != 0) & (rec.get_xy()[0] == -0.4):
			# print(rec.get_xy(),rec.get_height())
			ax1.text(rec.get_xy()[0] + rec.get_width() / 2 + kx, rec.get_xy()[1] -ky,
					 "{}\n{:.2%}".format(values_1[count], values_1[count] / sum(values_1)))

			count += 1
	elif( rec.get_height() !=0) & (rec.get_height()!=158):
			print(int(rec.get_height()))
			ax1.text(rec.get_xy()[0] + rec.get_width() / 2-0.15 , rec.get_height()-ky,
					'{}'.format( int(rec.get_height())), fontsize=12, color='black')



#
# df['Know_More_Score_2'].value_counts()
y20=np.array([135,0,0,0])
y21= np.array([189,0,0,0])
y22=np.array([264,0,0,0])
y23=[0,df['Know_More_Personal_Concerns_2'].sum(),df['Know_More_Good_Time_2'].sum(),df['Know_More_Sick_Help_2'].sum()]
ax2.bar(x, y20, color='steelblue')
ax2.bar(x, y21, bottom=y20,color='salmon')
ax2.bar(x, y22, bottom=y20+y21, color='wheat')
ax2.bar(x, y23, bottom=y20+y21+y22, color='darkgrey')
ax2.set_ylim(0, 750)
ax2.set_ylabel("Counts")
ax2.legend(["Triple Types","Single Type", "Double Types", ])
ax2.set_title("Know More Counts in Wave 2")


values_1 = [135, 189, 264]
kx, ky = -0.3, 50
count = 0
for i, rec in enumerate(ax2.patches):

	if (rec.get_xy()[1] != 0) & (rec.get_xy()[0] == -0.4):
			# print(rec.get_xy(),rec.get_height())
			ax2.text(rec.get_xy()[0] + rec.get_width() / 2 + kx, rec.get_xy()[1] -ky,
					 "{}\n{:.2%}".format(values_1[count], values_1[count] / sum(values_1)))

			count += 1
	elif( rec.get_height() !=0) & (rec.get_height()!=135):
			print(int(rec.get_height()))
			ax2.text(rec.get_xy()[0] + rec.get_width() / 2-0.15 , rec.get_height()-ky,
					'{}'.format( int(rec.get_height())), fontsize=12, color='black')


plt.savefig(Path.cwd()/'thesis/graphs/graph3.pdf')
plt.show()


# 4. Know More Type Dynamics
df_change_01=df.loc[df['Change_01']==1,]
df_change_10=df.loc[df['Change_10']==1,]


plt.rcParams["figure.figsize"] = [12,8]
plt.rcParams.update({'font.size': 11})
fig,(ax1,ax2)=plt.subplots(1,2)
fig.subplots_adjust(top=0.95)
x= ['Know More','Personal \n Concerns','Good Time','Sick Help']
y0=np.array([92,0,0,0])
y1= np.array([34,0,0,0])
y2=np.array([5,0,0,0])
y3=[0, df_change_10['Know_More_Personal_Concerns_1'].sum(),df_change_10['Know_More_Good_Time_1'].sum(),df_change_10['Know_More_Sick_Help_1'].sum()]

ax1.bar(x, y0, color='steelblue')
ax1.bar(x, y1, bottom=y0,color='salmon')
ax1.bar(x, y2, bottom=y0+y1, color='wheat')
ax1.bar(x, y3, bottom=y0+y1+y2, color='darkgrey')
ax1.set_ylabel("Counts")
ax1.legend(["Single Type", "Double Types","Triple Types",])
ax1.set_title("From Unsatisfied to Satisfied")
ax1.set_ylim(0, 150)
values_1 = [ 92, 34,5]
kx, ky = -0.3, 10
count = 0
for i, rec in enumerate(ax1.patches):

	if (rec.get_xy()[1] != 0) & (rec.get_xy()[0] == -0.4):
			# print(rec.get_xy(),rec.get_height())
			if values_1[count]==5:
				ax1.text(rec.get_xy()[0] + rec.get_width() / 2 + kx, rec.get_xy()[1] -5,
						 "{}\n{:.2%}".format(values_1[count], values_1[count] / sum(values_1)))

			else:

				ax1.text(rec.get_xy()[0] + rec.get_width() / 2 + kx, rec.get_xy()[1] -ky,
					 "{}\n{:.2%}".format(values_1[count], values_1[count] / sum(values_1)))

			count += 1
	elif( rec.get_height() !=0) & (rec.get_height()!=92):
			print(int(rec.get_height()))
			ax1.text(rec.get_xy()[0] + rec.get_width() / 2-0.15 , rec.get_height()-ky,
					'{}'.format( int(rec.get_height())), fontsize=12, color='black')



#
# df_change_01.Know_More_Score_2.value_counts()
y20=np.array([63,0,0,0])
y21= np.array([26,0,0,0])
y22=np.array([14,0,0,0])
y23=[0,df_change_01['Know_More_Personal_Concerns_2'].sum(),df_change_01['Know_More_Good_Time_2'].sum(),df_change_01['Know_More_Sick_Help_2'].sum()]
ax2.bar(x, y20, color='steelblue')
ax2.bar(x, y21, bottom=y20,color='salmon')
ax2.bar(x, y22, bottom=y20+y21, color='wheat')
ax2.bar(x, y23, bottom=y20+y21+y22, color='darkgrey')
ax2.set_ylim(0, 150)
ax2.set_ylabel("Counts")
ax2.legend(["Single Type", "Double Types","Triple Types", ])
ax2.set_title("From Satisfied to Unsatisfied")


values_1 = [63, 26, 14]
kx, ky = -0.3, 10
count = 0
for i, rec in enumerate(ax2.patches):

	if (rec.get_xy()[1] != 0) & (rec.get_xy()[0] == -0.4):
			# print(rec.get_xy(),rec.get_height())
			ax2.text(rec.get_xy()[0] + rec.get_width() / 2 + kx, rec.get_xy()[1] -ky,
					 "{}\n{:.2%}".format(values_1[count], values_1[count] / sum(values_1)))

			count += 1
	elif( rec.get_height() !=0) & (rec.get_height()!=63):
			print(int(rec.get_height()))
			ax2.text(rec.get_xy()[0] + rec.get_width() / 2-0.15 , rec.get_height()-ky,
					'{}'.format( int(rec.get_height())), fontsize=12, color='black')

#plt.show()


plt.savefig(Path.cwd()/'thesis/graphs/graph4.pdf')

# t-test

for var in demographic_variables:
	statictics=np.round(stats.ttest_ind(df[var][df['Change'] == 1], df[var][df['Change'] == 0]),3)
	print(var.replace('_1','').replace('_',' '),'&',statictics[0],'&',statictics[1],'\\\\')

for var in network_vars:
	temp=df.dropna(subset=[var])
	statictics = np.round(stats.ttest_ind(temp[var][temp['Change'] == 1], temp[var][temp['Change'] == 0]),3)
	print(var.replace('_1', '').replace('_', ' '), '&', statictics[0], '&', statictics[1], '\\\\')

for var in [x.replace('1','2') for x in network_vars]:
	temp = df.dropna(subset=[var])
	statictics = np.round(stats.ttest_ind(temp[var][temp['Change'] == 1], temp[var][temp['Change'] == 0]), 8)
	print(var.replace('_2', '').replace('_', ' '), '&', statictics[0], '&', statictics[1], '\\\\')
