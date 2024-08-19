import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Define constants from environment variables
LLM_API_KEY = os.getenv('LLM_API_KEY')
LLM_MODEL = os.getenv('LLM_MODEL')
LLM_TIMEOUT = int(os.getenv('LLM_TIMEOUT', 40))  # Default to 40 if not set
MAIN_AGENT_SYSTEM_MESSAGE = os.getenv('MAIN_AGENT_SYSTEM_MESSAGE')
IS_DEBUG_MODE = os.getenv('IS_DEBUG_MODE', 'False').lower() in ['true', '1', 't']  # Converts to boolean
MAX_AGENT_ITERATIONS = int(os.getenv('MAX_AGENT_ITERATIONS', 5))  # Default to 5 if not set

# Database connection details
TIDB_CONNECTION_STRING = os.getenv('TIDB_CONNECTION_STRING')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
DB_SSL_PATH = os.getenv('DB_SSL_PATH')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = int(os.getenv('DB_PORT', 4000))  # Default to 4000 if not set
