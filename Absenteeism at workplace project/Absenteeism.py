
# coding: utf-8

# In[3]:


import os
import pandas as pd
import numpy as np
import matplotlib as mlt
import matplotlib.pyplot as plt
import seaborn as sn


# In[97]:


os.chdir("G:/data science project")


# In[98]:


employee=pd.read_excel("Absenteeism_at_work_Project.xls")


# In[99]:


employee=employee[employee['Reason for absence']!=0]


# In[100]:


employee=employee[employee['Absenteeism time in hours']!=0]


# In[101]:


employee['Body mass index']=employee['Body mass index'].fillna(employee['Body mass index'].median())


# In[102]:


employee['Absenteeism time in hours']=employee['Absenteeism time in hours'].fillna(employee['Absenteeism time in hours'].mean())


# In[103]:


employee['Reason for absence']=employee['Reason for absence'].fillna(employee['Reason for absence'].median())


# In[104]:


employee['Month of absence']=employee['Month of absence'].fillna(employee['Month of absence'].median())


# In[105]:


employee['Education']=employee['Education'].fillna(employee['Education'].median())


# In[106]:


employee['Disciplinary failure']=employee['Disciplinary failure'].fillna(employee['Disciplinary failure'].median())


# In[107]:


employee['Social drinker']=employee['Social drinker'].fillna(employee['Social drinker'].median())


# In[108]:


employee['Social smoker']=employee['Social smoker'].fillna(employee['Social smoker'].median())


# In[109]:


employee['Pet']=employee['Pet'].fillna(employee['Pet'].mean())


# In[110]:


employee['Weight']=employee['Weight'].fillna(employee['Weight'].mean())


# In[111]:


employee['Height']=employee['Height'].fillna(employee['Height'].mean())


# In[112]:


employee['Transportation expense']=employee['Transportation expense'].fillna(employee['Transportation expense'].mean())


# In[113]:


employee['Distance from Residence to Work']=employee['Distance from Residence to Work'].fillna(employee['Distance from Residence to Work'].mean())


# In[114]:


employee['Service time']=employee['Service time'].fillna(employee['Service time'].mean())


# In[115]:


employee['Age']=employee['Age'].fillna(employee['Age'].mean())


# In[116]:


employee['Son']=employee['Son'].fillna(employee['Son'].mean())


# In[117]:


employee['Hit target']=employee['Hit target'].fillna(employee['Hit target'].mean())


# In[118]:


employee=employee.rename(columns={"Work load Average/day ":"Work load Average per day"})


# In[119]:


employee['Work load Average per day']=employee['Work load Average per day'].fillna(employee['Work load Average per day'].mean())


# In[120]:


missing_percent=((employee.isnull().sum()*100)/len(employee))


# In[121]:


print(missing_percent)


# In[122]:


employee.info()


# In[123]:


cnames=['ID','Transportation expense','Distance from Residence to Work','Service time','Age','Work load Average per day',
        'Hit target','Son','Pet','Weight','Height','Body mass index']


# In[124]:


employee_corr=employee.loc[:,cnames]


# In[125]:


f,ax=plt.subplots(figsize=(7,5))
corr=employee_corr.corr()
sn.heatmap(corr,mask=np.zeros_like(corr,dtype=np.bool),cmap=sn.diverging_palette(220,10,as_cmap=True),square=True,ax=ax)


# In[126]:


for i in cnames:
    q75,q25=np.percentile(employee.loc[:,i],[75,25])
    iqr=q75-q25
    min=q25-(iqr*1.5)
    max=q75+(iqr*1.5)
    employee=employee.drop(employee[employee.loc[:,i]<min].index)
    employee=employee.drop(employee[employee.loc[:,i]>max].index)


# In[127]:


employee['Absenteeism time in hours']=['Less than or equal to 4' if val in(range(1,4)) else 'Greater than 4'
                                       for val in employee['Absenteeism time in hours']]


# In[128]:


employee=employee.drop(['Disciplinary failure','ID','Height'],axis=1)


# In[129]:


employee=employee.drop(['Service time','Weight'],axis=1)


# In[130]:


employee=employee.drop(['Education'],axis=1)


# In[131]:


from sklearn.cross_validation import train_test_split
from sklearn.ensemble import RandomForestClassifier


# In[132]:


employee.info()


# In[134]:


x=employee.values[:,0:14]
y=employee.values[:,14]

x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.3)


# In[135]:


model=RandomForestClassifier(n_estimators=500).fit(x_train,y_train)


# In[136]:


predictions=model.predict(x_test)


# In[137]:


from sklearn.metrics import confusion_matrix


# In[138]:


cm=pd.crosstab(y_test,predictions)


# In[139]:


cm


# In[140]:


TN=cm.iloc[0,0]
FN=cm.iloc[1,0]
TP=cm.iloc[1,1]
FP=cm.iloc[0,1]


# In[141]:


((TP+TN)*100)/(TP+TN+FP+FN)


# In[142]:


(FN*100)/(FN+TP)

