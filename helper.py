import os
import re
from langchain_tavily import TavilySearch
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv
from tempfile import NamedTemporaryFile
from langchain.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.question_answering import load_qa_chain
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.tools import TavilySearchResults
from typing import List, Dict
import json
from werkzeug.utils import secure_filename

load_dotenv()
os.environ['HF_TOKEN'] = os.getenv("HF_TOKEN")
os.environ['GROQ_API_KEY'] = os.getenv("GROQ_API_KEY")
os.environ['TAVILY_API_KEY'] = os.getenv("TAVILY_API_KEY")

llm = ChatGroq(model="gemma2-9b-it", api_key=os.getenv("GROQ_API_KEY"), temperature=0)
tool = TavilySearchResults(max_results=100, search_depth='advanced')

def get_llm():
    try:
        return ChatGroq(
            temperature=0.7,
            model="gemma2-9b-it"
        )
    except Exception as e:
        raise Exception(f"Failed to initialize AI model: {str(e)}")

def get_embed_code(video_url):
    video_id = re.search(r"v=([^&]+)", video_url)
    if video_id:
        # return f'<iframe width="360" height="315" src="https://www.youtube.com/embed/{video_id.group(1)}" frameborder="0" allowfullscreen></iframe>'
        return video_id.group(1)
    return None

def is_youtube_url(url: str) -> bool:
    youtube_patterns = [
        r'^https?://(www\.)?youtube\.com/watch\?v=.+',
        r'^https?://youtu\.be/.+'
    ]
    
    return any(re.match(pattern, url) for pattern in youtube_patterns)

def get_youtube_urls(query="machine learning"):
    tool = TavilySearch(max_results=50)
    response = tool.invoke({'query': f"give me links of {query} videos in youtube. you must provide only youtube urls. url format: https://www.youtube.com/"})
    youtube_urls = []
    for i in response["results"]:
        if is_youtube_url(i['url']):
            youtube_urls.append(i['url'])
    return youtube_urls

def embed_codes(urls):
    return [get_embed_code(url) for url in urls]

def chat(query="hello"):
    llm = ChatGroq(model="gemma2-9b-it")
    return llm.invoke(query).content

def get_evaluation_prompt():
    return ChatPromptTemplate.from_template("""
    Analyze the provided resume and generate a concise evaluation within 20-30 lines. 
    Rate the resume out of 10 based on the following criteria:
    - Content relevance
    - Clarity
    - Structure
    - Achievements
    - Presentation
    - Skills

    Ensure the response includes:
    1. **Overall Rating**: Start with the score out of 10 and provide a brief justification.
    2. **Strengths**: Highlight positive aspects in 5-6 lines.
    3. **Suggestions for Improvement**: Mention areas for enhancement in 10-15 lines.
    4. **Suggest Skills**: Mention what skills the user is lacking.
    5. **Job Roles**: Suggest relevant jobs.

    Context:
    {context}

    Question: Evaluate this resume thoroughly and respond concisely in 10 lines.
    """)

def get_job_search_prompt():
    return ChatPromptTemplate.from_template("""
    Generate a concise search query based on the provided resume to find job opportunities.
    Focus on:
    1. Key skills from the resume
    2. Experience level
    3. Industry-specific terms
    4. Relevant job titles
    
    Format the response as a simple, clear search query without any additional text or explanation.
    For example: "software developer python javascript 3 years experience" or "data analyst SQL Python entry level"
    
    Context:
    {context}
    
    Question: Generate a focused job search query based on this resume.
    """)

def get_technical_prompt():
    return ChatPromptTemplate.from_template("""
    Based on the provided resume, generate 20 technical interview questions. These should cover:
    1. Technical skills
    2. Relevant projects
    3. Industry-specific knowledge
    Context:
    {context}
    Question: Generate 20 technical interview questions with answers based on the resume.
    """)

def get_non_technical_prompt():
    return ChatPromptTemplate.from_template("""
    Based on the provided resume, generate 20 non-technical interview questions. These should focus on:
    1. Behavioral aspects
    2. Teamwork and collaboration
    3. Problem-solving and leadership
    Context:
    {context}
    Question: Generate 20 non-technical interview questions with answers based on the resume.
    """)

def process_resume(file):
    # Save the uploaded file temporarily
    filename = secure_filename(file.filename)
    file_path = os.path.join('uploads', filename)
    file.save(file_path)
    
    try:
        # Load PDF using PyPDFLoader
        loader = PyPDFLoader(file_path)
        docs = loader.load()
        
        # Split text into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        split_docs = text_splitter.split_documents(docs)
        
        # Create embeddings with explicit device handling
        embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2"
        )
        
        # Create vector store
        vectorstore = FAISS.from_documents(split_docs, embeddings)
        
        return vectorstore
        
    finally:
        # Clean up the temporary file
        if os.path.exists(file_path):
            os.remove(file_path)

def generate_interview_questions(retriever, num_questions, technical=True):
    """
    Generate interview questions based on the resume content.
    
    Args:
        retriever: The retriever object containing resume information
        num_questions: Number of questions to generate
        technical: Whether to generate technical questions (True) or non-technical questions (False)
    
    Returns:
        List of generated questions
    """
    # Get relevant documents from retriever
    docs = retriever.invoke("Generate interview questions")
    
    # Initialize Groq chat model
    groq_chat = ChatGroq(temperature=0.7, model_name="gemma2-9b-it")
    
    if technical:
        prompt = f"""Based on the following resume content, generate {num_questions} technical interview questions 
        that would be relevant for this candidate's experience and skills. Focus on their technical expertise, 
        programming languages, and specific technologies mentioned in their resume.
        
        Resume Content:
        {docs}
        
        Format the questions as a JSON array of strings."""
    else:
        prompt = f"""Based on the following resume content, generate {num_questions} non-technical interview questions 
        that would be relevant for this candidate's experience and skills. Focus on soft skills, teamwork, 
        problem-solving, and behavioral aspects.
        
        Resume Content:
        {docs}
        
        Format the questions as a JSON array of strings."""
    
    # Generate questions using Groq
    response = groq_chat.invoke(prompt)
    
    try:
        # Parse the response as JSON
        questions = json.loads(response.content)
        return questions
    except json.JSONDecodeError:
        # If JSON parsing fails, split the response by newlines and clean up
        questions = [q.strip() for q in response.content.split('\n') if q.strip()]
        return questions[:num_questions]

