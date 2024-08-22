import pickle
import streamlit as st
import numpy as np
import pandas as pd
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
import mysql.connector
conn = mysql.connector.connect(

    host="localhost",

    user="root",

    port="3306",

    password="99946@abd",

    database="final-project"

)

table_name='youtube'
database="final-project"
cursor = conn.cursor()

writer = cursor 

query = "SELECT * FROM youtube"
cursor.execute(query)
view=cursor.fetchall()

query2 =f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}' AND TABLE_SCHEMA = '{database}' ORDER BY ORDINAL_POSITION"
cursor.execute(query2)
a=cursor.fetchall()
flat_list = [item[0] for item in a]
final=pd.DataFrame(view)
final.columns=flat_list
with open('model.pkl',"rb") as f:
    kmeans=pickle.load(f)
with open('vectorizer.pkl',"rb") as k:
    vectorizer=pickle.load(k)  
with open('X.pkl',"rb") as m:
    X=pickle.load(m)       
def recommend_channels(query):
    query_vector = vectorizer.transform([query])
    input_cluster = kmeans.predict(query_vector)[0]
    cluster_channels = final[final['cluster'] == input_cluster]
    similarity_scores = cosine_similarity(query_vector, X[cluster_channels.index]).flatten()
    recommended_indices = similarity_scores.argsort()[::-1]
    recommended_channels = cluster_channels.iloc[recommended_indices]
    return recommended_channels
m,n=st.columns([1,10])
with m:
    st.image(r"1000_F_300389025_b5hgHpjDprTySl8loTqJRMipySb1rO0I.jpg")
#a,b=st.columns([1,10])
#with b:       
query=st.text_input('please enter')
#if query:
#with b:
o=recommend_channels(query)
col1,col2=st.columns([1,2])
for i, j in o.iterrows():
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(j['snippet.thumbnails.default.url'], use_column_width=True)
    with col2:
        st.write(f'__{j['snippet.title']}__')
        st.write(f':red[{j['snippet.channelTitle']}]')
        a,b=st.columns([1,3])
        with a:
            try:
                st.write(":blue[View's]",int(j['statistics.viewCount']))
            except:
                st.wrtie(0)    
        with b:
            try:
                st.write('👍',j['statistics.likeCount']) 
            except:
                st.write(0)
                   