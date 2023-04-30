# -*- coding: utf-8 -*-
"""Copy of Untitled4.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1NGeoKFIhRXKLSpeTInTU3mlGjkL_vYGE
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score,confusion_matrix,roc_auc_score,ConfusionMatrixDisplay,precision_score,recall_score,f1_score,classification_report,roc_curve

import xgboost as xgb
import lightgbm as lgb
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB, BernoulliNB
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier

"""# **Reading Dataset**"""

df=pd.read_csv("brain_stroke.csv")
df.head()

# from google.colab import drive
# drive.mount('/content/drive')
# path1 = "/content/drive/MyDrive/Colab Data/brain_stroke.csv"
# df = pd.read_csv(path1)
# df.head()

"""# **Preprocessing of dataset**

### Checking for missing values
"""

df.isnull().sum()

"""### Checking the type of each columns"""

df.info()

"""### Looking for the categorical columns which needs to be LabelEncoded"""

categorical_columns = []
for col in df.columns:
  if(df[col].dtype == object):
    categorical_columns.append(col)
categorical_columns

numerical_columns = []
for col in df.columns:
  if(df[col].dtype != object):
    numerical_columns.append(col)
numerical_columns

"""# **Exploratory Data Analysis**

### Checking if there exist any imbalance in the dataset or not
"""

labels = df['stroke'].value_counts(sort = True).index
sizes = df['stroke'].value_counts(sort = True)
colors = ["green","red"]
expd = (0.3,0) 
plt.figure(figsize=(5,5))
plt.pie(sizes,explode=expd,labels=labels,colors=colors,autopct='%1.1f%%',shadow=True,startangle=90)
plt.title('Number of stroke in the dataset')
plt.legend(["Not having stroke" , "Having stroke"])
plt.show()

"""# **Categorical Columns**

### For all the features lets see the variation of numbers against the target variable 'stroke'
"""

sns.countplot(x='gender', hue='stroke', data=df)

df['gender'].value_counts()

sns.countplot(x='heart_disease', hue='stroke', data=df)

sns.countplot(x='ever_married', hue='stroke', data=df)

sns.countplot(x='work_type', hue='stroke', data=df)

sns.countplot(x='smoking_status', hue='stroke', data=df)

sns.countplot(x='Residence_type', hue='stroke', data=df)

"""# **Continuous Columns**"""

sns.kdeplot(data=df[df['stroke']==0],x='age',color='#7FB3D5', fill=True,alpha=0.3)
sns.kdeplot(data=df[df['stroke']==1],x='age',color='#F1605D', fill=True,alpha=0.3)
plt.title("Distribution of age ",fontdict={'fontweight': 'bold', 'size':18})
plt.legend(['No stroke' , 'stroke'],loc = 'upper left')

sns.kdeplot(data=df[df['stroke']==0],x='avg_glucose_level',color='#7FB3D5', fill=True,alpha=0.3)
sns.kdeplot(data=df[df['stroke']==1],x='avg_glucose_level',color='#F1605D', fill=True,alpha=0.3)
plt.title("Distribution of avg_glucose_level",fontdict={'fontweight': 'bold', 'size':18})
plt.legend(['No stroke' , 'Stroke'],loc = 'upper right')

sns.kdeplot(data=df[df['stroke']==0],x='bmi',color='#7FB3D5', fill=True,alpha=0.3)
sns.kdeplot(data=df[df['stroke']==1],x='bmi',color='#F1605D', fill=True,alpha=0.3)
plt.title("Distribution of bmi ",fontdict={'fontweight': 'bold', 'size':18})
plt.legend(['No stroke' , 'stroke'],loc = 'upper right')

cols = ['age', 'avg_glucose_level', 'bmi']
plt.figure(figsize = (16, 8))
idx = 0
for i in cols:
    plt.subplot(1,3,idx+1)
    sns.histplot(x = df[i],kde = True)
    plt.ylabel(None)
    plt.title(i)
    plt.xlabel(None)
    idx+=1
    
plt.plot()

for col in categorical_columns:
  encoder= LabelEncoder()
  df[col] = encoder.fit_transform(df[col])
df

numerical_columns

to_remove =['stroke','hypertension','heart_disease']
for i in to_remove :
  numerical_columns.remove(i)

numerical_columns

scaler = StandardScaler()
df[numerical_columns] = scaler.fit_transform(df[numerical_columns])
df

X = df.drop('stroke', axis=1)
y =df['stroke']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, stratify=y)

X_val, X_test, y_val, y_test = train_test_split(X_test, y_test, test_size=0.67, stratify=y_test)

models = [LogisticRegression() ,
          DecisionTreeClassifier(), 
          RandomForestClassifier(),
          BernoulliNB(),
          GaussianNB(),
          SVC(),
          KNeighborsClassifier(),
          GradientBoostingClassifier(),
          AdaBoostClassifier(),
          xgb.XGBClassifier()]
model_names = ['LogisticRegression',
               'DecisionTreeClassifier',
               'RandomForestClassifier',
               'BernoulliNB',
               'GaussianNB',
               'Support Vector Machine',
               'K-Nearest Neighbors',
               'GradientBoostingClassifier',
               'AdaBoost',
               'XGBClassifier',
               'LightGBM']
Precision = []
Recall = []
ROC = []
F1 = []

def training_summary(x_train, y_train, x_val, y_val, model_name , model):
  model.fit(x_train, y_train)
  prediction = model.predict(x_val)
  precision = precision_score(y_val, prediction)*100
  recall = recall_score(y_val, prediction)*100
  roc = roc_auc_score(y_val,prediction)*100
  f1 = f1_score(y_val,prediction)*100
  Precision.append(precision)
  Recall.append(recall)
  ROC.append(roc)
  F1.append(f1)

def evaluate_classifiers(x_train,y_train,x_val,y_val):
  training_summary(x_train,y_train, x_val, y_val, 'LogisticRegression',LogisticRegression())
  training_summary(x_train,y_train, x_val, y_val, 'DecisionTreeClassifier',DecisionTreeClassifier())
  training_summary(x_train,y_train, x_val, y_val, 'RandomForestClassifier',RandomForestClassifier(n_estimators=50,n_jobs=-1))   
  training_summary(x_train,y_train, x_val, y_val, 'BernoulliNB',BernoulliNB())
  training_summary(x_train,y_train, x_val, y_val, 'GaussianNB',GaussianNB())
  training_summary(x_train,y_train, x_val, y_val, 'Support Vector Machine',SVC())
  training_summary(x_train,y_train, x_val, y_val, 'K-Nearest Neighbors',KNeighborsClassifier(n_neighbors=1,algorithm='kd_tree',weights='uniform'))
  training_summary(x_train,y_train, x_val, y_val, 'GradientBoostingClassifier',GradientBoostingClassifier(learning_rate=0.1,loss='exponential',max_depth=70,
                          max_features=2,n_estimators=300))
  training_summary(x_train,y_train, x_val, y_val, 'AdaBoost', AdaBoostClassifier(n_estimators=100, base_estimator=DecisionTreeClassifier(max_depth=1)))
  training_summary(x_train,y_train, x_val, y_val, 'XGBClassifier',xgb.XGBClassifier())
  training_summary(x_train,y_train,x_val,y_val, 'LightGBM',lgb.LGBMClassifier())

evaluate_classifiers(X_train,y_train,X_val,y_val)

model_names

compare_classifiers = pd.DataFrame({'Model': model_names, 'Precision': Precision, 'Recall': Recall, 'ROC_AUC_Score' : ROC,'F1_score' : F1})
compare_classifiers.style.background_gradient(high=1,axis=0)

smote = SMOTE()
X_smote , y_smote = smote.fit_resample(X,y)

data_smote = pd.concat([X_smote, y_smote],axis=1)

X_train, X_test, y_train, y_test = train_test_split(X_smote, y_smote, test_size=0.3, stratify=y_smote)

X_val, X_test, y_val, y_test = train_test_split(X_test, y_test, test_size=0.67, stratify=y_test)

data_smote

class_counts = data_smote['stroke'].value_counts()
class_counts

fig,ax=plt.subplots(1,2,figsize=(12,5))
sns.scatterplot(data=df,x='age',y='avg_glucose_level',hue='stroke',ax=ax[0])\
.set_title("Actual Data")
sns.scatterplot(data=data_smote,x='age',y='avg_glucose_level',hue='stroke',ax=ax[1])\
.set_title("SMOTE Data")

Precision = []
Recall = []
ROC = []
F1 = []



evaluate_classifiers(X_train,y_train,X_test,y_test)

Precision

compare_classifiers = pd.DataFrame({'Model': model_names, 'Precision': Precision, 'Recall': Recall, 'ROC_AUC_Score' : ROC,'F1_score' : F1})
compare_classifiers.style.background_gradient(high=1,axis=0)

plt.figure(figsize = (10 , 5))
# compare_classifiers = compare_classifiers.sort_values(by='Recall', ascending=True)
sns.barplot(y = "Model" , x = "Recall" , data = compare_classifiers)
plt.title("Model Comparision based on Recall");

plt.figure(figsize = (10 , 5))
# compare_classifiers = compare_classifiers.sort_values(by='F1_score', ascending=True)
sns.barplot(y = "Model" , x = "ROC_AUC_Score" , data = compare_classifiers)
plt.title("Model Comparision based on ROC_AUC_Score");

plt.figure(figsize = (10 , 5))
# compare_classifiers = compare_classifiers.sort_values(by='F1_score', ascending=True)
sns.barplot(y = "Model" , x = "F1_score" , data = compare_classifiers)
plt.title("Model Comparision based on F1_score");

plt.figure(figsize=(12, 6))

# Set the style of the plot
sns.set(style="whitegrid")

# Melt the dataframe to create a long-form representation
melted_df = pd.melt(compare_classifiers, id_vars=['Model'], var_name='Metric', value_name='Value')

# Create a line plot
sns.lineplot(x='Model', y='Value', hue='Metric', data=melted_df)

# Add labels and title
plt.xticks(rotation=90)
plt.xlabel('Model')
plt.ylabel('Value')
plt.title('Comparison of Models based on Evaluation Metrics')

# Show the plot
plt.show()

import pickle
clf = RandomForestClassifier()
clf.fit(X_train, y_train)
pickle.dump(clf, open("random_forest_model.sav", "wb"))
pickle.dump(scaler, open("scaler.sav", "wb"))