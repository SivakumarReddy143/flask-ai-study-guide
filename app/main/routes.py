from flask import render_template, request, Blueprint, jsonify, session, redirect, url_for, current_app
from langchain_groq import ChatGroq
from helper import generate_interview_questions, get_youtube_urls, embed_codes, chat, process_resume, get_evaluation_prompt, get_job_search_prompt, get_technical_prompt, get_non_technical_prompt, llm, tool
from firebase_admin import auth as firebase_auth
from quiz.chat_utils import generate_quiz
from functools import wraps
from langchain.chains.question_answering import load_qa_chain
import os
from markdown import markdown
from dotenv import load_dotenv
import traceback
import sys
from werkzeug.utils import secure_filename
from langchain_community.tools import TavilySearchResults
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")


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

        return jsonify({'message': f'Login verified for {email}', 'uid': uid})
    
    except Exception as e:
        return jsonify({'message': f'Failed to verify token: {str(e)}'}), 400

@main.route('/logout', methods=['POST'])
def logout():
    session.clear()
    print("🔓 Flask session cleared.")
    return jsonify({"message": "Logged out"})

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'pdf'

@main.route("/test", methods=["GET"])
def test():
    return jsonify({"message": "Server is working!"})

@main.route("/resume-evaluation", methods=["GET", "POST"])
def resume_evaluation():
    if request.method == "POST":
        try:
            if "resume" not in request.files:
                return jsonify({"error": "No file uploaded"}), 400
            
            file = request.files["resume"]
            if file.filename == "":
                return jsonify({"error": "No file selected"}), 400
            
            if not file.filename.endswith('.pdf'):
                return jsonify({"error": "Please upload a PDF file"}), 400

            print(f"Processing file for evaluation: {file.filename}")
            vectorstore = process_resume(file)
            retriever = vectorstore.as_retriever()
            docs = retriever.get_relevant_documents("Evaluate this resume thoroughly.")

            qa_chain = load_qa_chain(llm=llm, chain_type="stuff", prompt=get_evaluation_prompt())
            response = qa_chain.run(input_documents=docs, question="Evaluate this resume thoroughly")
            return jsonify({"success": True, "result": markdown(response)})

        except Exception as e:
            print(f"Error in resume evaluation: {str(e)}")
            print(traceback.format_exc())
            return jsonify({"error": str(e)}), 500

    return render_template("resume_evaluation.html")

@main.route("/job-search", methods=["GET", "POST"])
def job_search():
    if request.method == "POST":
        try:
            if "resume" not in request.files:
                return jsonify({"error": "No file uploaded"}), 400
            
            file = request.files["resume"]
            if file.filename == "":
                return jsonify({"error": "No file selected"}), 400
            
            if not file.filename.endswith('.pdf'):
                return jsonify({"error": "Please upload a PDF file"}), 400

            print(f"Processing file for job search: {file.filename}")
            vectorstore = process_resume(file)
            retriever = vectorstore.as_retriever()
            docs = retriever.get_relevant_documents("Generate job search query")

            qa_chain = load_qa_chain(llm=llm, chain_type="stuff", prompt=get_job_search_prompt())
            job_query = qa_chain.run(input_documents=docs, question="Generate a search query for job portals")
            
            search_results = tool.invoke({'query': f"{job_query} jobs careers"})
            
            # Filter job-related results
            filtered_results = [
                result for result in search_results
                if isinstance(result, dict) and 'url' in result and 'title' in result
                and any(keyword in result['url'].lower() or keyword in result['title'].lower() 
                       for keyword in ['job', 'career', 'position', 'hiring', 'vacancy'])
            ]

            return jsonify({"success": True, "result": filtered_results[:10]})

        except Exception as e:
            print(f"Error in job search: {str(e)}")
            print(traceback.format_exc())
            return jsonify({"error": str(e)}), 500

    return render_template("job_search.html")

@main.route("/technical-interview", methods=["GET", "POST"])
def technical_interview():
    if request.method == "POST":
        try:
            if "resume" not in request.files:
                return jsonify({"error": "No file uploaded"}), 400
            
            file = request.files["resume"]
            if file.filename == "":
                return jsonify({"error": "No file selected"}), 400
            
            if not file.filename.endswith('.pdf'):
                return jsonify({"error": "Please upload a PDF file"}), 400

            print(f"Processing file for technical questions: {file.filename}")
            vectorstore = process_resume(file)
            retriever = vectorstore.as_retriever()
            docs = retriever.get_relevant_documents("Generate technical interview questions")

            qa_chain = load_qa_chain(llm=llm, chain_type="stuff", prompt=get_technical_prompt())
            questions = qa_chain.run(input_documents=docs, question="Generate technical interview questions")
            return jsonify({"success": True, "result": markdown(questions)})

        except Exception as e:
            print(f"Error in technical interview: {str(e)}")
            print(traceback.format_exc())
            return jsonify({"error": str(e)}), 500

    return render_template("technical_interview.html")

@main.route("/non-technical-interview", methods=["GET", "POST"])
def non_technical_interview():
    if request.method == "POST":
        try:
            if "resume" not in request.files:
                return jsonify({"error": "No file uploaded"}), 400
            
            file = request.files["resume"]
            if file.filename == "":
                return jsonify({"error": "No file selected"}), 400
            
            if not file.filename.endswith('.pdf'):
                return jsonify({"error": "Please upload a PDF file"}), 400

            print(f"Processing file for non-technical questions: {file.filename}")
            vectorstore = process_resume(file)
            retriever = vectorstore.as_retriever()
            docs = retriever.get_relevant_documents("Generate non-technical interview questions")

            qa_chain = load_qa_chain(llm=llm, chain_type="stuff", prompt=get_non_technical_prompt())
            questions = qa_chain.run(input_documents=docs, question="Generate non-technical interview questions")
            return jsonify({"success": True, "result": markdown(questions)})

        except Exception as e:
            print(f"Error in non-technical interview: {str(e)}")
            print(traceback.format_exc())
            return jsonify({"error": str(e)}), 500

    return render_template("non_technical_interview.html")

# Landing page for all resume services
@main.route("/resume-services")
def resume_services():
    return render_template("resume_services.html")
