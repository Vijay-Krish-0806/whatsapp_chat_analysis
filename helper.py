from urlextract import URLExtract
from wordcloud import WordCloud
from sklearn.feature_extraction.text import CountVectorizer

import emoji
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
extractor=URLExtract()
import pandas as pd

from collections import Counter
def fetch_stats(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
       
    num_messages= df.shape[0]
    words=[]
    count=0
    for message in df['message']:
        count+=len(message.split())

    #fetch media messages
    media_num=df[df['message']=='<Media omitted>\n'].shape[0]

    links=[]
    for message in df['message']:
        links.extend(extractor.find_urls(message))
    
    
    return num_messages,count,media_num,len(links)


def fetch_most_busy_users(df):
    values=df['user'].value_counts().head()
    df=round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'name','user':'percent'})
    return values,df

def create_wordcloud(df,selected_user):
    if selected_user!='Overall':
        df=df[(df['user']==selected_user)]
    temp=df[df['user']!='group_notification']
    temp=temp[temp['message']!='<Media omitted\n']
    custom_stopwords = {
    'ga', 'ra', 'le', 'haa', 'em', 'bro', 'lo', 'ani', 'nenu', 'ha', 
    'sare', 'ki', 'inka', 'nuvu', 'mari', 'kuda', 'ne', 'ah', 'ee', 'aa',
    'emo', 'enti', 'oka', 'roju', 'adhi', 'enjoy', 'malli', 'naku', 'ade',
    'teja', 'epudu', 'kani', 'ayina', 'cheppu', 'neku', 'nen', 'avuna', 'chey',
    'naaku', 'nee','media','omitted','ledhu','antha','anta','kk','null','edited'
}

    stopwords = list(ENGLISH_STOP_WORDS) + list(custom_stopwords)

    wc = WordCloud(width=500, height=500, background_color="white",stopwords=stopwords)
    df_wc=wc.generate(df['message'].str.cat(sep=" "))
    return df_wc


def most_common(df,selected_user):
    if selected_user!='Overall':
        df=df[(df['user']==selected_user)]
    temp=df[df['user']!='group_notification']
    temp=temp[temp['message']!='<Media omitted\n']
    custom_stopwords = {
    'ga', 'ra', 'le', 'haa', 'em', 'bro', 'lo', 'ani', 'nenu', 'ha', 
    'sare', 'ki', 'inka', 'nuvu', 'mari', 'kuda', 'ne', 'ah', 'ee', 'aa',
    'emo', 'enti', 'oka', 'roju', 'adhi', 'enjoy', 'malli', 'naku', 'ade',
    'teja', 'epudu', 'kani', 'ayina', 'cheppu', 'neku', 'nen', 'avuna', 'chey',
    'naaku', 'nee','media','omitted','ledhu','antha','anta','kk',
}

    stopwords = list(ENGLISH_STOP_WORDS) + list(custom_stopwords)
    vectorizer = CountVectorizer(stop_words=stopwords)
    X = vectorizer.fit_transform(temp['message'])
    words = vectorizer.get_feature_names_out()
    word_counts = X.toarray().sum(axis=0)
    word_frequencies = pd.DataFrame(zip(words, word_counts), columns=['Word', 'Frequency'])
    most_common = word_frequencies.sort_values(by='Frequency', ascending=False)
    
    return most_common

from emoji import is_emoji
from collections import Counter
import pandas as pd

def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if is_emoji(c)])
    
    # Count the frequency of each emoji
    counter = Counter(emojis)
    
    # Create a DataFrame to display the emojis and their counts
    emoji_df = pd.DataFrame(counter.most_common(len(counter)), columns=['Emoji', 'Count'])
    return emoji_df


def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    timeline=df.groupby(['year','month_num','month']).count()['message'].reset_index()
    time=[]
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+"-"+str(timeline['year'][i]))
    timeline['time']=time
    return timeline


def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    timeline=df.groupby(['only_date']).count()['message'].reset_index()
    return timeline

def week_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['day_name'].value_counts()
def month_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['month'].value_counts()
