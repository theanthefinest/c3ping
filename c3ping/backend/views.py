from django.shortcuts import render, redirect
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RecommendSerializer
import pandas as pd
from .functions import load_data, preprocess_data, create_vectorizer_and_model, recommend_courses
from django.shortcuts import render
import os 

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


df = preprocess_data(load_data())
tfidf, vectors, knn_model, df_valid = create_vectorizer_and_model(df)

class KNN_RecommendAPIView(APIView):
    def post(self, request):
        serializer = RecommendSerializer(data = request.data)
        if serializer.is_valid():
            query = serializer.validated_data['course_name']
            top_n = serializer.validated_data['top_n']
            results = recommend_courses(query, df_valid, tfidf, vectors, knn_model, n_recommendations=top_n, use_knn=True)
            return Response({'recommendations': results})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def home(request):
    return render(request, 'home.html')

def recommend_page(request):
    return render(request, 'recommend.html')

def analytics(request):
    df = load_data()
    top_df = df.sort_values(by=['Course Rating'], ascending=False).head(15)
    
    top_courses = []
    for _, course in top_df.iterrows():
        top_courses.append({
            'course_name': course['Course Name'],
            'rating': float(course['Course Rating']),
            'similarity': 1.0,  
            'url': course['Course URL'],
            'description': course.get('Course Description', '')[:100] + '...' if len(str(course.get('Course Description', ''))) > 100 else course.get('Course Description', ''),
            'skills': course.get('Skills', '')
        })
    
    context = {
        'top_courses': top_courses
    }
    
    return render(request, 'analytics.html', context)

def profile(request):
    return render(request, 'profile.html')

def distribution(request):
    return render(request, 'distribution.html')