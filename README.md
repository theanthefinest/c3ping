# Mini-Django Course Recommendation Website

This project is a Django-based web application for course recommendation and analytics, utilizing machine learning and data visualization tools. It is designed to help users find suitable courses and analyze course data interactively.

## Features
- Course recommendation system using machine learning (scikit-learn, pandas, numpy)
- Data analytics and visualization (Plotly, Streamlit)
- Natural language processing (NLTK, spaCy)
- Modern, responsive UI with custom CSS

## Project Structure
```
CourseWebsite/
├── CourseWebsite/         # Django project settings
├── Website/              # Main Django app (models, views, recommender, etc.)
├── static/               # Static files (CSS, JS)
├── templates/            # HTML templates
├── db.sqlite3            # SQLite database
├── manage.py             # Django management script
├── Final_Coursera.csv    # Course data
├── requirements.txt      # Python dependencies
```

## Installation
1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/mini-django.git
   cd mini-django
   ```
2. **Create and activate a virtual environment:**
   ```sh
   python -m venv env
   .\env\Scripts\activate  # On Windows
   # Or
   source env/bin/activate  # On macOS/Linux
   ```
3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
4. **Apply migrations:**
   ```sh
   python manage.py migrate
   ```
5. **Run the development server:**
   ```sh
   python manage.py runserver
   ```
6. **Access the app:**
   Open your browser and go to `http://127.0.0.1:8000/`

## Usage
- Register or log in to access personalized recommendations.
- Use the analytics dashboard for course insights.
- Explore interactive visualizations and recommendations.

## Dependencies
- Django
- streamlit==1.25.0
- pandas==1.5.3
- numpy==1.24.3
- scikit-learn==1.2.2
- plotly==5.15.0
- nltk==3.8.1
- spacy==3.5.0

See `requirements.txt` for the full list.

## License
This project is licensed under the MIT License.

## Acknowledgements
- [Django](https://www.djangoproject.com/)
- [scikit-learn](https://scikit-learn.org/)
- [Streamlit](https://streamlit.io/)
- [Plotly](https://plotly.com/)
- [NLTK](https://www.nltk.org/)
- [spaCy](https://spacy.io/)
