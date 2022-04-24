library("pglm")
library(sjPlot)
library(sjlabelled)
library(sjmisc)
library(ggplot2)
library(plm)
#install.packages("rbibutils")
library('bife')

df<-read.csv('/Users/valler/Documents/Oxford/MPhil/2021HT Social Network/social_network/data/thesis/data_long_format.csv')
df_female<-df[df['Female']==1,]
df_male<-df[df['Female']==0,]
  
# overall 

rg<-bife(Know_More~
           Network_Size+ 
           Same_Gender+
           Same_Race+Kin+Non_Kin+
           
           
           
           Belief_On_Having_Non.Kin_To_Help_With_Serious_Problem+
           Belief_On_Having_Kin_To_Help_With_Serious_Problem+
           Reciprocity+
           Demanding_and_Support+
           Actual_Support+
           
           Social_Companionship+
           Demanding+
           
           Frequency+
           Average_Knowing_Years+
           Confide+
           Especially_Close+ 
           
           Recent_Retired+
           New_School_Or_Job+
           Recent_Major_Problem_on_work_or_school_or_financial+
           Recent_Break_Up_with_Close_Friends_or_Relatives+
           Recent_Important_change_in_marriage+
           Recent_Have_a_Child_Or_Grandchild+
           Recent_Friend_Or_Kin_Died+
           Lower_Health
         |PRIM_KEY,data=df)

summary(rg)
apes_stat <- get_APEs(rg)
summary(apes_stat)



# by gender 



rg_female<-bife(Know_More~
                  Network_Size+ 
                  Same_Gender+
                  Same_Race+
                  
                  
                  
                  Belief_On_Having_Non.Kin_To_Help_With_Serious_Problem+
                  Belief_On_Having_Kin_To_Help_With_Serious_Problem+
                  Reciprocity+
                  Demanding_and_Support+
                  Actual_Support+
                  
                  Social_Companionship+
                  Demanding+
                  
                  Frequency+
                  Average_Knowing_Years+
                  Confide+
                  Especially_Close+ 
                  
                  Recent_Retired+
                  New_School_Or_Job+
                  Recent_Major_Problem_on_work_or_school_or_financial+
                  Recent_Break_Up_with_Close_Friends_or_Relatives+
                  Recent_Important_change_in_marriage+
                  Recent_Have_a_Child_Or_Grandchild+
                  Recent_Friend_Or_Kin_Died+
                  Lower_Health
                |PRIM_KEY,df_female,"logit")

apes_stat <- get_APEs(rg_female)
summary(apes_stat)


#males

rg_male<-bife(Know_More~
                Network_Size+ 
                Same_Gender+
                Same_Race+
                
                
                
                Belief_On_Having_Non.Kin_To_Help_With_Serious_Problem+
                Belief_On_Having_Kin_To_Help_With_Serious_Problem+
                Reciprocity+
                Demanding_and_Support+
                Actual_Support+
                
                Social_Companionship+
                Demanding+
                
                Frequency+
                Average_Knowing_Years+
                Confide+
                Especially_Close+ 
                
                Recent_Retired+
                New_School_Or_Job+
                Recent_Major_Problem_on_work_or_school_or_financial+
                Recent_Break_Up_with_Close_Friends_or_Relatives+
                Recent_Important_change_in_marriage+
                Recent_Have_a_Child_Or_Grandchild+
                Recent_Friend_Or_Kin_Died+
                Lower_Health
              |PRIM_KEY,df_male,"logit")

apes_stat <- get_APEs(rg_male)
summary(apes_stat)


summary(rg)
summary(rg_female)

summary(rg_male)


round(exp(rg$coefficients),digits = 3)

round(exp(rg_female$coefficients),digits = 3)
round(exp(rg_male$coefficients),digits = 3)



# write.csv(data,'/Users/valler/Documents/Oxford/MPhil/2021HT Social Network/social_network/data/thesis/regression_data.csv')


#plot 
plot_model(rg,sort.est = TRUE,show.values = TRUE, value.offset = .4,value.size = 2.8,title = "my own title")

plot_model(rg_female,sort.est = TRUE)
plot_model(rg_male,sort.est = TRUE)

