from dotenv import load_dotenv
import os

class Config:
    """Base configuration."""
    load_dotenv()
    SECRET_KEY = os.getenv("SECRET_KEY") or "Siva@143"
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    DEBUG = True  # Set to False in production environmentdfs

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DEBUG = True