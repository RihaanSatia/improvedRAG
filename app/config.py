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
    
    # Get total questions from env or use default
    total_questions = int(os.getenv('TOTAL_CALIBRATION_QUESTIONS', '14'))
    
    # Calculate distribution based on percentages
    questions_per_category = {
        'single_column': int(total_questions * 0.21),    # 21%
        'multi_column': int(total_questions * 0.21),     # 21%
        'table_purpose': int(total_questions * 0.14),    # 14%
        'business_logic': int(total_questions * 0.44)    # 44%
    }
    
    # Ensure we don't lose any questions due to rounding
    total_allocated = sum(questions_per_category.values())
    if total_allocated < total_questions:
        # Add remaining questions to business_logic category
        questions_per_category['business_logic'] += (total_questions - total_allocated)
    
    return {
        'openai_api_key': os.getenv('OPENAI_API_KEY'),
        'model_name': os.getenv('MODEL_NAME', 'gpt-3.5-turbo'),
        'questions_per_category': questions_per_category
    }
