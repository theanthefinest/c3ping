import requests

response = requests.post(
    'http://localhost:8000/api/recommend/knn/',
    json={'course_name': 'Finance for Managers', 'top_n': 5}
)
print('Status code:', response.status_code)
print('Raw response:', response.text)
try:
    print('KNN Response:', response.json())
except Exception as e:
    print('Error decoding JSON:', e)