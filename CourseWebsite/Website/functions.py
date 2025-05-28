import pandas as pd
import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics.pairwise import cosine_similarity

def load_data():
    try:
        df = pd.read_csv("D:\Mini-Django\Final_Coursera.csv")
        required_cols = ['Course Name', 'Course Description', 'Skills', 'Course Rating', 'Course URL']
        if not all(col in df.columns for col in required_cols):
            raise ValueError("Missing required columns")
        return df
    except (FileNotFoundError, ValueError):
        data = {
            'Course Name': [
                'Machine Learning Fundamentals', 'Python Programming Essentials', 'Data Science Bootcamp',
                'Web Development with JavaScript', 'Deep Learning Neural Networks', 'SQL Database Analysis',
                'Flutter Mobile Development', 'Cloud Computing AWS', 'Cybersecurity Fundamentals', 
                'Business Analytics Dashboard', 'React Frontend Development', 'Node.js Backend Programming',
                'Data Visualization with Python', 'Digital Marketing Strategy', 'Project Management Professional'
            ],
            'Course Description': [
                'Comprehensive introduction to machine learning algorithms and applications',
                'Learn Python programming from basics to advanced concepts',
                'End-to-end data science workflow with real projects',
                'Build modern web applications using JavaScript and frameworks',
                'Master neural networks and deep learning with TensorFlow',
                'Advanced SQL techniques for data analysis and reporting',
                'Create cross-platform mobile apps with Flutter and Dart',
                'Learn cloud services, deployment, and infrastructure on AWS',
                'Essential cybersecurity principles and threat protection',
                'Transform business data into actionable insights and dashboards',
                'Build responsive user interfaces with React.js',
                'Server-side development with Node.js and Express',
                'Create compelling visualizations using Python libraries',
                'Digital marketing strategies for modern businesses',
                'Professional project management methodologies and tools'
            ],
            'Skills': [
                'Machine Learning, Python, Scikit-learn, Statistics',
                'Python, Programming, OOP, Data Structures',
                'Data Science, Pandas, NumPy, Matplotlib, Statistics',
                'JavaScript, HTML, CSS, DOM, Web APIs',
                'Deep Learning, TensorFlow, Neural Networks, AI',
                'SQL, Database Design, Data Analysis, Reporting',
                'Flutter, Dart, Mobile Development, UI/UX',
                'AWS, Cloud Computing, DevOps, Infrastructure',
                'Security, Risk Assessment, Encryption, Compliance',
                'Business Intelligence, Excel, Tableau, Analytics',
                'React, JavaScript, Frontend, Component Architecture',
                'Node.js, Express, Backend, API Development',
                'Data Visualization, Python, Plotly, Seaborn',
                'Marketing, SEO, Social Media, Analytics',
                'Project Management, Agile, Scrum, Leadership'
            ],
            'Course Rating': [4.7, 4.5, 4.8, 4.2, 4.9, 4.6, 4.3, 4.4, 4.5, 4.7, 4.6, 4.4, 4.8, 4.1, 4.5],
            'Course URL': [f'https://example.com/course-{i}' for i in range(15)]
        }
        return pd.DataFrame(data)

def clean_text(text):
    if pd.isna(text):
        return ""
    text = str(text).lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def preprocess_data(df):
    df = df.copy()
    df['Course Name'] = df['Course Name'].fillna('')
    df['Course Description'] = df['Course Description'].fillna('')
    df['Skills'] = df['Skills'].fillna('')
    df['Course Rating'] = pd.to_numeric(df['Course Rating'], errors='coerce').fillna(4.0)
    df['Course URL'] = df['Course URL'].fillna('#')
    df['tags'] = (df['Course Name'].astype(str) + ' ' + 
                  df['Course Description'].astype(str) + ' ' + 
                  df['Skills'].astype(str))
    df['tags'] = df['tags'].apply(clean_text)
    stop_words = set([
        'the', 'a', 'an', 'and', 'or', 'but', 'if', 'because', 'as', 'what', 'which', 
        'this', 'that', 'these', 'those', 'then', 'just', 'so', 'than', 'such', 'both', 
        'through', 'about', 'for', 'is', 'of', 'while', 'during', 'to', 'from', 'in', 
        'on', 'by', 'with', 'at', 'be', 'have', 'has', 'had', 'do', 'does', 'did', 
        'will', 'would', 'should', 'could', 'can', 'may', 'might', 'must', 'shall'
    ])
    df['cleaned_tags'] = df['tags'].apply(
        lambda text: ' '.join([word for word in text.split() if word not in stop_words and len(word) > 2])
    )
    def simple_stem(text):
        words = text.split()
        stemmed = []
        for word in words:
            if word.endswith('ing') and len(word) > 4:
                stemmed.append(word[:-3])
            elif word.endswith('ed') and len(word) > 3:
                stemmed.append(word[:-2])
            elif word.endswith('s') and len(word) > 3 and not word.endswith('ss'):
                stemmed.append(word[:-1])
            else:
                stemmed.append(word)
        return ' '.join(stemmed)
    df['processed_tags'] = df['cleaned_tags'].apply(simple_stem)
    return df

def create_vectorizer_and_model(df):
    valid_mask = df['processed_tags'].str.len() > 0
    df_valid = df[valid_mask].copy()
    if len(df_valid) == 0:
        return None, None, None, df
    tfidf = TfidfVectorizer(
        max_features=5000,
        ngram_range=(1, 2),
        min_df=1,
        max_df=0.95
    )
    try:
        vectors = tfidf.fit_transform(df_valid['processed_tags'])
        model = NearestNeighbors(
            n_neighbors=min(20, len(df_valid)),
            metric='cosine',
            algorithm='brute'
        )
        model.fit(vectors)
        return tfidf, vectors, model, df_valid
    except Exception:
        return None, None, None, df

def preprocess_query(query, tfidf):
    if not query or not tfidf:
        return None
    query_clean = clean_text(query)
    stop_words = set([
        'the', 'a', 'an', 'and', 'or', 'but', 'if', 'because', 'as', 'what', 'which', 
        'this', 'that', 'these', 'those', 'then', 'just', 'so', 'than', 'such', 'both', 
        'through', 'about', 'for', 'is', 'of', 'while', 'during', 'to', 'from', 'in', 
        'on', 'by', 'with', 'at', 'be', 'have', 'has', 'had', 'do', 'does', 'did', 
        'will', 'would', 'should', 'could', 'can', 'may', 'might', 'must', 'shall'
    ])
    query_words = [word for word in query_clean.split() if word not in stop_words and len(word) > 2]
    if not query_words:
        return None
    query_processed = ' '.join(query_words)
    def simple_stem(text):
        words = text.split()
        stemmed = []
        for word in words:
            if word.endswith('ing') and len(word) > 4:
                stemmed.append(word[:-3])
            elif word.endswith('ed') and len(word) > 3:
                stemmed.append(word[:-2])
            elif word.endswith('s') and len(word) > 3 and not word.endswith('ss'):
                stemmed.append(word[:-1])
            else:
                stemmed.append(word)
        return ' '.join(stemmed)
    query_processed = simple_stem(query_processed)
    try:
        return tfidf.transform([query_processed])
    except Exception:
        return None

def recommend_courses(query, df, tfidf, vectors, model, n_recommendations=10, use_knn=True):
    if not query or tfidf is None:
        return []
    query_vector = preprocess_query(query, tfidf)
    if query_vector is None:
        return []
    try:
        seen = set()
        recommendations = []
        if use_knn and model is not None:
            n_neighbors = min(n_recommendations * 3, len(df))
            distances, indices = model.kneighbors(query_vector, n_neighbors=n_neighbors)
            for i, idx in enumerate(indices[0]):
                course_id = df.iloc[idx]['Course URL']
                if course_id in seen:
                    continue
                seen.add(course_id)
                similarity = max(0, 1 - distances[0][i])
                recommendations.append({
                    'course_name': df.iloc[idx]['Course Name'],
                    'rating': float(df.iloc[idx]['Course Rating']),
                    'similarity': float(similarity),
                    'url': df.iloc[idx]['Course URL'],
                    'description': df.iloc[idx].get('Course Description', '')[:100] + '...' if len(str(df.iloc[idx].get('Course Description', ''))) > 100 else df.iloc[idx].get('Course Description', ''),
                    'skills': df.iloc[idx].get('Skills', '')
                })
                if len(recommendations) >= n_recommendations:
                    break
        else:
            similarities = cosine_similarity(query_vector, vectors)[0]
            top_indices = similarities.argsort()[::-1]
            for idx in top_indices:
                if similarities[idx] > 0:
                    course_id = df.iloc[idx]['Course URL']
                    if course_id in seen:
                        continue
                    seen.add(course_id)
                    recommendations.append({
                        'course_name': df.iloc[idx]['Course Name'],
                        'rating': float(df.iloc[idx]['Course Rating']),
                        'similarity': float(similarities[idx]),
                        'url': df.iloc[idx]['Course URL'],
                        'description': df.iloc[idx].get('Course Description', '')[:100] + '...' if len(str(df.iloc[idx].get('Course Description', ''))) > 100 else df.iloc[idx].get('Course Description', ''),
                        'skills': df.iloc[idx].get('Skills', '')
                    })
                    if len(recommendations) >= n_recommendations:
                        break
        return recommendations
    except Exception:
        return []
   
def rating_dist():
    df = load_data()
    rating_dist = df['Course Rating'].value_counts().sort_index()
    return rating_dist.to_dict()