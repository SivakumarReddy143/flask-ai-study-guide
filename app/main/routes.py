from flask import render_template, request, Blueprint, jsonify, session, redirect, url_for
from helper import get_youtube_urls, embed_codes, chat
from firebase_admin import auth as firebase_auth
from quiz.chat_utils import generate_quiz
from functools import wraps

# 🔐 Login Required Decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('main.auth'))  # Redirect to login page
        return f(*args, **kwargs)
    return decorated_function

main = Blueprint('main', __name__)
print("Defining routes in routes.py...")

@main.route('/')
@login_required
def index():
    print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
    print("Session:", session)
    print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
    return render_template('index.html')

@main.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        topic = request.form.get('topic')
        difficulty = request.form.get('difficulty')
        num_questions = request.form.get('num_questions')
        quiz_data = generate_quiz(topic, difficulty, int(num_questions))
        return render_template('quiz.html', quiz=quiz_data, topic=topic)
    return render_template('quiz.html')

@main.route('/video_resources')
def video_resources():
    query = request.args.get('query', 'deep learning')  
    urls = get_youtube_urls(query)
    iframe_list = embed_codes(urls)
    return render_template('video_resources.html', query=query, video_urls=iframe_list)

@main.route('/notes')
def notes():
    return render_template('notes.html')

@main.route('/chatbot', methods=['GET', 'POST'])
def chatbot():
    response = ""
    if request.method == 'POST':
        user_input = request.form.get('user_input')
        response = chat(user_input)
    return render_template('chatbot.html', response=response)

@main.route("/auth")
def auth():
    return render_template("auth.html")

@main.route('/verify-token', methods=['POST'])
def verify_token():
    try:
        data = request.get_json()
        id_token = data.get('token')

        # 🔍 Verify the token using Firebase Admin SDK
        decoded_token = firebase_auth.verify_id_token(id_token)
        uid = decoded_token['uid']
        email = decoded_token.get('email', '')

        # 🔐 Store info in session
        session['user_id'] = uid
        session['user_email'] = email

        print("✅ Token decoded:", decoded_token)
        print("🎯 Session Set:", session)

        return jsonify({'message': f'Login verified for {email}', 'uid': uid})
    
    except Exception as e:
        return jsonify({'message': f'Failed to verify token: {str(e)}'}), 400

@main.route('/logout', methods=['POST'])
def logout():
    session.clear()
    print("🔓 Flask session cleared.")
    return jsonify({"message": "Logged out"})
