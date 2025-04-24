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
        
        Return the questions as a simple list, one question per line. Do not include any additional text or formatting."""
    else:
        prompt = f"""Based on the following resume content, generate {num_questions} non-technical interview questions 
        that would be relevant for this candidate's experience and skills. Focus on soft skills, teamwork, 
        problem-solving, and behavioral aspects.
        
        Resume Content:
        {docs}
        
        Return the questions as a simple list, one question per line. Do not include any additional text or formatting."""
    
    # Generate questions using Groq
    response = groq_chat.invoke(prompt)
    
    # Extract questions from the response
    questions = []
    for line in response.content.split('\n'):
        line = line.strip()
        if line and not line.startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '0.')):
            questions.append(line)
    
    # Ensure we have exactly num_questions
    return questions[:num_questions] 