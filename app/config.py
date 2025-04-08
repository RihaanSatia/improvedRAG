import os
from dotenv import load_dotenv

class ConfigError(Exception):
    pass

def load_config():
    load_dotenv()
    
    required_vars = ['OPENAI_API_KEY']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        raise ConfigError(
            f"Missing required environment variables: {', '.join(missing_vars)}"
        )
    
    return {
        'openai_api_key': os.getenv('OPENAI_API_KEY'),
        'sqlite_path': os.path.join("data", "imdb_full.sqlite"),
        'model_name': os.getenv('MODEL_NAME', 'gpt-3.5-turbo')
    }