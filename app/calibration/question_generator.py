from typing import List, Dict, Optional
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import ChatMessage
import json
from app.prompts import QUESTION_GENERATOR_PROMPT, GeneratedQuestion, QUESTION_CATEGORY_PROMPTS
from app.config import load_config
from app.calibration.storage import CalibrationQuestionStorage


class QuestionGenerationError(Exception):
    pass

def generate_calibration_question(
    table_name: str,
    table_description: str,
    columns_info: List[Dict],
    previous_questions: List[str],
    target_category: str
) -> GeneratedQuestion:
    """
    Generate a single calibration question using LLM.
    """
    config = load_config()
    llm = ChatOpenAI(
        temperature=0.8,  
        model_name=config['model_name']
    )
    
    # Format columns info for prompt
    columns_str = "\n".join([
        f"- {col['name']} ({col['type']})" 
        for col in columns_info
    ])
    
    # Format previous questions for prompt
    prev_questions_str = "\n".join([
        f"- {q}" for q in previous_questions
    ]) if previous_questions else "None"

    category_prompt = QUESTION_CATEGORY_PROMPTS[target_category]
    
    # Generate the prompt
    prompt = QUESTION_GENERATOR_PROMPT.format(
        table_name=table_name,
        table_description=table_description,
        columns_info=columns_str,
        previous_questions=prev_questions_str,
        target_category=target_category,
        category_prompt=category_prompt
    )
    
    # Get response from LLM
    messages = [
        ChatMessage(role="system", content="You are a analyst generating calibration questions."),
        ChatMessage(role="user", content=prompt)
    ]
    
    try:
        response = llm(messages)
        question_data = json.loads(response.content)
        # Set default empty string for reasoning if not provided
        processed_data = {
            'question': question_data['question'],
            'category': question_data['category'],
            'source_columns': question_data['source_columns']
        }
        return GeneratedQuestion(**processed_data)
    except json.JSONDecodeError as e:
        raise QuestionGenerationError(f"Failed to parse LLM response as JSON: {str(e)}")
    except Exception as e:
        raise QuestionGenerationError(f"Error generating question: {str(e)}")

def generate_question_set(
    table_name: str,
    table_description: str,
    columns_info: List[Dict],
    questions_per_category: Optional[Dict[str, int]] = None,
    storage: Optional[CalibrationQuestionStorage] = None
) -> List[GeneratedQuestion]:
    """
    Generate a set of calibration questions across all categories.
    
    Args:
        table_name: Name of the table
        table_description: Description of the table
        columns_info: List of column information dictionaries
        questions_per_category: Optional dict specifying number of questions per category.
                              If None, uses values from config.
        storage: Optional storage instance to persist questions
    Returns:
        List of GeneratedQuestion objects
    """
    if questions_per_category is None:
        config = load_config()
        questions_per_category = config['questions_per_category']
    print(questions_per_category)
    categories = [
        "single_column",
        "multi_column",
        "table_purpose",
        "business_logic"
    ]
    
    generated_questions = []
    previous_questions = []
    i = 1
    for category, num_questions in questions_per_category.items():
        for _ in range(num_questions):
            try:
                question = generate_calibration_question(
                    table_name=table_name,
                    table_description=table_description,
                    columns_info=columns_info,
                    previous_questions=previous_questions,
                    target_category=category
                )
                print(f'Question number {i}')
                i += 1
                generated_questions.append(question)
                previous_questions.append(question.question)
            except QuestionGenerationError as e:
                print(f"Failed to generate question for category {category}: {str(e)}")
                continue
    
    if storage and generated_questions:
        storage.store_questions(generated_questions)
    
    return generated_questions
