import pandas as pd
import numpy as np
import json,os

df=pd.read_csv("movie.csv")

def create_recommendation(watch_list):
  if not watch_list:  # Empty list 
    return []
  from sklearn.feature_extraction.text import CountVectorizer
  counter=CountVectorizer(max_features=4000, stop_words='english')
  vectors=counter.fit_transform(df.tags).toarray()
  movie_index_to_recommend=[]
  for i in watch_list:
    movie_index_to_recommend.append(int(df[df.movie_id==i].index[0]))
  user_vectors=vectors[movie_index_to_recommend]
  centroids=user_vectors.mean(axis=0)
  from sklearn.metrics.pairwise import cosine_similarity
  similarities=cosine_similarity(centroids.reshape(1, -1), vectors)
  movie_ids=np.array(df.movie_id)
  similarities_id=np.concat(([movie_ids],similarities),axis=0)
  similarities_list = []
  for i in similarities_id.T:
    similarities_list.append([int(i[0]),float(i[1])])
  for i in similarities_list[:]:
    if i[0] in watch_list:
      similarities_list.remove(i)
  similarities_list=sorted(similarities_list,reverse=True,key=lambda x:x[1])[:15]
  top_picks_id_list=[]
  for i in similarities_list:
    top_picks_id_list.append(i[0])
  top_picks_list=[]
  for i in top_picks_id_list:
    top_picks_list.append(df[df.movie_id==i].title_x.iloc[0])
  return top_picks_list