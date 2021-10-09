import streamlit as st
import warnings
warnings.filterwarnings("ignore")
# EDA Pkgs
import pandas as pd
import numpy as np
import pandas as pd
import tweepy
import json
from tweepy import OAuthHandler
import re
import textblob
from textblob import TextBlob
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

#To Hide Warnings
st.set_option('deprecation.showfileUploaderEncoding', False)
st.set_option('deprecation.showPyplotGlobalUse', False)
# Viz Pkgs
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import seaborn as sns
#sns.set_style('darkgrid')


STYLE = """
<style>
img {max-width: 100%;}
</style> """


#st.title("Live Twitter Sentiment analysis")
#st.subheader("Select a User for whom you'd like to get the sentiment analysis:")

st.markdown("Tweet Analysis")
st.subheader("Select a User")

################# Twitter API Connection #######################
consumerKey = "kDgO0qZRdVkKICung7MkPl2QU"
consumerSecret = "ZOQhlwSEMhZUtdVPjc9CG4kaGCEWdR6AT9e2SJiJXoIMHxnIDi"
accessToken = "1445776538599768074-Vl3Udixl0J4EwIokYsboiQYbkviqin"
accessTokenSecret = "9xBgvVedGyrtUsofSvVLqM9i499AfSoapl0XtBzaVamrL"


# Use the above credentials to authenticate the API.
# Creating the authentication data
authenticate = tweepy.OAuthHandler(consumerKey, consumerSecret)

# Set the access token and access token secret
authenticate.set_access_token(accessToken, accessTokenSecret)

# Create the API object
api = tweepy.API(authenticate, wait_on_rate_limit=True)
    
# Collect Input from user :
TwitterHandle = str()
TwitterHandle = str(st.text_input("Enter the TwitterHandle you are interested in (Press Enter once done)"))     
    
if len(TwitterHandle) > 0 :
    # Call the function to extract the data. pass the Twitter Handle and filename you want the data to be stored in.
    with st.spinner("Please wait, Tweets are being extracted"):
        posts = api.user_timeline(screen_name = TwitterHandle, count = 200, lang ='en', tweet_mode="extended")

    df = pd.DataFrame([tweet.full_text for tweet in posts], columns=['Tweets'])

st.success('Tweets have been Extracted !!!!')   
#df.to_csv("TweetDataset.csv",index=False)
#df.to_excel('{}.xlsx'.format("TweetDataset"),index=False)   ## Save as Excel


def cleanTxt(text):
    text = re.sub(r'@[A-Za-z0-9]+', '', text) #Removed @mentions
    text = re.sub(r'#', '', text) #Removed Hastags
    text = re.sub(r'RT[\s]+', '', text) #Removed RT
    text = re.sub(r'https?:\/\/\S+', '', text) # Removed hyperlinks

    return text
        
df['Tweets']=df['Tweets'].apply(cleanTxt)

# Create a function to get the functionality
def getSubjectivity(text):
    return TextBlob(text).sentiment.subjectivity

    # Create a function to get the polarity
def getPolarity(text):
    return TextBlob(text).sentiment.polarity

    # Create two new columns
df['Subjectivity'] = df['Tweets'].apply(getSubjectivity)
df['Polarity'] = df['Tweets'].apply(getPolarity)
    

def getAnalysis(score):
  if score < 0:
    return 'Negative'
  elif score == 0:
    return 'Neutral'
  else:
    return 'Positive'

df['Analysis'] = df['Polarity'].apply(getAnalysis)

df

df['Analysis'] = df['Polarity'].apply(getAnalysis)

                
        # Write Summary of the Tweets
st.write("Total Tweets Extracted for the User '{}' are : {}".format(TwitterHandle,len(df.Tweets)))
st.write("Total Positive Tweets are : {}".format(len(df[df["Analysis"]=="Positive"])))
st.write("Total Negative Tweets are : {}".format(len(df[df["Analysis"]=="Negative"])))
st.write("Total Neutral Tweets are : {}".format(len(df[df["Analysis"]=="Neutral"])))
        
    # See the Extracted Data : 
if st.button("See the Extracted Data"):
    #st.markdown(html_temp, unsafe_allow_html=True)
    st.success("Below is the Extracted Data :")
    st.write(df.head(50))
        
        # get the countPlot
if st.button("Get Count Plot for Different Sentiments"):
    st.success("Generating A Count Plot")
    st.subheader(" Count Plot for Different Sentiments")
    st.write(sns.countplot(df["Analysis"]))
    st.pyplot()
        
        # Piechart 
if st.button("Get Pie Chart for Different Sentiments"):
    st.success("Generating A Pie Chart")
    a=len(df[df["Analysis"]=="Positive"])
    b=len(df[df["Analysis"]=="Negative"])
    c=len(df[df["Analysis"]=="Neutral"])
    d=np.array([a,b,c])
    explode = (0.1, 0.0, 0.1)
    st.write(plt.pie(d,shadow=True,explode=explode,labels=["Positive","Negative","Neutral"],autopct='%1.2f%%'))
    st.pyplot()
            
       
        
        # Points to add 1. Make Backgroud Clear for Wordcloud 2. Remove keywords from Wordcloud

stopwords = set(STOPWORDS)

        # Create a Worlcloud
if st.button("Get WordCloud for{}".format(TwitterHandle)):
    st.success("Generating A WordCloud for all tweets by {}".format(TwitterHandle))
    allWords = ' '.join( [twts for twts in df['Tweets']])
    wordcloud = WordCloud(background_color='white', width=500, height=300, stopwords=stopwords,max_words=50, max_font_size=120, random_state=21).generate(allWords)	
    st.write(plt.imshow(wordcloud, interpolation='bilinear'))
    st.pyplot()
        
        
			
              
st.sidebar.header("About App")
st.sidebar.info("Twitter Sentiment analysis Project")
st.sidebar.text("Built with Streamlit")
    
st.sidebar.header("Project 2 -CSDA1040:")
st.sidebar.info("Group1")
#st.sidebar.subheader("Scatter-plot setup")
#box1 = st.sidebar.selectbox(label= "X axis", options = numeric_columns)
#box2 = st.sidebar.selectbox(label="Y axis", options=numeric_columns)
#sns.jointplot(x=box1, y= box2, data=df, kind = "reg", color= "red")
#st.pyplot()


if st.button("Exit"):
   st.balloons()

