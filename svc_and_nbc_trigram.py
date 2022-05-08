# -*- coding: utf-8 -*-
"""SVC AND NBC trigram.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1LG082LgXUgAvOhkChl6BZpZZ88bM8gEY
"""

from google.colab import drive
drive.mount('/content/drive')

# -*- coding: utf-8 -*-
"""
Created on Mon Aug 30 23:39:59 2021

@author: amand
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Mar 24 12:33:07 2021

@author: amand
"""

import re, nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import StratifiedKFold
import seaborn as sns
from sklearn import metrics
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import MultinomialNB
import joblib
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import plotly.graph_objs as go
import plotly.figure_factory as ff
from plotly.offline import plot
import plotly.express as px
import plotly.io as pio

# Reading dataset as dataframe
df = pd.read_csv("/content/drive/My Drive/Sentiment_Analysis_Data.csv", encoding = "ISO-8859-1") # You can also use "utf-8"
pd.set_option('display.max_colwidth', None) # Setting this so we can see the full content of cells

# Converting Sentiment Column to numerical features
#df['Analysis'] = df['Analysis'].map({'Positive': 1, 'Negative':-1, 'Neutral': 0})

# Cleaning Tweets
def cleaner(tweet):
    soup = BeautifulSoup(tweet, 'lxml') # removing HTML entities such as ‘&amp’,’&quot’,'&gt'; lxml is the html parser and shoulp be installed using 'pip install lxml'
    souped = soup.get_text()
    re1 = re.sub(r"(@|http://|https://|www|\\x)\S*", " ", souped) # substituting @mentions, urls, etc with whitespace
    re2 = re.sub("[^A-Za-z]+"," ", re1) # substituting any non-alphabetic character that repeats one or more times with whitespace

    """
    For more info on regular expressions visit -
    https://docs.python.org/3/howto/regex.html
    """

    tokens = nltk.word_tokenize(re2)
    lower_case = [t.lower() for t in tokens]

    stop_words = set(stopwords.words('english'))
    filtered_result = list(filter(lambda l: l not in stop_words, lower_case))

    wordnet_lemmatizer = WordNetLemmatizer()
    lemmas = [wordnet_lemmatizer.lemmatize(t) for t in filtered_result]
    return lemmas

df['cleaned_inflation_tweets'] = df.TWEETS.apply(cleaner)
df = df[df['cleaned_inflation_tweets'].map(len) > 0] # removing rows with cleaned tweets of length 0
print("Printing top 5 rows of dataframe showing original and cleaned tweets....")
print(df[['TWEETS','cleaned_inflation_tweets']].head())
df.drop(['TWEETS','cleaned_tweet', 'Subjectivity','Polarity'], axis=1, inplace=True)
# Saving cleaned tweets to csv
df.to_csv('Trigrams_cleaned tokens for Machine learning.csv')
df['cleaned_inflation_tweets'] = [" ".join(row) for row in df['cleaned_inflation_tweets'].values] # joining tokens to create strings. TfidfVectorizer does not accept tokens as input
data = df['cleaned_inflation_tweets']
Y = df['Analysis'] # target column
print(Y.head)

tfidf = TfidfVectorizer(min_df=.0015, ngram_range=(1,3)) # min_df=.0015 means that each ngram (unigram, bigram, & trigram) must be present in at least 16 documents for it to be considered as a token (10572*0.0015=15.858). This is a clever way of feature engineering
tfidf.fit(data) # learn vocabulary of entire data
data_tfidf = tfidf.transform(data) # creating tfidf values
tfidf.get_feature_names()
#pd.DataFrame.from_dict(data=dict([word, i] for i, word in enumerate(tfidf.get_feature_names())), orient='index').to_csv('features_trigram.csv', header=False)
#print(pd.DataFrame(data_tfidf).head(30))
print("Shape of tfidf matrix: ", data_tfidf.shape)


# Implementing Support Vector Classifier
model = LinearSVC() # kernel = 'linear' and C = 1

# Running cross-validation
kf = StratifiedKFold(n_splits=10, shuffle=True, random_state=1) # 10-fold cross-validation
scores=[]
iteration = 0
for train, test in kf.split(data_tfidf, Y):
    iteration += 1
    print("Iteration ", iteration)
    X_train, Y_train = data_tfidf, Y
    X_test, Y_test = data_tfidf, Y
    model.fit(X_train, Y_train) # Fitting SVC
    Y_pred = model.predict(X_test)
    score = metrics.accuracy_score(Y_test, Y_pred) # Calculating accuracy
    print("Cross-validation accuracy: ", score)
    scores.append(score) # appending cross-validation accuracy for each iteration
    print("SVC Predicted Y: ", Y_pred)
svc_mean_accuracy = np.mean(scores)
print("Mean SVC cross-validation accuracy: ", svc_mean_accuracy)

# Implementing Naive Bayes Classifier
print('                                                                 ')
nbc_clf = MultinomialNB()

# Running cross-validation
kf = StratifiedKFold(n_splits=5, shuffle=True, random_state=1) # 10-fold cross-validation
scores=[]
iteration = 0
for train, test in kf.split(data_tfidf, Y):
    iteration += 1
    print("Iteration ", iteration)
    X_train, Y_train = data_tfidf, Y
    X_test, Y_test = data_tfidf, Y
    nbc_clf.fit(X_train, Y_train) # Fitting NBC
    Y_pred = nbc_clf.predict(X_test)
    score = metrics.accuracy_score(Y_test, Y_pred) # Calculating accuracy
    print("Cross-validation accuracy: ", score)
    scores.append(score) # appending cross-validation accuracy for each iteration
    print("NBC Predicted Y: ", Y_pred)
nbc_mean_accuracy = np.mean(scores)
print("Mean NB cross-validation accuracy: ", nbc_mean_accuracy)

# Creating SVC on entire data and saving it,saving the SVC Trigram data with higher accuracy for deployment
clf = LinearSVC().fit(data_tfidf, Y)
joblib.dump(clf, 'svc_inflation.sav')


# Evaluating Decision Tree Model
Y_pred = model.predict(X_test)
print("Prediction Accuracy: ", metrics.accuracy_score(Y_test, Y_pred))
conf_mat = metrics.confusion_matrix(Y_test, Y_pred)
plt.figure(figsize=(8,6))
sns.heatmap(conf_mat,annot=True)
plt.title("Confusion_matrix")
plt.xlabel("Predicted Class")
plt.ylabel("Actual class")
plt.show()
print('Confusion matrix: \n', conf_mat)
print('TP: ', conf_mat[1,1])
print('TN: ', conf_mat[0,0])
print('FP: ', conf_mat[0,1])
print('FN: ', conf_mat[1,0])