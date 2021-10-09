\
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

html_temp = <div style="background-color:tomato;"><p style="color:white;font-size:25px;padding:9px">Live Twitter Sentiment Analysis</p></div>
    
    st.markdown(html_temp, unsafe_allow_html=True)
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
    
    TwitterHandle = "JustinTrudeau"
    posts = api.user_timeline(screen_name = TwitterHandle, count = 100, lang ='en', tweet_mode="extended")
    df = pd.DataFrame([tweet.full_text for tweet in posts], columns=['Tweets'])
    def get_tweets():
        l=[]
        i=1
        for tweet in posts[:5]:
            l.append(tweet.full_text)
            i= i+1
        return l
        recent_tweets=get_tweets()		
        return recent_tweets
	
    

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
	
        
        if score > 0:
            return 'Positive'
        elif score == 0:
            return 'Neutral'
        else:
            return 'Negative'

    df['Analysis'] = df['Polarity'].apply(getAnalysis)

 
    
    # Collect Input from user :
    TwitterHandle = str()
    TwitterHandle = str(st.text_input("Enter the TwitterHandle you are interested in (Press Enter once done)"))     
    
    if len(TwitterHandle) > 0 :
        # Call the function to extract the data. pass the Twitter Handle and filename you want the data to be stored in.
        with st.spinner("Please wait, Tweets are being extracted"):
            posts = api.user_timeline(screen_name = TwitterHandle, count = 100, lang ='en', tweet_mode="extended")
        st.success('Tweets have been Extracted !!!!')    
           
    
        # Call function to get Clean tweets
        df['CleanTxt'] = df['Tweets'].apply(lambda x : cleanTxt(x))
    
        # Call function to get the Sentiments
        df["Polarity"] = df["Tweets"].apply(lambda x : getAnalysis(x))
                
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
        
        # Create a Worlcloud
        if st.button("Get WordCloud for{}".format(TwitterHandle)):
            st.success("Generating A WordCloud for all tweets by {}".format(TwitterHandle))
            text = " ".join(review for review in df.cleanTxt)
            stopwords = set(STOPWORDS)
            text_newALL = prepCloud(text,TwitterHandle)
            wordcloud = WordCloud(stopwords=stopwords,max_words=800,max_font_size=70).generate(text_newALL)
            st.write(plt.imshow(wordcloud, interpolation='bilinear'))
            st.pyplot()
        
        
        #Wordcloud for Positive tweets only
        if st.button("Get WordCloud for all Positive Tweets by {}".format(TwitterHandle)):
            st.success("Generating A WordCloud for all Positive Tweets by {}".format(TwitterHandle))
            text_positive = " ".join(review for review in df[df["Analysis"]=="Positive"].cleanTxt)
            stopwords = set(STOPWORDS)
            text_new_positive = prepCloud(text_positive,TwitterHandle)
            #text_positive=" ".join([word for word in text_positive.split() if word not in stopwords])
            wordcloud = WordCloud(stopwords=stopwords,max_words=800,max_font_size=70).generate(text_new_positive)
            st.write(plt.imshow(wordcloud, interpolation='bilinear'))
            st.pyplot()
        
                #Wordcloud for Negative tweets only       
        if st.button("Get WordCloud for all Negative Tweets by {}".format(TwitterHandle)):
            st.success("Generating A WordCloud for all Positive Tweets by {}".format(TwitterHandle))
            text_negative = " ".join(review for review in df[df["Analysis"]=="Negative"].cleanTxt)
            stopwords = set(STOPWORDS)
            text_new_negative = prepCloud(text_negative,TwitterHandle)
            #text_negative=" ".join([word for word in text_negative.split() if word not in stopwords])
            wordcloud = WordCloud(stopwords=stopwords,max_words=800,max_font_size=70).generate(text_new_negative)
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


