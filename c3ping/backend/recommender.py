import pandas as pd
from .functions import *

df = load_data()
df_processed = preprocess_data(df)
tfidf, vectors, model, df_valid = create_vectorizer_and_model(df_processed)

def get_recommendations(query, n=5):
    return recommend_courses(query, df_valid, tfidf, vectors, model, n_recommendations=n)