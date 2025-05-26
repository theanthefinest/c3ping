from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .recommender import get_recommendations
import json
from django.utils.safestring import mark_safe
from .functions import rating_dist, load_data

# Create your views here.

def home(request):
    return render(request, "home.html")

def analytics(request):
    rating_dist_data = rating_dist()  # Call the function to get the data
    rating_dist_json = mark_safe(json.dumps(rating_dist_data))
    df = load_data()
    top_courses_df = df.sort_values('Course Rating', ascending=False).head(5)
    top_courses = []
    for _, row in top_courses_df.iterrows():
        skills_str = row.get('Skills', '')
        skills_list = [s.strip() for s in skills_str.split(',') if s.strip()]
        course_dict = {
            'Course_Name': row.get('Course Name', 'N/A'),
            'Course_Description': row.get('Course Description', ''),
            'Skills': skills_str,
            'Skills_list': skills_list,
            'Course_Rating': row.get('Course Rating', 0),
            'Course_URL': row.get('Course URL', '#')
        }
        top_courses.append(course_dict)
    
    return render(request, 'analytics.html', {
        'rating_dist_json': rating_dist_json,
        'top_courses': top_courses,
    })

def profile(request):
    return render(request, "profile.html")

def recommend_view(request):
    recommendations = []
    query = ""
    if request.method == "POST":
        query = request.POST.get("query", "")
        recommendations = get_recommendations(query)
        for rec in recommendations:
            rec['skills_list'] = [s.strip() for s in rec.get('skills', '').split(',') if s.strip()]
    return render(request, "recommend.html", {"recommendations": recommendations, "query": query})

